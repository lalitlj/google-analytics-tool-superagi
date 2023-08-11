import unittest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from superagi.tools.google_analytics_report_tool import GoogleAnalyticsReportTool, GoogleAnalyticsReportToolInput
from google.analytics.data_v1beta.types import RunReportRequest, DateRange


class TestAnalyticsReportTool(unittest.TestCase):

    def setUp(self):
        self.tool = GoogleAnalyticsReportTool()

    @patch.object(GoogleAnalyticsReportTool, 'get_dimensions_and_metrics')
    @patch.object(GoogleAnalyticsReportTool, '_execute')
    def test_google_analytics_report_tool(self, mock_execute, mock_get_dim_metrics):
        mock_get_dim_metrics.return_value = [['dim1', 'dim2'], ['met1', 'met2']]
        mock_execute.return_value = 'Success!'
        self.tool.run('some_property_id', 'some_google_cred')

    @patch.object(GoogleAnalyticsReportTool, '_execute')
    def test_wrong_input_type(self, mock_execute):
        with self.assertRaises(ValidationError):
            self.tool.run(222, 'cred')  # start_date_of_query should be string

    @patch.object(GoogleAnalyticsReportTool, '_execute')
    def test_missing_required_fields(self, mock_execute):
        with self.assertRaises(ValidationError):
            self.tool.run()  # missing start_date_of_query and end_date_of_query

    @patch('os.remove')
    @patch.object(BetaAnalyticsDataClient, 'run_report')
    @patch.object(GoogleAnalyticsReportTool, '_set_google_credentials')
    @patch.object(GoogleAnalyticsReportTool, 'get_dimensions_and_metrics')
    @patch.object(GoogleAnalyticsReportTool, 'get_tool_config')
    def test_run_report_request(self, mock_tool_config, mock_get_dim_metrics, mock_set_google_cred, mock_run_report,
                                mock_os):
        mock_tool_config.return_value = 123456
        mock_get_dim_metrics.return_value = [['dim1', 'dim2'], ['met1', 'met2']]
        mock_run_report.return_value = MagicMock()
        self.tool.run('2019-03-03', '2021-03-03', True)

    def test_create_run_report_request(self):
        dimensions = ['page_path', 'something_else']
        metrics = ['users', 'newUsers']
        property_id = '123456'
        start_date_of_query = '2020-11-15'
        end_date_of_query = '2021-11-15'
        request = self.tool._create_run_report_request(
            property_id,
            dimensions,
            metrics,
            start_date_of_query,
            end_date_of_query)
        self.assertIsInstance(request, RunReportRequest)
        self.assertIsInstance(request.date_ranges[0], DateRange)
        self.assertEqual(request.date_ranges[0].start_date, start_date_of_query)
        self.assertEqual(request.date_ranges[0].end_date, end_date_of_query)


if __name__ == "__main__":
    unittest.main()