from qa_api.assertions import (
    assert_saved_item,
    assert_saved_statistics,
    assert_seller_items,
    expect_status,
)
from qa_api.data import item_payload


def test_e2e_01_item_lifecycle(api, make_account, create_item):
    owner = make_account()
    payload = item_payload(owner.id)
    item_id = create_item(owner, payload)

    assert_saved_item(api, owner, item_id, payload)
    assert_seller_items(api, owner, {item_id: payload})
    for version in (1, 2):
        assert_saved_statistics(api, owner, item_id, version, payload["statistics"])
    expect_status(api.request("DELETE", f"/api/2/item/{item_id}", token=owner.token), 200)
    expect_status(api.request("GET", f"/api/1/item/{item_id}", token=owner.token), 404)
    assert_seller_items(api, owner, {})
