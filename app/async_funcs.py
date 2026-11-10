"""Тестируемые асинхронные функции для всех 5 заданий."""
import asyncio
from typing import Any, Awaitable, Callable

import aiohttp
import aiosqlite


# ---------- Задания 1 и 2: promise (future) ----------
def get_future_with_value(value: Any, delay: float = 0.01) -> "asyncio.Future":
    """Возвращает Future (аналог promise), который разрешается значением value."""
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_later(delay, future.set_result, value)
    return future


def get_future_with_error(exc: Exception, delay: float = 0.01) -> "asyncio.Future":
    """Возвращает Future, который отклоняется (reject) исключением exc."""
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_later(delay, future.set_exception, exc)
    return future


# ---------- Задание 3: HTTP-запрос ----------
async def fetch_json(url: str) -> dict:
    """Выполняет GET-запрос и возвращает JSON-ответ."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


# ---------- Задание 4: база данных ----------
async def init_db(db: aiosqlite.Connection) -> None:
    await db.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "email TEXT NOT NULL UNIQUE)"
    )
    await db.commit()


async def add_user(db: aiosqlite.Connection, name: str, email: str) -> int:
    """Добавляет пользователя и возвращает его id."""
    cursor = await db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
    )
    await db.commit()
    return cursor.lastrowid


async def get_user(db: aiosqlite.Connection, user_id: int):
    cursor = await db.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    )
    return await cursor.fetchone()


# ---------- Задание 5: async-функция в отдельном потоке ----------
async def multiply_async(a: int, b: int) -> int:
    await asyncio.sleep(0.01)
    return a * b


async def run_in_thread(
    coro_func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
) -> Any:
    """Запускает async-функцию в отдельном потоке (со своим циклом событий)
    и ждёт результат, не блокируя текущий цикл."""
    return await asyncio.to_thread(
        lambda: asyncio.run(coro_func(*args, **kwargs))
    )
