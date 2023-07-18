import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import date
from superagi.llms.base_llm import BaseLlm
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

    def _execute(self, dim: str, met: str, start: str, end: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "superagi/tools/google-analytics-tool-superagi/ga4api-34c2e.json"
        # pid=self.get_tool_config('property_id'
        pid=376881934
        client = BetaAnalyticsDataClient()

        m = self.getMetric(met)
        d = self.getDim(dim)
        mi=[]
        for x in m:
            mi.append(Metric(name=x))
        if len(m)==0:
            return "No metric found"
        di = []
        for x in d:
            di.append(Dimension(name=x))
            return "No dimension found"
        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=di,
            metrics=mi,
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

    def getMetric(self, metr: str) -> List[str]:
        p = []

        prompt = """1, if given {metr} means for the number of active users, else 0."""
        if self.generate(prompt, metr):
            p.append("activeUsers")
        prompt = """1, if given {metr} means for the number of times users added items to their shopping carts., else 0."""
        if self.generate(prompt, metr):
            p.append("addToCarts")
        p.append("country")
        return p

    def getDim(self, dim: str) -> List[str]:
        p = []
        prompt = """1, if given {dim} means names of the cities the user activity originated from, else 0."""
        if self.generate(prompt, dim):
            p.append("city")
        prompt = """1, if given {dim} means the IDs of the cities the user activity originated from, else 0."""
        if self.generate(prompt, dim):
            p.append("cityId")
        prompt = """1, if given {dim} means the name of the marketing campaign, else 0."""
        if self.generate(prompt, dim):
            p.append("campaignName")
        p.append("addToCarts")
        return p

    def generate(self, prompt, metr) -> bool:
        prompt = prompt.replace("{metr}", metr)

        messages = [{"role": "system", "content": prompt}]
        result = int(self.llm.chat_completion(messages, max_tokens=self.max_token_limit))
        return result