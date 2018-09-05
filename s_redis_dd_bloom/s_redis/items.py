# -*- coding: utf-8 -*-

import scrapy

class SRedisItem(scrapy.Item):
    table = 'tiezi_s_redis'
    title = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    reply_num = scrapy.Field()
    last_reply = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()

