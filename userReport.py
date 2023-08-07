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

    def _execute(self, start: str, end: str):

        pid=int(self.get_tool_config("PROPERTY_ID"))

        f=open("JSONcontent.json","w+")
        f.write(self.get_tool_config("GOOGLE_CREDENTIALS_FILE"))
        print(f.read())
        f.close()
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = "JSONcontent.json"

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(type(pid))
        print(pid)

        #property_id_here
        client = BetaAnalyticsDataClient()

        # m = self.getMetric(met)

        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(m)
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # mli=m.split('\', \'')
        # try:
        #     mli[0] = mli[0][mli[0].index('[')+2:]
        # except:
        #     return "No valid metric found"
        # mli[-1]=mli[-1][:-2]

        mi=[]
        mli=['newUsers','totalUsers']

        for x in mli:
            mi.append(Metric(name=x))


        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(mi)
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # d = self.getDim(dim)
        # if len(d)==0:
        #     return "No dimension found"
        #
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(d)
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        # dli = d.split('\', \'')
        # try:
        #     dli[0] = dli[0][dli[0].index('[') + 2:]
        # except:
        #     return "No valid dimension found"
        # dli[-1] = dli[-1][:-2]

        di=[]
        dli=['dateHour','city','country']

        for x in dli:
            di.append(Dimension(name=x))


        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(di)
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        request = RunReportRequest(
            property=f"properties/{pid}",
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

        # beautify
        return "Succesfully received a google analysis report\n"+st

    # def getMetric(self, metr: str) -> List[str]:
    #     prompt = """Take the following metrics into consideration, which stands for the data required
    #         {st}
    #         Among the following metric API names, form and return a list of less than 10 metrics that correspond the best with the given metrics above. They should be a subset of the above provided dimensions, and not point to other data not required. For example, if asked for active users, do not add cohortActiveUsers which has data which is unnecessary and is not queried for. Only find extremely relevant metric API name. If not found, return empty string.
    #         ['active1DayUsers', 'active28DayUsers', 'active7DayUsers', 'activeUsers', 'adUnitExposure', 'addToCarts', 'advertiserAdClicks', 'advertiserAdCost', 'advertiserAdCostPerClick', 'advertiserAdCostPerConversion', 'advertiserAdImpressions', 'averagePurchaseRevenue', 'averagePurchaseRevenuePerPayingUser', 'averagePurchaseRevenuePerUser', 'averageRevenuePerUser', 'averageSessionDuration', 'bounceRate', 'cartToViewRate', 'checkouts', 'cohortActiveUsers', 'cohortTotalUsers', 'conversions', 'crashAffectedUsers', 'crashFreeUsersRate', 'dauPerMau', 'dauPerWau', 'ecommercePurchases', 'engagedSessions', 'engagementRate', 'eventCount', 'eventCountPerUser', 'eventValue', 'eventsPerSession', 'firstTimePurchaserConversionRate', 'firstTimePurchasers', 'firstTimePurchasersPerNewUser', 'grossItemRevenue', 'grossPurchaseRevenue', 'itemListClickEvents', 'itemListClickThroughRate', 'itemListViewEvents', 'itemPromotionClickThroughRate', 'itemRefundAmount', 'itemRevenue', 'itemViewEvents', 'itemsAddedToCart', 'itemsCheckedOut', 'itemsClickedInList', 'itemsClickedInPromotion', 'itemsPurchased', 'itemsViewed', 'itemsViewedInList', 'itemsViewedInPromotion', 'newUsers', 'organicGoogleSearchAveragePosition', 'organicGoogleSearchClickThroughRate', 'organicGoogleSearchClicks', 'organicGoogleSearchImpressions', 'promotionClicks', 'promotionViews', 'publisherAdClicks', 'publisherAdImpressions', 'purchaseRevenue', 'purchaseToViewRate', 'purchaserConversionRate', 'refundAmount', 'returnOnAdSpend', 'screenPageViews', 'screenPageViewsPerSession', 'screenPageViewsPerUser', 'scrolledUsers', 'sessionConversionRate', 'sessions', 'sessionsPerUser', 'shippingAmount', 'taxAmount', 'totalAdRevenue', 'totalPurchasers', 'totalRevenue', 'totalUsers', 'transactions', 'transactionsPerPurchaser', 'userConversionRate', 'userEngagementDuration', 'wauPerMau']"""
    #
    #     return self.generate(prompt,metr)
    #
    # def getDim(self, dim: str) -> List[str]:
    #     prompt = """Take the following dimension into consideration, which stands for the data required
    #         {st}
    #         Among the following dimension API names, form and return a list of less than 10 dimensions that correspond the best with the given dimensions above. They should be a subset of the above provided dimensions, and not point to data not required. For example, if asked for date do not add dimensions such as dateHour, which has data which is unnecessary and is not queried for. Only find extremely relevant dimension API names. If not found, return empty string.
    #         ['achievementId', 'adFormat', 'adSourceName', 'adUnitName', 'appVersion', 'audienceId', 'audienceName', 'brandingInterest', 'browser', 'campaignId', 'campaignName', 'character', 'city', 'cityId', 'cohort', 'cohortNthDay', 'cohortNthMonth', 'cohortNthWeek', 'contentGroup', 'contentId', 'contentType', 'continent', 'continentId', 'country', 'countryId', 'date', 'dateHour', 'dateHourMinute', 'day', 'dayOfWeek', 'dayOfWeekName', 'defaultChannelGroup', 'deviceCategory', 'deviceModel', 'eventName', 'fileExtension', 'fileName', 'firstSessionDate', 'firstUserCampaignId', 'firstUserCampaignName', 'firstUserDefaultChannelGroup', 'firstUserGoogleAdsAccountName', 'firstUserGoogleAdsAdGroupId', 'firstUserGoogleAdsAdGroupName', 'firstUserGoogleAdsAdNetworkType', 'firstUserGoogleAdsCampaignId', 'firstUserGoogleAdsCampaignName', 'firstUserGoogleAdsCampaignType', 'firstUserGoogleAdsCreativeId', 'firstUserGoogleAdsCustomerId', 'firstUserGoogleAdsKeyword', 'firstUserGoogleAdsQuery', 'firstUserManualAdContent', 'firstUserManualTerm', 'firstUserMedium', 'firstUserSource', 'firstUserSourceMedium', 'firstUserSourcePlatform', 'fullPageUrl', 'googleAdsAccountName', 'googleAdsAdGroupId', 'googleAdsAdGroupName', 'googleAdsAdNetworkType', 'googleAdsCampaignId', 'googleAdsCampaignName', 'googleAdsCampaignType', 'googleAdsCreativeId', 'googleAdsCustomerId', 'googleAdsKeyword', 'googleAdsQuery', 'groupId', 'hostName', 'hour', 'isConversionEvent', 'isoWeek', 'isoYear', 'isoYearIsoWeek', 'itemAffiliation', 'itemBrand', 'itemCategory', 'itemCategory2', 'itemCategory3', 'itemCategory4', 'itemCategory5', 'itemId', 'itemListId', 'itemListName', 'itemListPosition', 'itemLocationID', 'itemName', 'itemPromotionCreativeName', 'itemPromotionCreativeSlot', 'itemPromotionId', 'itemPromotionName', 'itemVariant', 'landingPage', 'landingPagePlusQueryString', 'language', 'languageCode', 'level', 'linkClasses', 'linkDomain', 'linkId', 'linkText', 'linkUrl', 'manualAdContent', 'manualTerm', 'medium', 'method', 'minute', 'mobileDeviceBranding', 'mobileDeviceMarketingName', 'mobileDeviceModel', 'month', 'newVsReturning', 'nthDay', 'nthHour', 'nthMinute', 'nthMonth', 'nthWeek', 'nthYear', 'operatingSystem', 'operatingSystemVersion', 'operatingSystemWithVersion', 'orderCoupon', 'outbound', 'pageLocation', 'pagePath', 'pagePathPlusQueryString', 'pageReferrer', 'pageTitle', 'percentScrolled', 'platform', 'platformDeviceCategory', 'region', 'screenResolution', 'searchTerm', 'sessionCampaignId', 'sessionCampaignName', 'sessionDefaultChannelGroup', 'sessionGoogleAdsAccountName', 'sessionGoogleAdsAdGroupId', 'sessionGoogleAdsAdGroupName', 'sessionGoogleAdsAdNetworkType', 'sessionGoogleAdsCampaignId', 'sessionGoogleAdsCampaignName', 'sessionGoogleAdsCampaignType', 'sessionGoogleAdsCreativeId', 'sessionGoogleAdsCustomerId', 'sessionGoogleAdsKeyword', 'sessionGoogleAdsQuery', 'sessionManualAdContent', 'sessionManualTerm', 'sessionMedium', 'sessionSa360AdGroupName', 'sessionSa360CampaignId', 'sessionSa360CampaignName', 'sessionSa360CreativeFormat', 'sessionSa360EngineAccountId', 'sessionSa360EngineAccountName', 'sessionSa360EngineAccountType', 'sessionSa360Keyword', 'sessionSa360Medium', 'sessionSa360Query', 'sessionSa360Source', 'sessionSource', 'sessionSourceMedium', 'sessionSourcePlatform', 'shippingTier', 'signedInWithUserId', 'source', 'sourceMedium', 'sourcePlatform', 'streamId', 'streamName', 'testDataFilterId', 'testDataFilterName', 'transactionId', 'unifiedPagePathScreen', 'unifiedPageScreen', 'unifiedScreenClass', 'unifiedScreenName', 'userAgeBracket', 'userGender', 'videoProvider', 'videoTitle', 'videoUrl', 'virtualCurrencyName', 'visible', 'week', 'year', 'yearMonth', 'yearWeek']"""
    #
    #     return self.generate(prompt,dim)


    # def generate(self, prompt, st: str) -> List[str]:
    #     prompt = prompt.replace("{st}", st)
    #
    #     messages = [{"role": "system", "content": prompt}]
    #     result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
    #     return result["content"]
