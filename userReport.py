import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
import json
from typing import Type, Optional
from superagi.resource_manager.file_manager import FileManager
import yaml
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

class UserReportInput(BaseModel):
    start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end: str = Field(..., description=f"The last date of the query, in YYYY-MM-DD format, if today, return today's date")


class reportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Analytics Report Tool"
    args_schema: Type[BaseModel] = UserReportInput
    description: str = "Return a google analytics report for the information the user requires"
    resource_manager: Optional[FileManager] = None

    def _execute(self, start: str, end: str):

        property=int(self.get_tool_config("PROPERTY_ID"))
        dict = self.get_tool_config("GOOGLE_CREDENTIALS_FILE")

        writable = json.loads(json.loads(dict))
        with open("sample.json", "w") as outfile:
            json.dump(writable, outfile)
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = "sample.json"

        client = BetaAnalyticsDataClient()

        DimMetrics = self.returnDimMetrics()
        listofnames=[]

        for dimensions,metrics in DimMetrics:
            filename = dimensions[0]+metrics[0]
            if filename in listofnames:
                filename=filename+"New"
            filename=filename+".txt"
            listofnames.append(filename)

            mi=[]
            for x in metrics:
                mi.append(Metric(name=x))

            di=[]
            for x in dimensions:
                di.append(Dimension(name=x))

            request = RunReportRequest(
                property=f"properties/{property}",
                dimensions=di,
                metrics=mi,
                date_ranges=[DateRange(start_date=start, end_date=end)],
                limit=100000,
                offset=0,
            )
            response = client.run_report(request)

            st=""
            for dimensionHeader in response.dimension_headers:
                st= st+ dimensionHeader.name + " "
            for metricHeader in response.metric_headers:
                st= st + metricHeader.name +" "

            st= st+'\n'

            for row in response.rows:
                for i, dimension_value in enumerate(row.dimension_values):
                    st = st +dimension_value.value +" "

                for i, metric_value in enumerate(row.metric_values):
                    st= st+ metric_value.value+ " "
                st = st + '\n'

            self.resource_manager.write_file(filename,st)

        os.remove("sample.json")

        return "Succesfully wrote Google Analytics reports"

    def returnDimMetrics(self):
        DimMetrics = []
        # try:
        with open("superagi/tools/external-tools/google-analytics-tool-superagi/config.yaml", "r") as file:
            dict = yaml.parse(file)
            for lists in dict["list"]:
                DimMetrics.append([lists["Dimension"], lists["Metric"]])
            return DimMetrics
        # except:
        #     return [[['pageTitle'], ['totalUsers']], [
        #         ['deviceModel', 'deviceCategory'], ['totalUsers']], [['dateHour'],
        #                                                              ['totalUsers', 'averageSessionDuration',
        #                                                               'bounceRate']], [['sourceMedium'],
        #                                                                                ['totalUsers']]]