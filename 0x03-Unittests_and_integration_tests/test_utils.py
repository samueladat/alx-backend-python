#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Return value matches expected."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected,
        )

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """requests.get is patched; json() returns payload."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        with patch("utils.requests.get", return_value=mock_resp) as mget:
            result = get_json(test_url)
            mget.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self):
        """a_method is called once; value cached."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as m:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            m.assert_called_once()


if __name__ == "__main__":
    unittest.main()
