import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional, Dict
import time
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
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "superagi/tools/external_tools/google-analytics-tool-superagi/ga4api-34c2e.json"
        pid=self.get_tool_config("property_id")
        #property_id_here
        client = BetaAnalyticsDataClient()

        m = self.getMetric(met)

        mli=m.split('\', \'')
        mli[0]=mli[0][2:]
        mli[-1]=mli[-1][:-2]

        mi=[]

        for x in mli:
            mi.append(Metric(name=x))
        if len(m)==0:
            return "No metric found"

        d = self.getDim(dim)

        dli = d.split('\', \'')
        dli[0] = dli[0][2:]
        dli[-1] = dli[-1][:-2]

        di=[]

        for x in dli:
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
        prompt = """Take the following metrics into consideration
            {st}
            From the following metric API names, form and return a list of less than 10 metrics that correspond the best with the given metrics above. They should be a subset of the above provided dimensions. For example, if asked for active users, do not add cohortActiveUsers which has data which is unnecessary and is not queried for. Only find extremely relevant metric API name. If not found, return empty string.
            ['active1DayUsers', 'active28DayUsers', 'active7DayUsers', 'activeUsers', 'adUnitExposure', 'addToCarts', 'advertiserAdClicks', 'advertiserAdCost', 'advertiserAdCostPerClick', 'advertiserAdCostPerConversion', 'advertiserAdImpressions', 'averagePurchaseRevenue', 'averagePurchaseRevenuePerPayingUser', 'averagePurchaseRevenuePerUser', 'averageRevenuePerUser', 'averageSessionDuration', 'bounceRate', 'cartToViewRate', 'checkouts', 'cohortActiveUsers', 'cohortTotalUsers', 'conversions', 'crashAffectedUsers', 'crashFreeUsersRate', 'dauPerMau', 'dauPerWau', 'ecommercePurchases', 'engagedSessions', 'engagementRate', 'eventCount', 'eventCountPerUser', 'eventValue', 'eventsPerSession', 'firstTimePurchaserConversionRate', 'firstTimePurchasers', 'firstTimePurchasersPerNewUser', 'grossItemRevenue', 'grossPurchaseRevenue', 'itemListClickEvents', 'itemListClickThroughRate', 'itemListViewEvents', 'itemPromotionClickThroughRate', 'itemRefundAmount', 'itemRevenue', 'itemViewEvents', 'itemsAddedToCart', 'itemsCheckedOut', 'itemsClickedInList', 'itemsClickedInPromotion', 'itemsPurchased', 'itemsViewed', 'itemsViewedInList', 'itemsViewedInPromotion', 'newUsers', 'organicGoogleSearchAveragePosition', 'organicGoogleSearchClickThroughRate', 'organicGoogleSearchClicks', 'organicGoogleSearchImpressions', 'promotionClicks', 'promotionViews', 'publisherAdClicks', 'publisherAdImpressions', 'purchaseRevenue', 'purchaseToViewRate', 'purchaserConversionRate', 'refundAmount', 'returnOnAdSpend', 'screenPageViews', 'screenPageViewsPerSession', 'screenPageViewsPerUser', 'scrolledUsers', 'sessionConversionRate', 'sessions', 'sessionsPerUser', 'shippingAmount', 'taxAmount', 'totalAdRevenue', 'totalPurchasers', 'totalRevenue', 'totalUsers', 'transactions', 'transactionsPerPurchaser', 'userConversionRate', 'userEngagementDuration', 'wauPerMau']"""

        return self.generate(prompt,metr)

    def getDim(self, dim: str) -> List[str]:
        prompt = """Take the following dimensions into consideration
            {st}
            From the following dimension API names, form and return a list of less than 10 dimensions that correspond the best with the given dimensions above. They should be a subset of the above provided dimensions. For example, if asked for date do not add dimensions such as dateHour, which has data which is unnecessary and is not queried for. Only find extremely relevant dimension API names. If not found, return empty string.
            ['achievementId', 'adFormat', 'adSourceName', 'adUnitName', 'appVersion', 'audienceId', 'audienceName', 'brandingInterest', 'browser', 'campaignId', 'campaignName', 'character', 'city', 'cityId', 'cohort', 'cohortNthDay', 'cohortNthMonth', 'cohortNthWeek', 'contentGroup', 'contentId', 'contentType', 'continent', 'continentId', 'country', 'countryId', 'date', 'dateHour', 'dateHourMinute', 'day', 'dayOfWeek', 'dayOfWeekName', 'defaultChannelGroup', 'deviceCategory', 'deviceModel', 'eventName', 'fileExtension', 'fileName', 'firstSessionDate', 'firstUserCampaignId', 'firstUserCampaignName', 'firstUserDefaultChannelGroup', 'firstUserGoogleAdsAccountName', 'firstUserGoogleAdsAdGroupId', 'firstUserGoogleAdsAdGroupName', 'firstUserGoogleAdsAdNetworkType', 'firstUserGoogleAdsCampaignId', 'firstUserGoogleAdsCampaignName', 'firstUserGoogleAdsCampaignType', 'firstUserGoogleAdsCreativeId', 'firstUserGoogleAdsCustomerId', 'firstUserGoogleAdsKeyword', 'firstUserGoogleAdsQuery', 'firstUserManualAdContent', 'firstUserManualTerm', 'firstUserMedium', 'firstUserSource', 'firstUserSourceMedium', 'firstUserSourcePlatform', 'fullPageUrl', 'googleAdsAccountName', 'googleAdsAdGroupId', 'googleAdsAdGroupName', 'googleAdsAdNetworkType', 'googleAdsCampaignId', 'googleAdsCampaignName', 'googleAdsCampaignType', 'googleAdsCreativeId', 'googleAdsCustomerId', 'googleAdsKeyword', 'googleAdsQuery', 'groupId', 'hostName', 'hour', 'isConversionEvent', 'isoWeek', 'isoYear', 'isoYearIsoWeek', 'itemAffiliation', 'itemBrand', 'itemCategory', 'itemCategory2', 'itemCategory3', 'itemCategory4', 'itemCategory5', 'itemId', 'itemListId', 'itemListName', 'itemListPosition', 'itemLocationID', 'itemName', 'itemPromotionCreativeName', 'itemPromotionCreativeSlot', 'itemPromotionId', 'itemPromotionName', 'itemVariant', 'landingPage', 'landingPagePlusQueryString', 'language', 'languageCode', 'level', 'linkClasses', 'linkDomain', 'linkId', 'linkText', 'linkUrl', 'manualAdContent', 'manualTerm', 'medium', 'method', 'minute', 'mobileDeviceBranding', 'mobileDeviceMarketingName', 'mobileDeviceModel', 'month', 'newVsReturning', 'nthDay', 'nthHour', 'nthMinute', 'nthMonth', 'nthWeek', 'nthYear', 'operatingSystem', 'operatingSystemVersion', 'operatingSystemWithVersion', 'orderCoupon', 'outbound', 'pageLocation', 'pagePath', 'pagePathPlusQueryString', 'pageReferrer', 'pageTitle', 'percentScrolled', 'platform', 'platformDeviceCategory', 'region', 'screenResolution', 'searchTerm', 'sessionCampaignId', 'sessionCampaignName', 'sessionDefaultChannelGroup', 'sessionGoogleAdsAccountName', 'sessionGoogleAdsAdGroupId', 'sessionGoogleAdsAdGroupName', 'sessionGoogleAdsAdNetworkType', 'sessionGoogleAdsCampaignId', 'sessionGoogleAdsCampaignName', 'sessionGoogleAdsCampaignType', 'sessionGoogleAdsCreativeId', 'sessionGoogleAdsCustomerId', 'sessionGoogleAdsKeyword', 'sessionGoogleAdsQuery', 'sessionManualAdContent', 'sessionManualTerm', 'sessionMedium', 'sessionSa360AdGroupName', 'sessionSa360CampaignId', 'sessionSa360CampaignName', 'sessionSa360CreativeFormat', 'sessionSa360EngineAccountId', 'sessionSa360EngineAccountName', 'sessionSa360EngineAccountType', 'sessionSa360Keyword', 'sessionSa360Medium', 'sessionSa360Query', 'sessionSa360Source', 'sessionSource', 'sessionSourceMedium', 'sessionSourcePlatform', 'shippingTier', 'signedInWithUserId', 'source', 'sourceMedium', 'sourcePlatform', 'streamId', 'streamName', 'testDataFilterId', 'testDataFilterName', 'transactionId', 'unifiedPagePathScreen', 'unifiedPageScreen', 'unifiedScreenClass', 'unifiedScreenName', 'userAgeBracket', 'userGender', 'videoProvider', 'videoTitle', 'videoUrl', 'virtualCurrencyName', 'visible', 'week', 'year', 'yearMonth', 'yearWeek']"""

        return self.generate(prompt,dim)


    def generate(self, prompt, st: str) -> List[str]:
        prompt = prompt.replace("{st}", st)

        messages = [{"role": "system", "content": prompt}]
        result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
        return result["content"]

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
