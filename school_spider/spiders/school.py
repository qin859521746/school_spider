# -*- coding: utf-8 -*-
import scrapy
from school_spider.items import schoolItem
from school_spider.items import majorItem


class SchoolSpider(scrapy.Spider):
    name = 'school'
    start_urls = ['https://gaokao.chsi.com.cn']
    offset = 0

    def parse(self, response):
        # 院校库
        school_url = self.start_urls[0] + \
                     response.xpath('//li[@class="nav-cx clearfix"]/ul[@class="nav-td clearfix"]/li['
                                    '1]/a/@href').extract()[0]
        # 专业库
        major_url = self.start_urls[0] + \
                    response.xpath('//li[@class="nav-ss clearfix"]/ul[@class="nav-td clearfix"]/li['
                                   '1]/a/@href').extract()[0]
        yield scrapy.Request(
            url=major_url,
            callback=self.First_major_parse
        )
        while self.offset<=2720:
            self.offset += 20
            school_url=school_url+ 'search--ss-on,searchType-1,option-qg,start-' + str(self.offset) + '.dhtml'
            yield scrapy.Request(
                url=school_url,
                callback=self.school_parse
            )


    def First_major_parse(self, response):
        # 高职专业
        gaozhi_major_url = self.start_urls[0] + response.xpath(
            '//div[@class="ch-alert ch-alert-info zyk-info"]/a/@href'
        ).extract()[0]
        # 本科专业
        benke_major_url = self.start_urls[0] + response.xpath(
            '//div[@class="ch-alert ch-alert-info zyk-info"]/a/@href'
        ).extract()[1]
        yield scrapy.Request(
            url=benke_major_url,
            callback=self.benke_major_parse
        )

    def benke_major_parse(self, response):
        left_majors = response.xpath(
            '//div[@class="zyk-zydm-ml clearfix"]/div[@class="left"]/table[@class="ch-table"]//tr'
        )
        right_majors=response.xpath(
            '//div[@class="zyk-zydm-ml clearfix"]/div[@class="right"]/table[@class="ch-table"]//tr'
        )
        majors=left_majors[1:]+right_majors[1:]
        for each in majors:
            item = majorItem()
            majorID = each.xpath('td[1]/strong/text()').extract()
            majorName = each.xpath('td[2]/strong/text()').extract()
            if len(majorID) == 0:
                majorID = each.xpath('td[1]/text()').extract()
                majorName = each.xpath('td[2]/text()').extract()
            item['majorID'] = majorID[0]
            item['majorName'] = majorName[0]
            yield item

    def school_parse(self, response):
        school_html = response.xpath(
            '//div[@class="yxk-table"]/table[@class="ch-table"]//tr'
        )
        for each in school_html[1:]:
            item = schoolItem()
            item['schoolName'] = each.xpath('td[1]/a/text()').extract()[0].replace('\r', '').strip()
            item['schoolLocation'] = each.xpath('td[2]/text()').extract()[0].replace('\r', '').strip()
            item['schoolBeto'] = each.xpath('td[3]/text()').extract()[0].replace('\r', '').strip()
            item['schoolType'] = each.xpath('td[4]/text()').extract()[0].replace('\r', '').strip()
            item['schoolLevel'] = each.xpath('td[5]/text()').extract()[0].strip()
            try:
                item['schoolSatis'] = each.xpath('td[8]/a/text()').extract()[0]
            except:
                item['schoolSatis'] = '--'
            yield item
