from uuid import uuid4

import pytest

from qa_api.assertions import (
    assert_error_codes,
    assert_item,
    assert_saved_item,
    assert_saved_statistics,
    assert_seller_items,
    expect_json,
    expect_status,
    only_record,
)
from qa_api.data import item_payload


def test_del_01_delete_removes_item(api, account, create_item):
    payload = item_payload(account.id)
    item_id = create_item(account, payload)
    seller_path = f"/api/1/{account.id}/item"
    before = expect_json(api.request("GET", seller_path, token=account.token), 200)
    assert_item(only_record(before), item_id, payload)

    response = api.request("DELETE", f"/api/2/item/{item_id}", token=account.token)

    expect_status(response, 200)
    expect_status(api.request("GET", f"/api/1/item/{item_id}", token=account.token), 404)
    assert expect_json(api.request("GET", seller_path, token=account.token), 200) == []


def test_del_02_delete_missing_item_returns_404(api, account, create_item):
    payload = item_payload(account.id)
    existing = create_item(account, payload)
    response = api.request("DELETE", f"/api/2/item/{uuid4()}", token=account.token)

    expect_status(response, 404)
    assert_saved_item(api, account, existing, payload)
    assert_seller_items(api, account, {existing: payload})


def test_exp_04_delete_keeps_other_item_with_same_payload(api, account, create_item):
    payload = item_payload(account.id)
    first_id = create_item(account, payload)
    second_id = create_item(account, payload)
    assert first_id != second_id
    first_path = f"/api/2/item/{first_id}"

    expect_status(api.request("DELETE", first_path, token=account.token), 200)
    expect_status(api.request("DELETE", first_path, token=account.token), 404)
    expect_status(api.request("GET", f"/api/1/item/{first_id}", token=account.token), 404)

    items = expect_json(api.request("GET", f"/api/1/{account.id}/item", token=account.token), 200)
    assert_item(only_record(items), second_id, payload)
    for version in (1, 2):
        assert_saved_statistics(api, account, second_id, version, payload["statistics"])


@pytest.mark.parametrize(
    "was_created",
    [pytest.param(False, id="never-created"), pytest.param(True, id="deleted")],
)
def test_exp_07_delete_missing_item_status_is_consistent(api, account, create_item, was_created):
    item_id = create_item(account) if was_created else str(uuid4())
    path = f"/api/2/item/{item_id}"
    if was_created:
        expect_status(api.request("DELETE", path, token=account.token), 200)

    response = api.request("DELETE", path, token=account.token)

    assert_error_codes(response, (404,), issue="API-06")
