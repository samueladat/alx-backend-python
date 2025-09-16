#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient.org."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """org returns the mocked payload and calls get_json once with the URL."""
        payload = {"login": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)

        # Support both implementations: property or method.
        org_attr = client.org
        result = org_attr() if callable(org_attr) else org_attr

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()



