# -*- coding: utf-8 -*-

from scrapy.conf import settings
import pymongo

class MongoPipeline(object):

    def __init__(self):
        self.mongo_uri = settings['MONGO_URI']
        self.mongo_db = settings['MONGO_DATABASE']

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db['tiezi_s_redis'].insert(dict(item))