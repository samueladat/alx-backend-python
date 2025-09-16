#!/usr/bin/env python3
"""
Unit tests for utils module
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator"""

    def test_memoize(self):
        """a_property should call a_method only once and cache the value"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # First access triggers a_method
            self.assertEqual(obj.a_property, 42)
            # Second access should use the cached value (no extra call)
            self.assertEqual(obj.a_property, 42)

            mock_method.assert_called_once()

