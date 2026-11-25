from uuid import uuid4

import pytest

from qa_api.assertions import assert_error_codes, assert_saved_statistics, expect_status
from qa_api.data import item_payload


@pytest.mark.parametrize(
    "version", [pytest.param(1, id="STAT-01-v1"), pytest.param(2, id="STAT-01-v2")]
)
def test_get_item_statistics(api, account, create_item, version):
    payload = item_payload(account.id)
    item_id = create_item(account, payload)

    assert_saved_statistics(api, account, item_id, version, payload["statistics"])


@pytest.mark.parametrize(
    "version", [pytest.param(1, id="STAT-02-v1"), pytest.param(2, id="STAT-02-v2")]
)
def test_statistics_preserve_first_count(api, account, create_item, version):
    counters = {"likes": 1, "viewCount": 1, "contacts": 1}
    item_id = create_item(account, item_payload(account.id, statistics=counters))

    assert_saved_statistics(api, account, item_id, version, counters)


@pytest.mark.parametrize(
    "version", [pytest.param(1, id="STAT-03-v1"), pytest.param(2, id="STAT-03-v2")]
)
def test_get_missing_statistics_returns_404(api, account, version):
    response = api.request("GET", f"/api/{version}/statistic/{uuid4()}", token=account.token)

    expect_status(response, 404)


@pytest.mark.parametrize(
    "version", [pytest.param(1, id="STAT-04-v1"), pytest.param(2, id="STAT-04-v2")]
)
def test_deleted_item_statistics_returns_404(api, account, create_item, version):
    payload = item_payload(account.id)
    item_id = create_item(account, payload)
    assert_saved_statistics(api, account, item_id, version, payload["statistics"])
    expect_status(api.request("DELETE", f"/api/2/item/{item_id}", token=account.token), 200)
    expect_status(api.request("GET", f"/api/1/item/{item_id}", token=account.token), 404)

    response = api.request("GET", f"/api/{version}/statistic/{item_id}", token=account.token)

    expect_status(response, 404, issue="API-02")


def test_exp_03_statistics_v2_error_status_is_consistent(api, account):
    response = api.request("GET", "/api/2/statistic/not-a-uuid", token=account.token)

    assert_error_codes(response, (400, 404), issue="API-05")


def test_exp_10_statistics_stay_with_their_own_item(api, account, create_item):
    first_counters = {"likes": 1, "viewCount": 22, "contacts": 333}
    second_counters = {"likes": 44, "viewCount": 555, "contacts": 6}
    first_id = create_item(account, item_payload(account.id, statistics=first_counters))
    second_id = create_item(account, item_payload(account.id, statistics=second_counters))
    for version in (1, 2):
        assert_saved_statistics(api, account, first_id, version, first_counters)
        assert_saved_statistics(api, account, second_id, version, second_counters)

    deleted = api.request("DELETE", f"/api/2/item/{first_id}", token=account.token)

    expect_status(deleted, 200)
    for version in (1, 2):
        assert_saved_statistics(api, account, second_id, version, second_counters)
