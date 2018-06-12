# -*- coding: utf-8 -*-
import re

import scrapy
from chinanpo.items import ChinanpoItem


class ChinanpoSpider(scrapy.Spider):
    name = 'chinanpoSpider'
    allowed_domains = ['www.chinanpo.gov.cn']
    start_urls = ['http://www.chinanpo.gov.cn/']

    # REQUEST_HEADERS = {
    #     'Host': "www.chinanpo.gov.cn",
    #     "Origin": "http://www.chinanpo.gov.cn",
    #     "Referer": "http://www.chinanpo.gov.cn/search/orgcx.html"
    # }
    REQUEST_HEADERS = {
        'Host': "www.chinanpo.gov.cn",
        "Origin": "http://www.chinanpo.gov.cn",
        "Referer": "http://www.chinanpo.gov.cn/search/orgcx.html",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.3',
    }
    current_page = 0


    def start_requests(self):
        FormData = {
            "status": "2",
            "tabIndex": "2",
            "regNum": "-1",
            "page_flag": "true",
            "pagesize_key": "macList",
            "goto_page": "next",
            "current_page": "4",
            "total_count": "798576",
            "page_size": "10000",
        }
        url = "http://www.chinanpo.gov.cn/search/orgcx.html"
        return [scrapy.FormRequest(url, formdata=FormData, method='POST', callback=self.parse,
                                   headers=self.REQUEST_HEADERS)]
        # pass

    def parse(self, response):
        lines = response.xpath('//*[@id="local-data"]//tr/td/a/@href').extract()
        for line in lines:
            match_obj = re.match(r".*\"(\w+)?\".*,\"?(\w+)\"", line)
            if match_obj:
                i = match_obj.group(1)
                u = match_obj.group(2)
                # self.parse_iu(str(url))
                url = "http://www.chinanpo.gov.cn/search/poporg.html?i={}&u={}".format(i, u)
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={"unified_social_credit_code": u})
        # self.current_page += 1
        # FormData = {
        #     "status": "2",
        #     "tabIndex": "2",
        #     "regNum": "-1",
        #     "page_flag": "true",
        #     "pagesize_key": "macList",
        #     "goto_page": "next",
        #     "current_page": str(self.current_page),
        #     "total_count": "798576",
        #     "page_size": "3000",
        # }
        # yield [scrapy.FormRequest(url, formdata=FormData, method='POST', callback=self.parse,
        #                          headers=self.REQUEST_HEADERS)]

    def parse_detail(self, response):
        # //div[@class="title_bg"]/h3/text()
        # /html/body/div/div[2]/table/tbody/tr/td[2]
        # /html/body/div/div[2]/table/tbody/tr/td[4]

        unified_social_credit_code = response.meta.get("unified_social_credit_code")
        name_and_uscc = response.xpath('//div[@class="title_bg"]//text()').extract_first()
        name = name_and_uscc.strip().split("统一社会信用代码")[0].strip()

        left = response.xpath('//tr/td[2]/text()').extract()
        right = response.xpath('//tr/td[4]/text()').extract()

        left = [i.strip() for i in left]
        right = [i.strip() for i in right]

        registration_org = left[0]
        legal = left[1]
        website = right[5]
        address = left[4]
        competent_org = right[0]
        registration_fund = left[2]
        status = right[2]
        org_type = left[3]
        phone_num = left[5]
        business = left[6]
        expiry_date = right[4]

        # name = scrapy.Field()
        # unified_social_credit_code = scrapy.Field()  # Unified Social Credit Code 统一社会信用代码
        # registration_org = scrapy.Field()  # 登记管理机关
        # legal = scrapy.Field()  # 法定代表人
        # website = scrapy.Field()  # 网址
        # registration_id = scrapy.Field()  # 登记证号
        # address = scrapy.Field()  # 住所
        # competent_org = scrapy.Field()  # 业务主管单位
        # registration_fund = scrapy.Field()  # 注册资金
        # status = scrapy.Field()  # 登记状态
        # type = scrapy.Field()  # 社会组织类型
        item = ChinanpoItem()

        item["name"] = name
        item["unified_social_credit_code"] = unified_social_credit_code
        item["registration_org"] = registration_org
        item["legal"] = legal
        item["website"] = website
        item["address"] = address
        item["competent_org"] = competent_org
        item["registration_fund"] = registration_fund
        item["org_type"] = org_type
        item["phone_num"] = phone_num
        item["expiry_date"] = expiry_date
        item["business"] = business
        item["status"] = status

        yield item

    def parse_uscc(str_value):
        match_obj = re.match(r".*?(\d+).*", str_value)
        if match_obj:
            return match_obj.group(1)

    def parse_iu(str_value):
        pass
