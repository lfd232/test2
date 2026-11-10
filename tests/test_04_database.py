"""Задание 4: корректное добавление записи в БД (aiosqlite, SQLite in-memory)."""
import aiosqlite
import pytest
import pytest_asyncio

from app.async_funcs import add_user, get_user, init_db


@pytest_asyncio.fixture
async def db(event_loop):
    connection = await aiosqlite.connect(":memory:")
    await init_db(connection)
    yield connection
    await connection.close()


@pytest.mark.asyncio
async def test_add_user_inserts_new_record(event_loop, db):
    user_id = await add_user(db, "Alice", "alice@example.com")

    assert user_id == 1
    row = await get_user(db, user_id)
    assert tuple(row) == (1, "Alice", "alice@example.com")


@pytest.mark.asyncio
async def test_add_user_increases_row_count(event_loop, db):
    await add_user(db, "Alice", "alice@example.com")
    await add_user(db, "Bob", "bob@example.com")

    cursor = await db.execute("SELECT COUNT(*) FROM users")
    (count,) = await cursor.fetchone()
    assert count == 2


@pytest.mark.asyncio
async def test_add_user_duplicate_email_fails(event_loop, db):
    await add_user(db, "Alice", "alice@example.com")
    with pytest.raises(aiosqlite.IntegrityError):
        await add_user(db, "Alice2", "alice@example.com")
