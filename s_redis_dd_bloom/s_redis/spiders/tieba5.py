# -*- coding: utf-8 -*-
import scrapy
from s_redis.items import SRedisItem
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule



class Tieba3Spider(RedisSpider):
    name = 'tieba5'
    allowed_domains = ['tieba.baidu.com']
    redis_key = "tieba5spider:start_urls"


    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, callback=self.parse)


    def parse(self, response):

        each_page = response.xpath('//li[@class=" j_thread_list clearfix"]')

        for tiezi in each_page:
            item = SRedisItem()
            item['id'] = tiezi.xpath('./div/div[2]/div[1]/div[1]/a/@href').extract_first(default='N/A')
            item['title'] = tiezi.xpath('.//div[@class="threadlist_lz clearfix"]/div/a/text()').extract_first(default='N/A')
            item['author'] = tiezi.xpath('.//span[@class="tb_icon_author "]/@title|//span[@class="tb_icon_author no_icon_author"]/@title').re_first('主题作者:\s(.*)')
            item['create_time'] = tiezi.xpath('.//span[@class="pull-right is_show_create_time"]/text()').extract_first(default='N/A')
            item['reply_num'] = tiezi.xpath('.//span[@class="threadlist_rep_num center_text"]/text()').extract_first(default='N/A')
            item['last_reply'] = tiezi.xpath('.//span[@class="threadlist_reply_date pull_right j_reply_data"]/text()').re_first('\r\n\s*(\d+:\d+|\d+-\d+)\s*')
            item['content'] = tiezi.xpath('./div/div[2]/div[2]/div[1]/div/text()').extract_first(default='N/A').strip()
            # content = tiezi.xpath('./div/div[2]/div[2]/div[1]/div/text()').extract_first(default='N/A')
            # item['content'] = re.sub('[\n\t\r\s]', '', content)

            yield item
