from uuid import uuid4

import pytest

from qa_api.assertions import (
    assert_error_codes,
    assert_item,
    assert_saved_item,
    assert_saved_statistics,
    expect_json,
    expect_status,
    only_record,
)
from qa_api.data import item_payload


def test_item_06_get_missing_item_returns_404(api, account):
    response = api.request("GET", f"/api/1/item/{uuid4()}", token=account.token)

    expect_status(response, 404)


@pytest.mark.parametrize(
    ("method", "path"),
    [
        pytest.param("GET", "/api/1/item/not-a-uuid", id="ID-01-get-item"),
        pytest.param("GET", "/api/1/statistic/not-a-uuid", id="ID-01-stats-v1"),
        pytest.param("DELETE", "/api/2/item/not-a-uuid", id="ID-01-delete"),
    ],
)
def test_invalid_uuid_is_rejected(api, account, create_item, method, path):
    if method == "DELETE":
        payload = item_payload(account.id)
        existing = create_item(account, payload)
    response = api.request(method, path, token=account.token)

    expect_status(response, 400)
    if method == "DELETE":
        assert_saved_item(api, account, existing, payload)


def test_exp_09_uppercase_uuid_addresses_the_same_item(api, account, create_item):
    payload = item_payload(account.id)
    item_id = create_item(account, payload)
    uppercase_id = item_id.upper()

    response = api.request("GET", f"/api/1/item/{uppercase_id}", token=account.token)

    assert_item(only_record(expect_json(response, 200)), item_id, payload)
    for version in (1, 2):
        assert_saved_statistics(api, account, uppercase_id, version, payload["statistics"])
    deleted = api.request("DELETE", f"/api/2/item/{uppercase_id}", token=account.token)
    expect_status(deleted, 200)
    expect_status(api.request("GET", f"/api/1/item/{item_id}", token=account.token), 404)


def test_exp_13_missing_item_id_status_is_consistent(api, account):
    response = api.request("GET", "/api/1/item/", token=account.token)

    assert_error_codes(response, (400, 404), issue="API-09")
