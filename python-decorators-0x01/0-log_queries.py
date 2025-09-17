#!/usr/bin/env python3
"""
Task 0: Logging Database Queries
Create a decorator to log SQL queries executed by a function with timestamp.
"""

import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """
    Decorator to log SQL queries with a timestamp before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] Executing function without explicit query")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database based on the provided query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users;")
    print(users)

