"""Задание 3: HTTP-запрос к API через aiohttp.

Вместо реального внешнего API поднимается локальный aiohttp-сервер
(в том же цикле событий), поэтому тест стабилен и не требует интернета.
"""
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.test_utils import TestServer

from app.async_funcs import fetch_json


async def handle_users(request):
    return web.json_response({"id": 1, "name": "Alice"})


async def handle_error(request):
    return web.json_response({"error": "boom"}, status=500)


@pytest_asyncio.fixture
async def server(event_loop):
    app = web.Application()
    app.router.add_get("/users/1", handle_users)
    app.router.add_get("/error", handle_error)
    srv = TestServer(app, loop=event_loop)
    await srv.start_server()
    yield srv
    await srv.close()


@pytest.mark.asyncio
async def test_fetch_json_returns_correct_response(event_loop, server):
    data = await fetch_json(str(server.make_url("/users/1")))
    assert data == {"id": 1, "name": "Alice"}


@pytest.mark.asyncio
async def test_fetch_json_raises_on_http_error(event_loop, server):
    with pytest.raises(ClientResponseError) as exc_info:
        await fetch_json(str(server.make_url("/error")))
    assert exc_info.value.status == 500
