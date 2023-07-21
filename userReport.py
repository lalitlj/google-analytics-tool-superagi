import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional, Dict
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
    llm: Optional[BaseLlm] = None

    def _execute(self, dim: str, met: str, start: str, end: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "superagi/tools/google-analytics-tool-superagi/ga4api-34c2e.json"
        # pid=int(self.get_tool_config('property_id'))
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
        if len(d)==0:
            return "No dimension found"
        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=di,
            metrics=mi,
            date_ranges=[DateRange(start_date=start, end_date=end)],
            limit=100000,
            offset=0,
        )
        response = client.run_report(request)

        # beautify
        return self.beautify(response.rows,di,mi)

    def getMetric(self, metr: str) -> List[str]:
        p = []

        file = open("met.txt", "r")
        li=file.readlines()

        for str in li:
            prompt = """1 if given {metr} stands for {str}"""
            if self.generate(prompt,str[:-2]):
                p.append(str[:-2])

        # prompt = """1 if given {metr} means for the number of active users, else 0."""
        # if self.generate(prompt, metr):
        #     p.append("activeUsers")
        # prompt = """1 if given {metr} means the number of times users added items to shopping carts, else 0."""
        # if self.generate(prompt, metr):
        #     p.append("addToCarts")
        # prompt = """1 if given {metr} means the bounce rate, else 0."""
        # if self.generate(prompt, metr):
        #     p.append("bounceRate")
        # prompt = """1 if given {metr} means new users, else 0."""
        # if self.generate(prompt, metr):
        #     p.append("newUsers")
        return p

    def getDim(self, dim: str) -> List[str]:
        p = []

        file = open("met.txt", "r")
        li = file.readlines()

        for str in li:
            prompt = """1 if given {metr} stands for {str}"""
            if self.generate(prompt, str[:-2]):
                p.append(str[:-2])

        # prompt = """1 if given {dim} means names of the cities the user activity originated from, else 0."""
        # if self.generate(prompt, dim):
        #     p.append("city")
        # prompt = """1 if given {dim} means the IDs of the cities the user activity originated from, else 0."""
        # if self.generate(prompt, dim):
        #     p.append("cityId")
        # prompt = """1 if given {dim} means the name of the marketing campaign, else 0."""
        # if self.generate(prompt, dim):
        #     p.append("campaignName")
        # prompt = """1 if given {dim} means the title of the pages viewed, else 0."""
        # if self.generate(prompt, dim):
        #     p.append("pageTitle")
        # prompt = """1 if given {dim} means the source of conversion event, else 0."""
        # if self.generate(prompt, dim):
        #     p.append("source")
        return p

    def generate(self, prompt, metr: str) -> bool:
        prompt = prompt.replace("{metr}", metr)

        messages = [{"role": "system", "content": prompt}]
        result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
        re = int(result["content"])
        return re

    def beautify(self,response: List[Dict[str,List[Dict[str,str]]]], di: List[str], mi: List[str]):
        prompt = f"""Return a beautified tabular form of the {response}
            data structure, which contains row entries with dimension values representing a list of
            dimensions {di} and row entries containing metric values representing a list of metrics
            {mi}. Also brief a description of the received data in a paragraph."""

        prompt = prompt.replace(f"{response}", str(response))
        prompt = prompt.replace(f"{di}", str(di))
        prompt = prompt.replace(f"{mi}", str(mi))

        messages = [{"role": "system", "content": prompt}]
        result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
        re = result["content"]
        return re
