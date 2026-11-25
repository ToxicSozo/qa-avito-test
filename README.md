# QA-стажировка Авито

Решение тестового задания. Осень 2026.

- **Задание 1** — дефекты по скриншотам. Приоритеты и иллюстрации. [TASK-1.md](./TASK-1.md)
- **Задание 2.1** — автотесты API пользователей, объявлений и статистики. [Тест-кейсы](./TESTCASES.md) · [Баг-репорты](./BUGS.md) · [Промпты](./PROMPTS.md)

[Официальное ТЗ](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2026/QA-trainee-assignment-autumn-2026.md) · [Postman-коллекция](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2026/postman_collection.json)

## Стек

- Python 3.10+ и pytest — запуск сценариев, фикстуры, параметризация.
- Requests — HTTP-запросы к стенду.
- pytest-html — HTML-отчёт со шагами и JSON-вложениями.
- Ruff — линтинг и форматирование.

## Структура проекта

```text
.
├── tests/
│   ├── conftest.py                 # Фикстуры и очистка объявлений
│   ├── test_auth.py                # Регистрация и авторизация
│   ├── test_access.py              # Доступ к защищённым методам
│   ├── test_create_item.py         # Создание объявления
│   ├── test_get_item.py            # Чтение по UUID
│   ├── test_get_seller_items.py    # Список объявлений продавца
│   ├── test_delete_item.py         # Удаление
│   ├── test_statistics.py          # Статистика v1 и v2
│   └── test_e2e.py                 # Жизненный цикл объявления
├── src/
│   └── qa_api/
│       ├── __init__.py
│       ├── client.py               # HTTPS-клиент
│       ├── data.py                 # Тестовые аккаунты и тела запросов
│       ├── assertions.py           # Проверки HTTP-ответов и данных
│       └── reporting.py            # Шаги и вложения для отчёта
├── task-1-images/                  # Иллюстрации к дефектам задания 1
├── TASK-1.md
├── TESTCASES.md
├── BUGS.md
├── PROMPTS.md
├── REPORT-EXAMPLE.html
├── pyproject.toml                  # Настройки pytest и Ruff
└── requirements.txt
```

### Архитектура и размещение файлов

ТЗ осени 2026 требует сдать оба задания в одном репозитории. Все файлы должны быть в корне. Здесь в корне документы, конфигурация и пример отчёта. Код и иллюстрации в каталогах — отступление от ТЗ. [Требование Авито](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2026/QA-trainee-assignment-autumn-2026.md#L179)

На отборе осенью 2025 Авито оценивало логику каталогов, имена файлов, читаемость тестов и вынос общего кода. Сценарии по операциям лежат в `tests/`. Клиент, общие проверки и отчётность — в модулях `src/qa_api/`. Разбиение упрощает поиск и правки. [Критерии структуры проекта](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2025/Solution%20and%20advice.md#L200-L206) · [Критерии реализации автотестов](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2025/Solution%20and%20advice.md#L255-L261) · [Документация pytest](https://docs.pytest.org/en/stable/explanation/goodpractices.html#choosing-a-test-layout)

Фикстуры создают аккаунты и объявления во время теста. После теста удаляют объявления даже при падении. При ошибке создания или потере ответа сверяют список этого тестового продавца. Запросы очистки, завершившиеся тайм-аутом, повторяют в конце прогона. Повторный отказ отображается в pytest. Запуск по одному и в любом порядке. [Фикстуры проекта](./tests/conftest.py) · [Подход AvitoTech к тестовым данным](https://habr.com/ru/companies/avito/articles/1047534/) · [Очистка данных в pytest](https://docs.pytest.org/en/stable/how-to/fixtures.html#safe-teardowns)

## Установка и запуск

Нужны Python 3.10+ и доступ к стенду Авито. Команды запускайте из корня. В PowerShell `python --version` должен показать версию интерпретатора. Если команда выводит только `Python`, используйте полный путь к установленному `python.exe` для создания `.venv`.

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

**Linux и macOS**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

| Переменная | Значение по умолчанию | Назначение |
| --- | --- | --- |
| `QA_API_BASE_URL` | `https://qa-internship.avito.com` | HTTPS-адрес стенда |
| `QA_API_TIMEOUT` | `15` | Тайм-аут HTTP-запросов в секундах |

### Выборочный запуск

Далее `python` — интерпретатор из `.venv`. Без активации используйте путь из блока вашей ОС.

```bash
python -m pytest --collect-only -q
python -m pytest -v tests/test_statistics.py
python -m pytest -v tests/test_e2e.py
```

## Покрытие и результаты

**68 тестов** на стенде. Покрытие включает штатные и негативные сценарии, граничные значения и смену состояния объявления. [Тест-кейсы](./TESTCASES.md)

`E2E-01` регистрирует пользователя, получает токен и создаёт объявление. Сверяет объявление по UUID и в списке продавца, читает статистику v1 и v2. После удаления проверяет `404` по UUID и пустой список. [Тест E2E](./tests/test_e2e.py)

25 ноября 2026 года на Windows 11 без VPN все 68 тестов выполнились за **25,22 с** в обратном порядке сбора pytest. **51 тест прошёл**, 17 упали по девяти описанным дефектам API. Ошибок подготовки и очистки в этом прогоне не было. Код возврата pytest — `1`. [Баг-репорты](./BUGS.md)

## HTML-отчёт

```bash
python -m pytest -v --html=report.html --self-contained-html
```

Откройте `report.html` в браузере. Разверните тест для просмотра шагов подготовки, проверки и очистки. В `Links` — JSON-вложение с HTTP-статусами, временем запросов и диагностикой. Известные падения содержат ID дефекта. [Пример отчёта](./REPORT-EXAMPLE.html)

## Линтер и форматтер

```bash
python -m ruff check .
python -m ruff format --check .
```

Правила запуска и стиля — в [pyproject.toml](./pyproject.toml).
