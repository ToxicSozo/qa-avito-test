import json
import re
from collections.abc import Callable
from functools import partial
from html import escape
from typing import Any

import pytest
import pytest_html
import requests

from qa_api.client import ITEMS

HTTP_EXCHANGES = pytest.StashKey[list[dict[str, Any]]]()
REPORT_PHASES = pytest.StashKey[list[dict[str, Any]]]()
PHASE_NAMES = {"setup": "Подготовка", "call": "Проверка", "teardown": "Очистка"}
RESULT_NAMES = {"passed": "пройдено", "failed": "ошибка", "skipped": "пропущено"}
COUNTERS = ("likes", "viewCount", "contacts")
SAFE_ERROR_MESSAGES = {
    "invalid JSON body",
    "invalid username or password",
    "не передано тело объявления",
    "передан некорректный идентификатор объявления",
    "route /api/1/item/ not found",
    *(f"поле {field} обязательно" for field in ("price", *COUNTERS)),
}


def _selected_numbers(data: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    values = {}
    for key in fields:
        if key in data:
            value = data[key]
            values[key] = value if type(value) is int else {"type": type(value).__name__}
    return values


def _selected_item_values(data: dict[str, Any]) -> dict[str, Any]:
    values = _selected_numbers(data, ("sellerID", "sellerId", "price", *COUNTERS))
    if "statistics" in data:
        statistics = data["statistics"]
        values["statistics"] = (
            _selected_numbers(statistics, COUNTERS)
            if isinstance(statistics, dict)
            else {"type": type(statistics).__name__}
        )
    return values


def _response_diagnostics(response: requests.Response, media_type: str) -> dict[str, Any]:
    if media_type != "application/json":
        return {}
    try:
        body = response.json()
    except ValueError:
        return {"invalid_json": True}
    if isinstance(body, list):
        return {
            "record_count": len(body),
            "records": [
                _selected_item_values(record) for record in body[:3] if isinstance(record, dict)
            ],
        }
    if response.status_code < 400 or not isinstance(body, dict):
        return {}

    diagnostics: dict[str, Any] = {}
    for key in ("code", "status"):
        value = str(body.get(key))
        if re.fullmatch(r"[1-5][0-9]{2}", value):
            diagnostics[f"json_{key}"] = int(value)
    messages = [body.get("message"), body.get("error"), body.get("status")]
    result = body.get("result")
    if isinstance(result, dict):
        messages.append(result.get("message"))
    diagnostics["messages"] = list(
        dict.fromkeys(
            message
            for message in messages
            if isinstance(message, str) and message in SAFE_ERROR_MESSAGES
        )
    )
    return diagnostics


def _capture_http_exchanges(session: requests.Session, item: pytest.Item) -> None:
    if not item.config.getoption("htmlpath", default=None):
        return
    exchanges = item.stash.setdefault(HTTP_EXCHANGES, [])

    def capture(response: requests.Response, **_kwargs: Any) -> None:
        request = response.request
        path = request.path_url.partition("?")[0]
        media_type = response.headers.get("Content-Type", "").partition(";")[0].strip().lower()
        exchange = {
            "method": request.method,
            "path": path,
            "http_status": response.status_code,
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000),
            "json_response": media_type == "application/json",
            "response_diagnostics": _response_diagnostics(response, media_type),
        }
        if request.method == "POST" and path.endswith(ITEMS) and request.body:
            try:
                payload = json.loads(request.body)
            except (TypeError, ValueError):
                payload = None
            if isinstance(payload, dict):
                exchange["item_input"] = _selected_item_values(payload)
        exchanges.append(exchange)

    session.hooks["response"].append(capture)


@pytest.fixture
def attach_http_trace(request: pytest.FixtureRequest) -> Callable[[requests.Session], None]:
    return partial(_capture_http_exchanges, item=request.node)


def _render_steps(phases: list[dict[str, Any]]) -> str:
    sections = []
    for phase in phases:
        title = escape(PHASE_NAMES[phase["phase"]])
        result = escape(RESULT_NAMES.get(phase["result"], phase["result"]))
        requests_list = "".join(
            f"<li><code>{escape(step['method'])} {escape(step['path'])}</code>"
            f" → HTTP {step['http_status']} ({step['elapsed_ms']} мс)</li>"
            for step in phase["http"]
        )
        details = f"<ul>{requests_list}</ul>" if requests_list else ""
        sections.append(f"<li><strong>{title}</strong> — {result}{details}</li>")
    return (
        '<section class="api-steps"><h4>Шаги сценария</h4><ol>'
        + "".join(sections)
        + "</ol></section>"
    )


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    report = yield
    if not item.config.getoption("htmlpath", default=None):
        return report

    exchanges = item.stash.get(HTTP_EXCHANGES, [])
    phases = item.stash.setdefault(REPORT_PHASES, [])
    phase = {"phase": report.when, "result": report.outcome, "http": exchanges.copy()}
    exchanges.clear()
    issue = re.search(r"BUGS\.md, (API-[0-9]{2})", report.longreprtext)
    if issue:
        phase["bug_report"] = issue[1]
    phases.append(phase)

    if report.when == "teardown":
        report.extras = [
            *getattr(report, "extras", []),
            pytest_html.extras.html(_render_steps(phases)),
            pytest_html.extras.json(
                {"test": report.nodeid, "phases": phases}, name="Диагностика JSON"
            ),
        ]
    return report


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(cells: list[str]) -> None:
    for index, cell in enumerate(cells):
        if cell.startswith('<td class="col-links">'):
            cells[index] = cell.replace(
                '<a target="_blank" href="data:application/json;',
                '<a download="api-diagnostics.json" href="data:application/json;',
            )
