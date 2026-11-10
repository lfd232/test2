"""Задание 2: Future отклоняется с ожидаемым исключением."""
import pytest

from app.async_funcs import get_future_with_error


@pytest.mark.asyncio
async def test_future_rejects_with_expected_exception(event_loop):
    future = get_future_with_error(ValueError("что-то пошло не так"))
    with pytest.raises(ValueError, match="что-то пошло не так"):
        await future
    assert isinstance(future.exception(), ValueError)


@pytest.mark.asyncio
async def test_future_rejects_with_custom_exception_type(event_loop):
    with pytest.raises(KeyError):
        await get_future_with_error(KeyError("k"))
