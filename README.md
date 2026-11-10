# Асинхронные тесты (pytest + asyncio)

## Установка и запуск
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

## Структура
- `app/async_funcs.py` — тестируемые функции
- `tests/conftest.py` — фикстура `event_loop`
- `tests/test_01_future_resolves.py` — Future разрешается значением
- `tests/test_02_future_rejects.py` — Future отклоняется исключением
- `tests/test_03_http_request.py` — HTTP-запрос через aiohttp (локальный тестовый сервер)
- `tests/test_04_database.py` — добавление записи в БД (aiosqlite)
- `tests/test_05_thread.py` — async-функция в отдельном потоке

Версия `pytest-asyncio` ограничена `<1.0`, т.к. в 1.0 фикстура `event_loop` удалена
(здесь она определена вручную в `conftest.py`, как требует задание).
