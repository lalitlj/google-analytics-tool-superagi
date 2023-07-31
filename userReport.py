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
        print(m)
        print(
            "AJBKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ0")
        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        d = self.getDim(dim)
        mi=[]
        for x in m:
            mi.append(Metric(name=x))
        if len(m)==0:
            return "No metric found"

        print(mi)
        print("AJBKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ0")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        di = []
        for x in d:
            di.append(Dimension(name=x))
        if len(d)==0:
            return "No dimension found"

        print(di)


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
        # p = []
        #
        # li= ['active1DayUsers\n', 'active28DayUsers\n', 'active7DayUsers\n', 'activeUsers\n', 'adUnitExposure\n', 'addToCarts\n', 'advertiserAdClicks\n', 'advertiserAdCost\n', 'advertiserAdCostPerClick\n', 'advertiserAdCostPerConversion\n', 'advertiserAdImpressions\n', 'averagePurchaseRevenue\n', 'averagePurchaseRevenuePerPayingUser\n', 'averagePurchaseRevenuePerUser\n', 'averageRevenuePerUser\n', 'averageSessionDuration\n', 'bounceRate\n', 'cartToViewRate\n', 'checkouts\n', 'cohortActiveUsers\n', 'cohortTotalUsers\n', 'conversions\n', 'crashAffectedUsers\n', 'crashFreeUsersRate\n', 'dauPerMau\n', 'dauPerWau\n', 'ecommercePurchases\n', 'engagedSessions\n', 'engagementRate\n', 'eventCount\n', 'eventCountPerUser\n', 'eventValue\n', 'eventsPerSession\n', 'firstTimePurchaserConversionRate\n', 'firstTimePurchasers\n', 'firstTimePurchasersPerNewUser\n', 'grossItemRevenue\n', 'grossPurchaseRevenue\n', 'itemListClickEvents\n', 'itemListClickThroughRate\n', 'itemListViewEvents\n', 'itemPromotionClickThroughRate\n', 'itemRefundAmount\n', 'itemRevenue\n', 'itemViewEvents\n', 'itemsAddedToCart\n', 'itemsCheckedOut\n', 'itemsClickedInList\n', 'itemsClickedInPromotion\n', 'itemsPurchased\n', 'itemsViewed\n', 'itemsViewedInList\n', 'itemsViewedInPromotion\n', 'newUsers\n', 'organicGoogleSearchAveragePosition\n', 'organicGoogleSearchClickThroughRate\n', 'organicGoogleSearchClicks\n', 'organicGoogleSearchImpressions\n', 'promotionClicks\n', 'promotionViews\n', 'publisherAdClicks\n', 'publisherAdImpressions\n', 'purchaseRevenue\n', 'purchaseToViewRate\n', 'purchaserConversionRate\n', 'refundAmount\n', 'returnOnAdSpend\n', 'screenPageViews\n', 'screenPageViewsPerSession\n', 'screenPageViewsPerUser\n', 'scrolledUsers\n', 'sessionConversionRate\n', 'sessions\n', 'sessionsPerUser\n', 'shippingAmount\n', 'taxAmount\n', 'totalAdRevenue\n', 'totalPurchasers\n', 'totalRevenue\n', 'totalUsers\n', 'transactions\n', 'transactionsPerPurchaser\n', 'userConversionRate\n', 'userEngagementDuration\n', 'wauPerMau\n']
        #
        # for st in li:
        #     st=st.rstrip('\n')
        #     prompt = """You will only respond with either 1, or 0.
        #         Return 1 if a part of the metrics {metr} refers to {st}, else return 0."""
        #     prompt = prompt.replace("{metr}", metr)
        #     if self.generate(prompt,st):
        #             p.append(st)
        #     time.sleep(0.000001)
        #
        # return p
        prompt = """Take the following dimension into consideration, which stands for the data required
            {st}
            Among the following dimension API names, form and return a list of less than 10 dimensions that correspond the best with the given dimensions above. They should be a subset of the above provided dimensions, and not point to other data not required.
            ['active1DayUsers', 'active28DayUsers', 'active7DayUsers', 'activeUsers', 'adUnitExposure', 'addToCarts', 'advertiserAdClicks', 'advertiserAdCost', 'advertiserAdCostPerClick', 'advertiserAdCostPerConversion', 'advertiserAdImpressions', 'averagePurchaseRevenue', 'averagePurchaseRevenuePerPayingUser', 'averagePurchaseRevenuePerUser', 'averageRevenuePerUser', 'averageSessionDuration', 'bounceRate', 'cartToViewRate', 'checkouts', 'cohortActiveUsers', 'cohortTotalUsers', 'conversions', 'crashAffectedUsers', 'crashFreeUsersRate', 'dauPerMau', 'dauPerWau', 'ecommercePurchases', 'engagedSessions', 'engagementRate', 'eventCount', 'eventCountPerUser', 'eventValue', 'eventsPerSession', 'firstTimePurchaserConversionRate', 'firstTimePurchasers', 'firstTimePurchasersPerNewUser', 'grossItemRevenue', 'grossPurchaseRevenue', 'itemListClickEvents', 'itemListClickThroughRate', 'itemListViewEvents', 'itemPromotionClickThroughRate', 'itemRefundAmount', 'itemRevenue', 'itemViewEvents', 'itemsAddedToCart', 'itemsCheckedOut', 'itemsClickedInList', 'itemsClickedInPromotion', 'itemsPurchased', 'itemsViewed', 'itemsViewedInList', 'itemsViewedInPromotion', 'newUsers', 'organicGoogleSearchAveragePosition', 'organicGoogleSearchClickThroughRate', 'organicGoogleSearchClicks', 'organicGoogleSearchImpressions', 'promotionClicks', 'promotionViews', 'publisherAdClicks', 'publisherAdImpressions', 'purchaseRevenue', 'purchaseToViewRate', 'purchaserConversionRate', 'refundAmount', 'returnOnAdSpend', 'screenPageViews', 'screenPageViewsPerSession', 'screenPageViewsPerUser', 'scrolledUsers', 'sessionConversionRate', 'sessions', 'sessionsPerUser', 'shippingAmount', 'taxAmount', 'totalAdRevenue', 'totalPurchasers', 'totalRevenue', 'totalUsers', 'transactions', 'transactionsPerPurchaser', 'userConversionRate', 'userEngagementDuration', 'wauPerMau']"""

        return self.generate(prompt,metr)

    def getDim(self, dim: str) -> List[str]:
        # p = []
        #
        # li=['achievementId\n', 'adFormat\n', 'adSourceName\n', 'adUnitName\n', 'appVersion\n', 'audienceId\n', 'audienceName\n', 'brandingInterest\n', 'browser\n', 'campaignId\n', 'campaignName\n', 'character\n', 'city\n', 'cityId\n', 'cohort\n', 'cohortNthDay\n', 'cohortNthMonth\n', 'cohortNthWeek\n', 'contentGroup\n', 'contentId\n', 'contentType\n', 'continent\n', 'continentId\n', 'country\n', 'countryId\n', 'date\n', 'dateHour\n', 'dateHourMinute\n', 'day\n', 'dayOfWeek\n', 'dayOfWeekName\n', 'defaultChannelGroup\n', 'deviceCategory\n', 'deviceModel\n', 'eventName\n', 'fileExtension\n', 'fileName\n', 'firstSessionDate\n', 'firstUserCampaignId\n', 'firstUserCampaignName\n', 'firstUserDefaultChannelGroup\n', 'firstUserGoogleAdsAccountName\n', 'firstUserGoogleAdsAdGroupId\n', 'firstUserGoogleAdsAdGroupName\n', 'firstUserGoogleAdsAdNetworkType\n', 'firstUserGoogleAdsCampaignId\n', 'firstUserGoogleAdsCampaignName\n', 'firstUserGoogleAdsCampaignType\n', 'firstUserGoogleAdsCreativeId\n', 'firstUserGoogleAdsCustomerId\n', 'firstUserGoogleAdsKeyword\n', 'firstUserGoogleAdsQuery\n', 'firstUserManualAdContent\n', 'firstUserManualTerm\n', 'firstUserMedium\n', 'firstUserSource\n', 'firstUserSourceMedium\n', 'firstUserSourcePlatform\n', 'fullPageUrl\n', 'googleAdsAccountName\n', 'googleAdsAdGroupId\n', 'googleAdsAdGroupName\n', 'googleAdsAdNetworkType\n', 'googleAdsCampaignId\n', 'googleAdsCampaignName\n', 'googleAdsCampaignType\n', 'googleAdsCreativeId\n', 'googleAdsCustomerId\n', 'googleAdsKeyword\n', 'googleAdsQuery\n', 'groupId\n', 'hostName\n', 'hour\n', 'isConversionEvent\n', 'isoWeek\n', 'isoYear\n', 'isoYearIsoWeek\n', 'itemAffiliation\n', 'itemBrand\n', 'itemCategory\n', 'itemCategory2\n', 'itemCategory3\n', 'itemCategory4\n', 'itemCategory5\n', 'itemId\n', 'itemListId\n', 'itemListName\n', 'itemListPosition\n', 'itemLocationID\n', 'itemName\n', 'itemPromotionCreativeName\n', 'itemPromotionCreativeSlot\n', 'itemPromotionId\n', 'itemPromotionName\n', 'itemVariant\n', 'landingPage\n', 'landingPagePlusQueryString\n', 'language\n', 'languageCode\n', 'level\n', 'linkClasses\n', 'linkDomain\n', 'linkId\n', 'linkText\n', 'linkUrl\n', 'manualAdContent\n', 'manualTerm\n', 'medium\n', 'method\n', 'minute\n', 'mobileDeviceBranding\n', 'mobileDeviceMarketingName\n', 'mobileDeviceModel\n', 'month\n', 'newVsReturning\n', 'nthDay\n', 'nthHour\n', 'nthMinute\n', 'nthMonth\n', 'nthWeek\n', 'nthYear\n', 'operatingSystem\n', 'operatingSystemVersion\n', 'operatingSystemWithVersion\n', 'orderCoupon\n', 'outbound\n', 'pageLocation\n', 'pagePath\n', 'pagePathPlusQueryString\n', 'pageReferrer\n', 'pageTitle\n', 'percentScrolled\n', 'platform\n', 'platformDeviceCategory\n', 'region\n', 'screenResolution\n', 'searchTerm\n', 'sessionCampaignId\n', 'sessionCampaignName\n', 'sessionDefaultChannelGroup\n', 'sessionGoogleAdsAccountName\n', 'sessionGoogleAdsAdGroupId\n', 'sessionGoogleAdsAdGroupName\n', 'sessionGoogleAdsAdNetworkType\n', 'sessionGoogleAdsCampaignId\n', 'sessionGoogleAdsCampaignName\n', 'sessionGoogleAdsCampaignType\n', 'sessionGoogleAdsCreativeId\n', 'sessionGoogleAdsCustomerId\n', 'sessionGoogleAdsKeyword\n', 'sessionGoogleAdsQuery\n', 'sessionManualAdContent\n', 'sessionManualTerm\n', 'sessionMedium\n', 'sessionSa360AdGroupName\n', 'sessionSa360CampaignId\n', 'sessionSa360CampaignName\n', 'sessionSa360CreativeFormat\n', 'sessionSa360EngineAccountId\n', 'sessionSa360EngineAccountName\n', 'sessionSa360EngineAccountType\n', 'sessionSa360Keyword\n', 'sessionSa360Medium\n', 'sessionSa360Query\n', 'sessionSa360Source\n', 'sessionSource\n', 'sessionSourceMedium\n', 'sessionSourcePlatform\n', 'shippingTier\n', 'signedInWithUserId\n', 'source\n', 'sourceMedium\n', 'sourcePlatform\n', 'streamId\n', 'streamName\n', 'testDataFilterId\n', 'testDataFilterName\n', 'transactionId\n', 'unifiedPagePathScreen\n', 'unifiedPageScreen\n', 'unifiedScreenClass\n', 'unifiedScreenName\n', 'userAgeBracket\n', 'userGender\n', 'videoProvider\n', 'videoTitle\n', 'videoUrl\n', 'virtualCurrencyName\n', 'visible\n', 'week\n', 'year\n', 'yearMonth\n', 'yearWeek\n']
        #
        # for st in li:
        #     st=st.rstrip('\n')
        #     prompt = """You will only respond with either 1, or 0.
        #         Return 1 if a part of the dimensions {dim} refers to {st}, else return 0."""
        #     prompt = prompt.replace("{dim}", dim)
        #     if self.generate(prompt, st):
        #         p.append(st)
        #     time.sleep(0.000001)
        #
        # return p
        p=[]
        prompt = """Take the following dimension into consideration, which stands for the data required
                    {st}
                    Among the following dimension API names, form and return a list of less than 10 dimensions that correspond the best with the given dimensions above. They should be a subset of the above provided dimensions, and not point to other data not required.
                    ['achievementId', 'adFormat', 'adSourceName', 'adUnitName', 'appVersion', 'audienceId', 'audienceName', 'brandingInterest', 'browser', 'campaignId', 'campaignName', 'character', 'city', 'cityId', 'cohort', 'cohortNthDay', 'cohortNthMonth', 'cohortNthWeek', 'contentGroup', 'contentId', 'contentType', 'continent', 'continentId', 'country', 'countryId', 'date', 'dateHour', 'dateHourMinute', 'day', 'dayOfWeek', 'dayOfWeekName', 'defaultChannelGroup', 'deviceCategory', 'deviceModel', 'eventName', 'fileExtension', 'fileName', 'firstSessionDate', 'firstUserCampaignId', 'firstUserCampaignName', 'firstUserDefaultChannelGroup', 'firstUserGoogleAdsAccountName', 'firstUserGoogleAdsAdGroupId', 'firstUserGoogleAdsAdGroupName', 'firstUserGoogleAdsAdNetworkType', 'firstUserGoogleAdsCampaignId', 'firstUserGoogleAdsCampaignName', 'firstUserGoogleAdsCampaignType', 'firstUserGoogleAdsCreativeId', 'firstUserGoogleAdsCustomerId', 'firstUserGoogleAdsKeyword', 'firstUserGoogleAdsQuery', 'firstUserManualAdContent', 'firstUserManualTerm', 'firstUserMedium', 'firstUserSource', 'firstUserSourceMedium', 'firstUserSourcePlatform', 'fullPageUrl', 'googleAdsAccountName', 'googleAdsAdGroupId', 'googleAdsAdGroupName', 'googleAdsAdNetworkType', 'googleAdsCampaignId', 'googleAdsCampaignName', 'googleAdsCampaignType', 'googleAdsCreativeId', 'googleAdsCustomerId', 'googleAdsKeyword', 'googleAdsQuery', 'groupId', 'hostName', 'hour', 'isConversionEvent', 'isoWeek', 'isoYear', 'isoYearIsoWeek', 'itemAffiliation', 'itemBrand', 'itemCategory', 'itemCategory2', 'itemCategory3', 'itemCategory4', 'itemCategory5', 'itemId', 'itemListId', 'itemListName', 'itemListPosition', 'itemLocationID', 'itemName', 'itemPromotionCreativeName', 'itemPromotionCreativeSlot', 'itemPromotionId', 'itemPromotionName', 'itemVariant', 'landingPage', 'landingPagePlusQueryString', 'language', 'languageCode', 'level', 'linkClasses', 'linkDomain', 'linkId', 'linkText', 'linkUrl', 'manualAdContent', 'manualTerm', 'medium', 'method', 'minute', 'mobileDeviceBranding', 'mobileDeviceMarketingName', 'mobileDeviceModel', 'month', 'newVsReturning', 'nthDay', 'nthHour', 'nthMinute', 'nthMonth', 'nthWeek', 'nthYear', 'operatingSystem', 'operatingSystemVersion', 'operatingSystemWithVersion', 'orderCoupon', 'outbound', 'pageLocation', 'pagePath', 'pagePathPlusQueryString', 'pageReferrer', 'pageTitle', 'percentScrolled', 'platform', 'platformDeviceCategory', 'region', 'screenResolution', 'searchTerm', 'sessionCampaignId', 'sessionCampaignName', 'sessionDefaultChannelGroup', 'sessionGoogleAdsAccountName', 'sessionGoogleAdsAdGroupId', 'sessionGoogleAdsAdGroupName', 'sessionGoogleAdsAdNetworkType', 'sessionGoogleAdsCampaignId', 'sessionGoogleAdsCampaignName', 'sessionGoogleAdsCampaignType', 'sessionGoogleAdsCreativeId', 'sessionGoogleAdsCustomerId', 'sessionGoogleAdsKeyword', 'sessionGoogleAdsQuery', 'sessionManualAdContent', 'sessionManualTerm', 'sessionMedium', 'sessionSa360AdGroupName', 'sessionSa360CampaignId', 'sessionSa360CampaignName', 'sessionSa360CreativeFormat', 'sessionSa360EngineAccountId', 'sessionSa360EngineAccountName', 'sessionSa360EngineAccountType', 'sessionSa360Keyword', 'sessionSa360Medium', 'sessionSa360Query', 'sessionSa360Source', 'sessionSource', 'sessionSourceMedium', 'sessionSourcePlatform', 'shippingTier', 'signedInWithUserId', 'source', 'sourceMedium', 'sourcePlatform', 'streamId', 'streamName', 'testDataFilterId', 'testDataFilterName', 'transactionId', 'unifiedPagePathScreen', 'unifiedPageScreen', 'unifiedScreenClass', 'unifiedScreenName', 'userAgeBracket', 'userGender', 'videoProvider', 'videoTitle', 'videoUrl', 'virtualCurrencyName', 'visible', 'week', 'year', 'yearMonth', 'yearWeek']"""

        return self.generate(prompt,dim)


    def generate(self, prompt, st: str) -> bool:
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
