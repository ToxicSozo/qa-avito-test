import pytest

from qa_api.assertions import (
    assert_error_reason,
    bearer_token,
    error_messages,
    expect_json,
    expect_status,
    registration_id,
)
from qa_api.client import AUTHORIZE, REGISTER
from qa_api.data import Credentials


def _assert_no_access_token(response):
    try:
        body = response.json()
    except ValueError:
        if "json" in response.headers.get("Content-Type", "").lower():
            raise AssertionError("Ответ об ошибке объявлен как JSON, но не разбирается") from None
        return
    if isinstance(body, dict) and "accessToken" in body:
        raise AssertionError("Ответ с ошибкой авторизации содержит поле accessToken")


def test_reg_01_register_returns_created_user(api):
    registration = Credentials.unique().payload()

    response = api.request("POST", REGISTER, json=registration)

    registration_id(response, registration["username"])


def test_reg_02_register_rejects_duplicate_username(api):
    registration = Credentials.unique().payload()
    expect_status(api.request("POST", REGISTER, json=registration), 201)

    response = api.request("POST", REGISTER, json=registration)

    expect_status(response, 409)


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("username", id="REG-03-missing-username"),
        pytest.param("password", id="REG-03-missing-password"),
    ],
)
def test_register_requires_credentials(api, field):
    registration = Credentials.unique().payload()
    incomplete = registration.copy()
    del incomplete[field]

    response = api.request("POST", REGISTER, json=incomplete)

    expect_status(response, 400)
    if field == "password":
        registration_id(api.request("POST", REGISTER, json=registration), registration["username"])


def test_auth_01_authorize_returns_usable_bearer(api):
    registration = Credentials.unique().payload()
    seller_id = registration_id(
        api.request("POST", REGISTER, json=registration), registration["username"]
    )

    response = api.request("POST", AUTHORIZE, json=registration)

    token = bearer_token(response)
    seller_items = api.request("GET", f"/api/1/{seller_id}/item", token=token)
    assert expect_json(seller_items, 200) == []


def test_auth_02_authorize_rejects_wrong_password(api):
    registration = Credentials.unique().payload()
    expect_status(api.request("POST", REGISTER, json=registration), 201)
    sign_in = dict(registration, password=Credentials.unique().payload()["password"])

    response = api.request("POST", AUTHORIZE, json=sign_in)

    expect_status(response, 401)
    _assert_no_access_token(response)


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("username", id="AUTH-03-missing-username"),
        pytest.param("password", id="AUTH-03-missing-password"),
    ],
)
def test_authorize_requires_credentials(api, field):
    registration = Credentials.unique().payload()
    expect_status(api.request("POST", REGISTER, json=registration), 201)
    del registration[field]

    response = api.request("POST", AUTHORIZE, json=registration)

    expect_status(response, 400)
    _assert_no_access_token(response)


def test_exp_05_duplicate_registration_keeps_original_password(api, account):
    duplicate = {
        "username": account.credentials.username,
        "password": Credentials.unique().password,
    }

    expect_status(api.request("POST", REGISTER, json=duplicate), 409)
    rejected_login = api.request("POST", AUTHORIZE, json=duplicate)
    expect_status(rejected_login, 401)
    _assert_no_access_token(rejected_login)
    token = bearer_token(api.request("POST", AUTHORIZE, json=account.credentials.payload()))
    assert expect_json(api.request("GET", f"/api/1/{account.id}/item", token=token), 200) == []


@pytest.mark.parametrize(
    "path", [pytest.param(REGISTER, id="register"), pytest.param(AUTHORIZE, id="authorize")]
)
def test_exp_12_short_password_does_not_report_invalid_json(api, path):
    credentials = Credentials.unique().payload()
    if path == AUTHORIZE:
        expect_status(api.request("POST", REGISTER, json=credentials), 201)
    credentials["password"] = "short"

    response = api.request("POST", path, json=credentials)

    if path == REGISTER and response.status_code == 201:
        # The public contract does not specify a minimum password length.
        seller_id = registration_id(response, credentials["username"])
        token = bearer_token(api.request("POST", AUTHORIZE, json=credentials))
        assert expect_json(api.request("GET", f"/api/1/{seller_id}/item", token=token), 200) == []
        return

    _assert_no_access_token(response)
    if path == AUTHORIZE and response.status_code == 401:
        if response.content.strip():
            if "json" in response.headers.get("Content-Type", "").lower():
                messages = " ".join(error_messages(response.json()))
            else:
                messages = response.text.casefold()
            terms = ("credential", "unauthoriz", "password", "парол", "учётн", "учетн", "авториз")
            explains_rejection = "invalid json body" not in messages and any(
                term in messages for term in terms
            )
            assert explains_rejection, "Ожидалась диагностика отказа во входе (BUGS.md, API-08)"
        return

    body = expect_json(response, 400, issue="API-08")
    if path == REGISTER:
        corrected = dict(credentials, password=Credentials.unique().password)
        created = api.request("POST", REGISTER, json=corrected)
        registration_id(created, corrected["username"])
    assert_error_reason(
        body,
        ("password", "парол"),
        (
            "length",
            "short",
            "minimum",
            "at least",
            "character",
            "weak",
            "invalid",
            "длин",
            "корот",
            "миним",
            "символ",
            "слаб",
            "некоррект",
            "невалид",
            "байт",
        ),
        issue="API-08",
        misleading="invalid json body",
    )


def test_auth_04_unknown_login_does_not_register_user(api):
    credentials = Credentials.unique().payload()

    rejected = api.request("POST", AUTHORIZE, json=credentials)
    expect_status(rejected, 401)
    _assert_no_access_token(rejected)
    created = api.request("POST", REGISTER, json=credentials)
    registration_id(created, credentials["username"])
