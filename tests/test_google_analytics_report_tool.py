import unittest
from unittest.mock import patch, MagicMock
from google_analytics_report_tool import GoogleAnalyticsReportTool


class TestGoogleAnalyticsReportTool(unittest.TestCase):

    def setUp(self):
        self.tool = GoogleAnalyticsReportTool()
        self.tool.resource_manager = MagicMock()

    @patch('google_analytics_report_tool.BetaAnalyticsDataClient')
    def test_execute(self, mock_client):
        mock_run_report = MagicMock()
        mock_client.return_value.run_report.return_value = mock_run_report
        resp = self.tool._execute('2000-01-01', '2000-01-01', False)
        self.assertIn("Successfully wrote", resp)

    @patch('google_analytics_report_tool.json')
    @patch('google_analytics_report_tool.os')
    def test_set_google_credentials(self, mock_os, mock_json):
        self.tool._set_google_credentials('dummy_cred')
        mock_json.loads.assert_called_with('dummy_cred')
        mock_os.environ.__setitem__.assert_called_with('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')

    def test_generate_filename(self):
        filenames = ['dummymetric.txt']
        filename = self.tool._generate_filename(['dummy'], ['metric'], filenames)
        self.assertEqual(filename, 'dummyNewmetric.txt')

    def test_create_run_report_request(self):
        def_dimension = 'dummy_dimension'
        def_metric = 'dummy_metric'
        request = self.tool._create_run_report_request(1, [def_dimension], [def_metric], '2000-01-01', '2000-01-01')
        self.assertEqual(request.dimensions[0].name, def_dimension)
        self.assertEqual(request.metrics[0].name, def_metric)

    @patch('google_analytics_report_tool.yaml')
    def test_get_dimensions_and_metrics(self, mock_yaml):
        def_side_effect(filename, Loader):
        return {"GOOGLE_ANALYTICS_VARIABLES": [{'Dimension': 'dummyDimension', 'Metric': 'dummyMetric'}]}

    mock_yaml.load.side_effect = def_side_effect
    dimensions_and_metrics = self.tool.get_dimensions_and_metrics()
    self.assertEqual(dimensions_and_metrics, [['dummyDimension', 'dummyMetric']])


if __name__ == "__main__":
    unittest.main()
