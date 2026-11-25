import logging
import math
import os
from collections.abc import Callable, Iterator
from typing import Any
from uuid import UUID

import pytest
import requests

from qa_api.assertions import bearer_token, expect_json, item_id_from_creation, registration_id
from qa_api.client import (
    AUTHORIZE,
    DEFAULT_BASE_URL,
    ITEMS,
    REGISTER,
    ApiClient,
    ApiTimeoutError,
    ApiTransportError,
    https_base_url,
)
from qa_api.data import Account, Credentials, item_payload

pytest_plugins = ("qa_api.reporting",)


@pytest.fixture(scope="session")
def api_settings() -> tuple[str, float]:
    try:
        base_url = https_base_url(os.environ.get("QA_API_BASE_URL", DEFAULT_BASE_URL))
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from None

    try:
        timeout = float(os.environ.get("QA_API_TIMEOUT", "15"))
    except ValueError:
        raise pytest.UsageError("QA_API_TIMEOUT must be a positive number of seconds") from None
    if not math.isfinite(timeout) or timeout <= 0:
        raise pytest.UsageError("QA_API_TIMEOUT must be a positive number of seconds")
    return base_url, timeout


@pytest.fixture
def api(
    api_settings: tuple[str, float],
    attach_http_trace: Callable[[requests.Session], None],
) -> Iterator[ApiClient]:
    with requests.Session() as session:
        session.trust_env = False
        attach_http_trace(session)
        yield ApiClient(session, *api_settings)


@pytest.fixture
def make_account(api: ApiClient) -> Callable[[], Account]:
    def make() -> Account:
        credentials = Credentials.unique()
        registered = api.request("POST", REGISTER, json=credentials.payload())
        seller_id = registration_id(registered, credentials.username)
        token = bearer_token(api.request("POST", AUTHORIZE, json=credentials.payload()))
        return Account(seller_id, credentials, token)

    return make


@pytest.fixture
def account(make_account: Callable[[], Account]) -> Account:
    return make_account()


def _clean_test_items(client, owners_to_check, created_items):
    errors = []
    timeouts = []
    # Only inspect lists of accounts registered by this test.
    for owner in tuple(owners_to_check.values()):
        path = f"/api/1/{owner.id}/item"
        try:
            records = expect_json(client.request("GET", path, token=owner.token), 200)
        except ApiTimeoutError as exc:
            timeouts.append(str(exc))
            continue
        except (AssertionError, ApiTransportError) as exc:
            errors.append(str(exc))
            continue
        del owners_to_check[owner.id]
        if not isinstance(records, list):
            errors.append(f"GET {path}: expected an item list during cleanup")
            continue
        for record in records:
            seller_id = record.get("sellerId") if isinstance(record, dict) else None
            if type(seller_id) is not int or seller_id != owner.id:
                errors.append(f"GET {path}: unexpected seller record during cleanup")
                continue
            try:
                raw_id = record.get("id")
                if not isinstance(raw_id, str):
                    raise ValueError
                item_id = str(UUID(raw_id))
            except ValueError:
                errors.append(f"GET {path}: expected an item UUID for cleanup")
                continue
            created_items[owner.id, item_id] = owner.token

    for key, token in reversed(tuple(created_items.items())):
        path = f"/api/2/item/{key[1]}"
        try:
            response = client.request("DELETE", path, token=token)
        except ApiTimeoutError as exc:
            timeouts.append(str(exc))
            continue
        except ApiTransportError as exc:
            errors.append(str(exc))
            continue
        if response.status_code in {200, 404}:
            del created_items[key]
        else:
            errors.append(f"DELETE {path}: expected HTTP 200 or 404, got {response.status_code}")
    return errors, timeouts


@pytest.fixture(scope="session")
def deferred_cleanup(api_settings):
    pending = []
    yield pending
    if pending:
        errors = []
        with requests.Session() as session:
            session.trust_env = False
            client = ApiClient(session, *api_settings)
            for clean in pending:
                failed, timed_out = clean(client)
                errors.extend(failed + timed_out)
        if errors:
            pytest.fail("Final item cleanup failed\n" + "\n".join(errors), pytrace=False)


@pytest.fixture
def post_item(api: ApiClient, deferred_cleanup) -> Iterator[Callable[..., requests.Response]]:
    created_items: dict[tuple[int, str], str] = {}
    owners_to_check: dict[int, Account] = {}

    def post(
        owner: Account,
        payload: dict[str, Any],
        *,
        authenticated: bool = True,
    ) -> requests.Response:
        try:
            token = owner.token if authenticated else None
            response = api.request("POST", ITEMS, token=token, json=payload)
        except ApiTransportError:
            owners_to_check[owner.id] = owner
            raise

        # Even an error response may have committed a write. Reconcile only this test's seller.
        if 200 <= response.status_code < 300:
            try:
                item_id = item_id_from_creation(response)
            except AssertionError:
                owners_to_check[owner.id] = owner
            else:
                created_items[owner.id, item_id] = owner.token
        else:
            owners_to_check[owner.id] = owner
        return response

    yield post

    def clean(client):
        return _clean_test_items(client, owners_to_check, created_items)

    errors, timeouts = clean(api)
    if timeouts:
        logging.getLogger(__name__).warning(
            "Cleanup deferred after timeout: %s", "; ".join(timeouts)
        )
        deferred_cleanup.append(clean)
    if errors:
        pytest.fail("Item cleanup failed\n" + "\n".join(errors), pytrace=False)


@pytest.fixture
def create_item(
    post_item: Callable[..., requests.Response],
) -> Callable[..., str]:
    def create(owner: Account, payload: dict[str, Any] | None = None) -> str:
        if payload is None:
            payload = item_payload(owner.id)
        response = post_item(owner, payload)
        expect_json(response, 200)
        return item_id_from_creation(response)

    return create
