"""Задание 1: Future разрешается с ожидаемым значением."""
import pytest

from app.async_funcs import get_future_with_value


@pytest.mark.asyncio
async def test_future_resolves_with_expected_value(event_loop):
    future = get_future_with_value(42)
    result = await future
    assert result == 42
    assert future.done()
    assert future.exception() is None


@pytest.mark.asyncio
async def test_future_resolves_with_string(event_loop):
    assert await get_future_with_value("hello") == "hello"
