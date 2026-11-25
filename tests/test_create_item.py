from uuid import uuid4

import pytest

from qa_api.assertions import (
    assert_error_reason,
    assert_item,
    assert_saved_item,
    assert_saved_statistics,
    assert_seller_items,
    expect_json,
    expect_status,
    item_id_from_creation,
    only_record,
)
from qa_api.data import item_payload


def test_item_01_create_and_get_item(api, account, post_item):
    payload = item_payload(account.id, name=f"Диван «Лето» {uuid4().hex[:8]}")

    response = post_item(account, payload)
    expect_json(response, 200)
    item_id = item_id_from_creation(response)

    assert_saved_item(api, account, item_id, payload)


def test_item_02_create_accepts_identical_items(api, account, create_item):
    payload = item_payload(account.id)

    first_id = create_item(account, payload)
    second_id = create_item(account, payload)

    assert first_id != second_id, "Одинаковые тела запросов должны создать разные UUID"
    assert_saved_item(api, account, first_id, payload)
    assert_saved_item(api, account, second_id, payload)


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        pytest.param("name", 123, id="ITEM-03-name"),
        pytest.param("price", "9900", id="ITEM-03-price"),
        pytest.param("sellerID", None, id="ITEM-03-seller-id"),
        pytest.param("statistics", [], id="ITEM-03-statistics"),
    ],
)
def test_create_rejects_wrong_json_type(api, account, post_item, field, invalid_value):
    payload = item_payload(account.id)
    payload[field] = str(account.id) if field == "sellerID" else invalid_value

    response = post_item(account, payload)

    expect_status(response, 400)
    assert_seller_items(api, account, {})


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("likes", id="ITEM-07-likes"),
        pytest.param("viewCount", id="ITEM-07-view-count"),
        pytest.param("contacts", id="ITEM-07-contacts"),
    ],
)
def test_create_accepts_zero_counter(api, account, post_item, field):
    payload = item_payload(account.id)
    payload["statistics"][field] = 0

    response = post_item(account, payload)

    expect_json(response, 200, issue="API-01")
    item_id = item_id_from_creation(response)
    assert_saved_item(api, account, item_id, payload)


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("likes", id="ITEM-08-likes"),
        pytest.param("viewCount", id="ITEM-08-view-count"),
        pytest.param("contacts", id="ITEM-08-contacts"),
    ],
)
def test_create_rejects_negative_counter(api, account, post_item, field):
    payload = item_payload(account.id)
    payload["statistics"][field] = -1

    response = post_item(account, payload)

    expect_status(response, 400, issue="API-01")
    assert_seller_items(api, account, {})


@pytest.mark.parametrize(
    "seller_id",
    [
        pytest.param(None, id="ITEM-09-missing-seller-id"),
        pytest.param(0, id="ITEM-09-zero-seller-id"),
    ],
)
def test_create_rejects_invalid_seller_id(api, account, post_item, seller_id):
    payload = item_payload(account.id)
    if seller_id is None:
        del payload["sellerID"]
    else:
        payload["sellerID"] = seller_id

    expect_status(post_item(account, payload), 400)
    assert_seller_items(api, account, {})


def test_exp_01_create_rejects_negative_price(api, account, post_item):
    payload = item_payload(account.id, price=-1)

    response = post_item(account, payload)

    expect_status(response, 400, issue="API-03")
    assert_seller_items(api, account, {})


def test_exp_02_create_rejects_whitespace_only_name(api, account, post_item):
    payload = item_payload(account.id, name="   ")

    response = post_item(account, payload)

    expect_status(response, 400, issue="API-04")
    assert_seller_items(api, account, {})


@pytest.mark.parametrize("field", ["name", "price", "statistics"])
def test_exp_06_rejected_creation_leaves_seller_list_empty(api, account, post_item, field):
    payload = item_payload(account.id)
    del payload[field]

    expect_status(post_item(account, payload), 400)
    assert_seller_items(api, account, {})


def test_exp_08_accepted_large_integers_are_preserved(api, account, post_item):
    counters = dict.fromkeys(("likes", "viewCount", "contacts"), 2**53 + 1)
    payload = item_payload(account.id, price=2**63 - 1, statistics=counters)
    list_path = f"/api/1/{account.id}/item"

    response = post_item(account, payload)

    if response.status_code == 400:
        assert expect_json(api.request("GET", list_path, token=account.token), 200) == []
        return

    expect_json(response, 200)
    item_id = item_id_from_creation(response)
    assert_saved_item(api, account, item_id, payload)
    items = expect_json(api.request("GET", list_path, token=account.token), 200)
    assert_item(only_record(items), item_id, payload)
    for version in (1, 2):
        assert_saved_statistics(api, account, item_id, version, counters)


def test_exp_11_wrong_price_type_does_not_report_missing_body(api, account, post_item):
    payload = item_payload(account.id, price="abc")

    response = post_item(account, payload)

    body = expect_json(response, 400, issue="API-07")
    assert_seller_items(api, account, {})
    control = payload.copy()
    del control["price"]
    missing = post_item(account, control)
    missing_body = expect_json(missing, 400, issue="API-07")
    assert_seller_items(api, account, {})
    assert_error_reason(
        missing_body,
        ("price", "цен", "стоимост"),
        ("required", "missing", "обязат", "отсутств"),
        issue="API-07",
    )
    assert_error_reason(
        body,
        ("price", "цен", "стоимост"),
        (
            "type",
            "number",
            "numeric",
            "integer",
            "int64",
            "int32",
            "тип",
            "числ",
            "целочисл",
            "чисел",
        ),
        issue="API-07",
        misleading="не передано тело объявления",
    )


def test_item_10_own_user_header_does_not_replace_required_seller(
    api, account, post_item, monkeypatch
):
    payload = item_payload(account.id)
    del payload["sellerID"]
    with monkeypatch.context() as headers:
        headers.setitem(api.session.headers, "X-UserId", str(account.id))
        response = post_item(account, payload)

    expect_status(response, 400)
    assert_seller_items(api, account, {})


@pytest.mark.parametrize("field", ["likes", "viewCount", "contacts"])
def test_item_11_create_requires_each_counter(api, account, post_item, field):
    payload = item_payload(account.id)
    del payload["statistics"][field]
    expect_status(post_item(account, payload), 400)
    assert_seller_items(api, account, {})
