#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator
Create a decorator that automatically handles opening and closing database connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator to handle database connection automatically.
    Opens the connection, passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID from the users table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Example usage
    user = get_user_by_id(user_id=1)
    print(user)
