# -*- coding: utf-8 -*-
import re
from scrapy.conf import settings
from s_redis.items import SRedisItem
from scrapy_redis.spiders import RedisSpider
from scrapy.mail import MailSender
import scrapy
from scrapy import Spider

class Tieba2Spider(Spider):
    name = 'tieba2'
    allowed_domains = ['tieba.baidu.com']
    # redis_key = "tieba2spider:start_urls"
    # url_1 = 'https://tieba.baidu.com/f?kw=%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4&ie=utf-8&pn=50'
    start_urls = ['https://tieba.baidu.com/f?kw=%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4&ie=utf-8&pn=50']

    # 自己给数据库队列
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)


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
            content = tiezi.xpath('./div/div[2]/div[2]/div[1]/div/text()').extract_first(default='N/A')
            item['content'] = re.sub('[\n\t\r\s]', '', content)
            yield item


    def closed(self, reason):
        mailer = MailSender.from_settings(settings)
        subject = 'qwe'
        body = 'asd'
        try:
            mailer.send(to=[settings['MAIL_TO']], subject=subject, body=body, mimetype='text/plain')
            print('邮件发送成功')
        except Exception:
            print('邮件发送失败')

