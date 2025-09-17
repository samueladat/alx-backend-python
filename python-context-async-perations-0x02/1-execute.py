#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
Implement a class-based context manager ExecuteQuery that executes a query
and returns the results.
"""

import sqlite3


class ExecuteQuery:
    """
    A custom context manager that executes a query with parameters
    and returns the result.
    """

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and fetch results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure connection is closed safely."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print("Users older than 25:", results)
