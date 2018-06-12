# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinanpoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    unified_social_credit_code = scrapy.Field()  # Unified Social Credit Code 统一社会信用代码
    registration_org = scrapy.Field()  # 登记管理机关
    legal = scrapy.Field()  # 法定代表人
    website = scrapy.Field()  # 网址
    registration_id = scrapy.Field()  # 登记证号
    address = scrapy.Field()  # 住所
    competent_org = scrapy.Field()  # 业务主管单位
    registration_fund = scrapy.Field()  # 注册资金
    status = scrapy.Field()  # 登记状态
    org_type = scrapy.Field()  # 社会组织类型
    phone_num = scrapy.Field()
    business = scrapy.Field()  # 业务范围
    expiry_date = scrapy.Field()  # 有效期