#!/usr/bin/env python3
"""
Task 0: Custom Class-Based Context Manager for Database Connection
"""

import sqlite3


class DatabaseConnection:
    """
    A custom context manager to handle opening and closing SQLite database connections.
    Ensures connections are properly closed, even if errors occur.
    """

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return the connection object."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure proper cleanup:
        - Commit if no exception occurred.
        - Rollback if an exception occurred.
        - Always close the connection.
        """
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        print("Users:", results)
