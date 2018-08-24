# -*- coding: utf-8 -*-
import scrapy
import re
from s_redis.items import SRedisItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class TiebaSpider(CrawlSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    # redis_key = "tiebaspider:start_urls"
    start_urls = ['https://tieba.baidu.com/f?kw=%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4&ie=utf-8&pn=50']

    rules = (
       Rule(LinkExtractor(allow=r'pn=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        each_page = response.xpath('//li[@class=" j_thread_list clearfix"]')

        for tiezi in each_page:
            item = SRedisItem()
            item['id'] = tiezi.xpath('./div/div[2]/div[1]/div[1]/a/@href').extract_first(default='N/A')
            item['title'] = tiezi.xpath('.//div[@class="threadlist_lz clearfix"]/div/a/text()').extract_first(default='N/A')
            item['author'] = tiezi.xpath('.//span[@class="tb_icon_author "]/@title|//span[@class="tb_icon_author no_icon_author"]/@title').re('主题作者:\s(.*)')[0]
            item['create_time'] = tiezi.xpath('.//span[@class="pull-right is_show_create_time"]/text()').extract_first(default='N/A')
            item['reply_num'] = tiezi.xpath('.//span[@class="threadlist_rep_num center_text"]/text()').extract_first(default='N/A')
            item['last_reply'] = tiezi.xpath('.//span[@class="threadlist_reply_date pull_right j_reply_data"]/text()').re('\r\n\s*(\d+:\d+|\d+-\d+)\s*')[0]
            content = tiezi.xpath('./div/div[2]/div[2]/div[1]/div/text()').extract_first(default='N/A')
            item['content'] = re.sub('[\n\t\r\s]', '', content)
            yield item
