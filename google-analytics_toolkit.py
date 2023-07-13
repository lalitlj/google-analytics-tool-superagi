from abc import ABC
import os
from superagi.tools.base_tool import BaseToolkit, BaseTool
from typing import List

class AnalyticsToolkit(BaseToolkit, ABC):
    name: str = "Google Analytics Toolkit"
    description: str = "Google Analytics Toolkit returns google analytics reports requested by the user"

    def get_tools(self) -> List[BaseTool]:
        return [reportTool()]

    def get_env_keys(self) -> List[str]:
        return ["GOOGLE_APPLICATION_CREDENTIALS"]