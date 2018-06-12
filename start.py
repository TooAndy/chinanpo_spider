# /usr/bin/env python
# -*- coding: utf-8 -*-

# create by Andy

from scrapy.cmdline import execute
import re


def parse_iu(str_value):
    match_obj = re.match(r".*\"(\w+)?\".*,\"?(\w+)\"", str_value)
    if match_obj:
        i = match_obj.group(1)
        u = match_obj.group(2)
        return i, u


if __name__ == '__main__':
    execute("scrapy crawl chinanpoSpider".split(" "))
    # url = 'javascript:popOrgWin("970982","52510800MJQ0506533")'
    # #
    # # b = url.split("\"")[3]
    # # print(b)
    # print(parse_iu(url)[0])