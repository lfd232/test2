import asyncio

import pytest


@pytest.fixture
def event_loop():
    """Фикстура event_loop: создаёт новый цикл событий для каждого теста."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
