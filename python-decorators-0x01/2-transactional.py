#!/usr/bin/env python3
"""
Task 2: Transaction Management Decorator
Create a decorator that manages database transactions by automatically committing
or rolling back changes.
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


def transactional(func):
    """
    Decorator to wrap database operations in a transaction.
    Commits if successful, rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[TRANSACTION ERROR] Rolled back due to: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email with automatic transaction handling.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


if __name__ == "__main__":
    # Example usage
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
    print("✅ Email updated successfully (or rolled back on error)")
