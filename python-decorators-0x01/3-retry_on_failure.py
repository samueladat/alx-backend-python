#!/usr/bin/env python3
"""
Task 3: Using Decorators to Retry Database Queries
Create a decorator that retries database operations if they fail due to transient errors.
"""

import time
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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it raises an exception.
    Retries up to 'retries' times, waiting 'delay' seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[RETRY {attempt}/{retries}] Failed with error: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            print("[RETRY] All attempts failed. Raising last exception.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users with retry logic applied in case of transient errors.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"❌ Operation failed after retries: {e}")
