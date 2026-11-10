"""Задание 5: async-функция в отдельном потоке возвращает корректный результат."""
import threading

import pytest

from app.async_funcs import multiply_async, run_in_thread


@pytest.mark.asyncio
async def test_run_in_thread_returns_result(event_loop):
    result = await run_in_thread(multiply_async, 6, 7)
    assert result == 42


@pytest.mark.asyncio
async def test_run_in_thread_uses_other_thread(event_loop):
    import asyncio

    main_thread = threading.get_ident()
    seen = {}

    async def whoami():
        seen["thread"] = threading.get_ident()
        await asyncio.sleep(0)
        return "ok"

    assert await run_in_thread(whoami) == "ok"
    assert seen["thread"] != main_thread
