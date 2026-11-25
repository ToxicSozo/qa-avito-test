import pytest

from qa_api.assertions import assert_saved_item, assert_seller_items, expect_status
from qa_api.data import item_payload


@pytest.mark.parametrize(
    "path",
    [
        pytest.param("/api/1/item/{item_id}", id="ACCESS-01-get-item"),
        pytest.param("/api/1/{seller_id}/item", id="ACCESS-01-list-seller"),
        pytest.param("/api/1/statistic/{item_id}", id="ACCESS-01-stats-v1"),
        pytest.param("/api/2/statistic/{item_id}", id="ACCESS-01-stats-v2"),
    ],
)
def test_read_requires_bearer(api, account, create_item, path):
    item_id = create_item(account) if "{item_id}" in path else None
    response = api.request("GET", path.format(item_id=item_id, seller_id=account.id))
    expect_status(response, 401)


def test_access_01_create_requires_bearer(api, account, post_item):
    assert_seller_items(api, account, {})
    response = post_item(account, item_payload(account.id), authenticated=False)

    expect_status(response, 401)
    assert_seller_items(api, account, {})


def test_access_01_delete_requires_bearer(api, account, create_item):
    payload = item_payload(account.id)
    item_id = create_item(account, payload)
    assert_saved_item(api, account, item_id, payload)

    response = api.request("DELETE", f"/api/2/item/{item_id}")

    expect_status(response, 401)
    assert_saved_item(api, account, item_id, payload)
    assert_seller_items(api, account, {item_id: payload})
