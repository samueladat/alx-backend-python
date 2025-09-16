#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),             # empty dict, path "a"
        ({"a": 1}, ("a", "b")),   # "b" missing in {"a": 1}
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError with expected message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the KeyError message matches the missing key
        self.assertEqual(str(cm.exception), repr(path[-1]))


if __name__ == "__main__":
    unittest.main()
