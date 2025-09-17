#!/usr/bin/env python3
"""
Task 4: Parameterize and patch as decorators
Unit tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org"""

    @patch("client.get_json")  # patch where it's looked up (no real HTTP)
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, mock_get_json, org_name):
        """
        Ensure:
        - .org returns the mocked payload
        - get_json called exactly once with the expected URL
        - No external network calls occur (because get_json is patched)
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)

        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )

        # Optional: accessing again uses memoized value (still no extra calls)
        _ = client.org
        mock_get_json.assert_called_once()  # still one call


if __name__ == "__main__":
    unittest.main()
