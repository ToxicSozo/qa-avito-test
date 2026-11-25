import re
from typing import Any
from uuid import UUID

import requests

UUID_IN_STATUS = re.compile(r"\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b", re.IGNORECASE)


def request_label(response: requests.Response) -> str:
    return f"{response.request.method} {response.request.path_url}"


def expect_status(response: requests.Response, status: int, *, issue: str = "") -> None:
    reference = f" (BUGS.md, {issue})" if issue else ""
    assert response.status_code == status, (
        f"{request_label(response)}: expected HTTP {status}, got HTTP {response.status_code}"
        f"{reference}"
    )


def expect_json(response: requests.Response, status: int, *, issue: str = "") -> Any:
    expect_status(response, status, issue=issue)
    media_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    assert media_type == "application/json", (
        f"{request_label(response)}: expected JSON, got {media_type or 'no Content-Type'}"
    )
    try:
        return response.json()
    except ValueError:
        raise AssertionError(f"{request_label(response)}: malformed JSON response") from None


def assert_error_codes(response, allowed_statuses, *, issue):
    http_status = response.status_code
    assert http_status in allowed_statuses, (
        f"{request_label(response)}: HTTP {http_status}, ожидался {allowed_statuses}"
        f" (BUGS.md, {issue})"
    )
    media_type = response.headers.get("Content-Type", "").partition(";")[0].strip().lower()
    if media_type == "application/json" or media_type.endswith("+json"):
        try:
            body = response.json()
        except ValueError:
            raise AssertionError(f"Некорректный JSON в ответе (BUGS.md, {issue})") from None
        if isinstance(body, dict):
            for field in ("status", "code"):
                value = str(body.get(field, "")).strip()
                if value.isascii() and value.isdecimal():
                    assert int(value) == http_status, (
                        f"HTTP {http_status} и поле {field} расходятся (BUGS.md, {issue})"
                    )


def item_id_from_creation(response: requests.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        data = None
    status = data.get("status") if isinstance(data, dict) else None
    item_ids = UUID_IN_STATUS.findall(status) if isinstance(status, str) else []
    if len(item_ids) != 1:
        raise AssertionError(
            f"{request_label(response)}: expected one created item UUID in the status field"
        )
    return str(UUID(item_ids[0]))


def registration_id(response, username):
    user = expect_json(response, 201)
    if not isinstance(user, dict) or "password" in user:
        raise AssertionError("Регистрация должна вернуть JSON-объект без поля password")
    assert user.get("username") == username, "Регистрация должна вернуть имя пользователя"
    user_id = user.get("id")
    assert type(user_id) is int and user_id > 0, "Ожидался положительный числовой id"
    return user_id


def bearer_token(response):
    body = expect_json(response, 200)
    if not isinstance(body, dict):
        raise AssertionError("В ответе авторизации ожидается JSON-объект")
    token = body.get("accessToken")
    if not isinstance(token, str) or not token.strip() or body.get("tokenType") != "Bearer":
        raise AssertionError("Авторизация должна вернуть непустой accessToken и tokenType Bearer")
    return token


def only_record(records):
    assert isinstance(records, list), "В ответе ожидается JSON-массив"
    assert len(records) == 1, "В ответе ожидается ровно одна запись"
    return records[0]


def error_messages(body):
    if not isinstance(body, dict):
        raise AssertionError("В ответе об ошибке ожидается JSON-объект")
    messages = []
    for details in (body, body.get("error"), body.get("result")):
        if isinstance(details, dict):
            messages.extend(details.get(key) for key in ("field", "error", "message", "status"))
    return {message.strip().casefold() for message in messages if isinstance(message, str)}


def assert_error_reason(body, subjects, reasons, *, issue, misleading=""):
    messages = " ".join(error_messages(body))
    identifies_problem = (
        any(word in messages for word in subjects)
        and any(word in messages for word in reasons)
        and (not misleading or misleading not in messages)
    )
    assert identifies_problem, f"Ожидалось объяснение ошибки в данных (BUGS.md, {issue})"


def _assert_counters(actual, expected):
    assert isinstance(actual, dict), "Статистика должна быть JSON-объектом"
    for field, expected_value in expected.items():
        value = actual.get(field)
        assert type(value) is int, f"Счётчик {field} должен быть целым числом"
        assert value == expected_value, f"Счётчик {field} изменился после сохранения"


def assert_item(actual, item_id, payload):
    assert isinstance(actual, dict), "Объявление должно быть JSON-объектом"
    assert actual.get("id") == item_id
    assert actual.get("name") == payload["name"]
    assert type(actual.get("price")) is int
    assert actual.get("price") == payload["price"]
    assert type(actual.get("sellerId")) is int
    assert actual.get("sellerId") == payload["sellerID"]
    _assert_counters(actual.get("statistics"), payload["statistics"])


def assert_seller_items(api, owner, expected):
    response = api.request("GET", f"/api/1/{owner.id}/item", token=owner.token)
    records = expect_json(response, 200)
    assert isinstance(records, list), "В списке продавца ожидается JSON-массив"
    assert len(records) == len(expected), "Количество объявлений продавца изменилось"
    seen = set()
    for record in records:
        assert isinstance(record, dict), "Объявление должно быть JSON-объектом"
        item_id = record.get("id")
        assert isinstance(item_id, str) and item_id in expected, "В списке найден лишний UUID"
        assert_item(record, item_id, expected[item_id])
        seen.add(item_id)
    assert seen == expected.keys(), "В списке должны быть все ожидаемые UUID"


def assert_saved_item(api, owner, item_id, payload):
    response = api.request("GET", f"/api/1/item/{item_id}", token=owner.token)
    assert_item(only_record(expect_json(response, 200)), item_id, payload)


def assert_saved_statistics(api, owner, item_id, version, counters):
    response = api.request("GET", f"/api/{version}/statistic/{item_id}", token=owner.token)
    _assert_counters(only_record(expect_json(response, 200)), counters)
