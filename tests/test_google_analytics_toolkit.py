import unittest
import os
from unittest.mock import patch
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from google_analytics_report_tool import GoogleAnalyticsReportTool
from google_analytics_toolkit import GoogleAnalyticsToolkit
from superagi.types.key_type import ToolConfigKeyType


class TestGoogleAnalyticsToolkit(unittest.TestCase):

    def setUp(self):
        self.toolKit = GoogleAnalyticsToolkit()

    def test_name(self):
        self.assertEqual(self.toolKit.name, "Google Analytics Toolkit")

    def test_description(self):
        self.assertEqual(self.toolKit.description,
                         "Google Analytics Toolkit returns google analytics reports requested by the user")

    def test_get_tools(self):
        self.assertIsInstance(self.toolKit.get_tools()[0], GoogleAnalyticsReportTool)

    def test_get_env_keys(self):
        env_keys = self.toolKit.get_env_keys()
        self.assertIsInstance(env_keys[0], ToolConfiguration)
        self.assertEqual(env_keys[0].key, "PROPERTY_ID")
        self.assertEqual(env_keys[0].key_type, ToolConfigKeyType.STRING)
        self.assertEqual(env_keys[0].is_required, True)
        self.assertEqual(env_keys[0].is_secret, True)
        self.assertIsInstance(env_keys[1], ToolConfiguration)
        self.assertEqual(env_keys[1].key, "GOOGLE_CREDENTIALS_FILE")
        self.assertEqual(env_keys[1].key_type, ToolConfigKeyType.FILE)
        self.assertEqual(env_keys[1].is_required, True)
        self.assertEqual(env_keys[1].is_secret, False)

if __name__ == '__main__':
    unittest.main()