import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

class ReportInput(BaseModel):
    # met: str = Field(..., description="The metric the user wants to know, for example number of active users")
    # dim: str = Field(..., description="The context or dimension for which the user wants to know, for example, a city")
    # start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    # end: str = Field(..., description=f"The last date of the query, in YYYY-MM-DD format, if today, return today's date")
    m: int = Field(..., description="1, if the user has told to do something")

class singleUseTool(BaseTool):
    name: str = "Routine Analytics Report Tool"
    args_schema: Type[BaseModel] = ReportInput
    description: str = "Give routine weekly Google Analytics report"

    def _execute(self,m: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "superagi/tools/google-analytics-tool-superagi/ga4api-34c2e.json"
        # pid=int(self.get_tool_config('property_id'))
        pid=376881934
        client = BetaAnalyticsDataClient()

        str=""
        if m:
            str=" "

        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=[Dimension(name="country"),
                        Dimension(name="region"),
                        Dimension(name="city")],
            metrics=[Metric(name="activeUsers"),
                     Metric(name="newUsers"),
                     Metric(name="bounceRate")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
            limit=100000,
            offset=0,
        )

        response = client.run_report(request)

        re = "Country, Region, City, Users, New Users, Bounce \n"

        for row in response.rows():
            re = re + row.dimension_values[0].value +" "+row.dimension_values[1].value +" "+row.dimension_values[2].value +" "+row.metric_values[0].value+" "+row.metric_values[1].value+" "+row.metric_values[2].value+"\n"

        # Countries --------------------------------------------------------------------------------------------------------------------------------------------------

        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=[Dimension(name="country")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )

        response = client.run_report(request)
        ros=response.rows()
        ros=sorted(ros,key=self.sor,reverse=True)

        totalsessions=0
        for x in response.rows:
            totalsessions=totalsessions+int(x.metric_values[0].value)

        st="Top 5 Countries by session numbers and percentage:\n"
        for x in range(min(len(ros),5)):
            st=st+ros.dimension_values[0].value+" "+ros.metric_values[0].values+" "+(int(ros.metric_values[0])/totalsessions)+"\n"

        # Pages ------------------------------------------------------------------------------------------------------------------------------------------------------

        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=[Dimension(name="pageTitle")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )

        response = client.run_report(request)
        ros = response.rows()
        ros = sorted(ros, key=self.sor, reverse=True)

        pt = "Top 5 Pages by session numbers and percentage:\n"
        for x in range(min(len(ros), 5)):
            pt = pt + ros.dimension_values[0].value + " " + ros.metric_values[0].values + " " + (int(ros.metric_values[0]) / totalsessions) + "\n"

        # Sources ----------------------------------------------------------------------------------------------------------------------------------------------------

        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=[Dimension(name="source")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )

        response = client.run_report(request)
        ros = response.rows()
        ros = sorted(ros, key=self.sor, reverse=True)

        xt = "Top 5 Sources by session numbers and percentage:\n"
        for x in range(min(len(ros), 5)):
            xt = xt + ros.dimension_values[0].value + " " + ros.metric_values[0].values + " " + (int(ros.metric_values[0]) / totalsessions) + "\n"

        return [str, re, st, pt, xt]

    def sor(self, dict):
        return dict.metric_values[0].value