#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries
Run multiple database queries concurrently using asyncio.gather with aiosqlite.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40;") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """
    Run async_fetch_users and async_fetch_older_users concurrently
    and print their results.
    """
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:", users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
