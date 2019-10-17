# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class majorItem(scrapy.Item):
    majorName = scrapy.Field()
    majorID = scrapy.Field()


class schoolItem(scrapy.Item):
    schoolName = scrapy.Field()  # 院校名称
    schoolLocation = scrapy.Field()  # 院校所在地
    schoolBeto = scrapy.Field()  # 院校隶属
    schoolType = scrapy.Field()  # 院校类型
    schoolLevel = scrapy.Field()  # 学历层次
    schoolSatis = scrapy.Field()  # 满意度


class SchoolSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
