import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import date
from getMetricDimensions import getMetric, getDim
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

class UserReportInput(BaseModel):
    met: str = Field(..., description="The metric the user wants to know, for example number of active users")
    dim: str = Field(..., description="The context or dimension for which the user wants to know, for example, a city")
    start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end: str = Field(..., description=f"The last date of the query, in YYYY-MM-DD format, if today, return today's date")


class reportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Analytics Report Tool"
    args_schema: Type[BaseModel] = UserReportInput
    description: str = "Return a google analytics report for the information the user requires"

    def _execute(self, met, dim, start, end):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4api-34c2ef9a36e9.json'
        pid=376881934
        client = BetaAnalyticsDataClient()

        # m = getMetric(met)
        # d = getDim(dim)
        # mi=[]
        # for x in m:
        #     mi.append(Metric(name=x))
        # if len(m)==0:
        #     return "No metric found"
        # di = []
        # for x in d:
        #     di.append(Dimension(name=x))
        #     return "No dimension found"
        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=(Dimension(name="city")),
            metrics=(Metric(name="activeUsers")),
            date_ranges=[DateRange(start_date=start, end_date=end)],
        )
        response = client.run_report(request)

        str = ""
        for row in response.rows:
            str = str + "\n"
            for x in row.dimension_values:
                str = str + x.value + " "

            for x in row.metric_values:
                str = str + x.value + " "

        return str