from qa_api.assertions import assert_saved_item, assert_seller_items, expect_status
from qa_api.data import item_payload


def test_item_04_get_seller_items_is_scoped(api, account, make_account, create_item):
    other = make_account()
    assert account.id != other.id

    first = item_payload(account.id)
    second = item_payload(account.id)
    other_item = dict(first, sellerID=other.id)
    first_id = create_item(account, first)
    other_id = create_item(other, other_item)
    second_id = create_item(account, second)

    assert len({first_id, other_id, second_id}) == 3
    assert_saved_item(api, account, first_id, first)
    assert_saved_item(api, other, other_id, other_item)
    assert_seller_items(api, account, {first_id: first, second_id: second})
    assert_seller_items(api, other, {other_id: other_item})


def test_item_05_get_seller_items_is_empty(api, account):
    assert_seller_items(api, account, {})


def test_item_12_list_rejects_invalid_seller_id(api, account):
    response = api.request("GET", "/api/1/not-a-number/item", token=account.token)
    expect_status(response, 400)
