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

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Verify that:
        - GithubOrgClient.org returns the value from get_json
        - get_json is called exactly once with the expected URL
        - No external HTTP call is made (thanks to patch)
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        # org is a @memoize-wrapped property, so call without parentheses
        self.assertEqual(client.org, expected_payload)

        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )


if __name__ == "__main__":
    unittest.main()
