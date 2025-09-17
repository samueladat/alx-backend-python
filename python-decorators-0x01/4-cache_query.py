#!/usr/bin/env python3
"""
Task 4: Using Decorators to Cache Database Queries
Create a decorator that caches the results of database queries 
to avoid redundant calls.
"""

import sqlite3
import functools

# Simple dictionary to hold cached queries
query_cache = {}


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


def cache_query(func):
    """
    Decorator to cache query results based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Executing and caching result for query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users with caching applied to avoid redundant calls.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call -> query executed and cached
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call -> cache used
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
