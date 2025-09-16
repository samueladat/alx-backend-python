#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient.org."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org property."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and get_json is called once."""
        # Arrange: set up the mock return value
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        # Act: create client and access the org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called once with correct URL, and result matches expected
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
