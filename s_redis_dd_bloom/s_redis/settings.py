# -*- coding: utf-8 -*-

BOT_NAME = 's_redis'

SPIDER_MODULES = ['s_redis.spiders']
NEWSPIDER_MODULE = 's_redis.spiders'

ROBOTSTXT_OBEY = False

MONGO_URI = 'localhost'
MONGO_DATABASE = 'baidu'


REDIS_HOST = 'localhost'
# REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 5
}


# LOG_FILE = "s_redis.log"
# LOG_LEVEL = "INFO"


DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/4.0 (compatible; GoogleToolbar 6.1.1518.856; Windows 5.2; MSIE 8.0.6001.18702)',
}


# 去重类，要使用Bloom Filter请替换DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# 散列函数的个数，默认为6，可以自行修改
BLOOMFILTER_HASH_NUMBER = 6
# Bloom Filter的bit参数，默认30，占用128MB空间，去重量级1亿
BLOOMFILTER_BIT = 30

# 使用了scrapy_redis_bloomfilter里的调度器组件，不使用scrapy默认的调度器
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
# 使用队列形式
SCHEDULER_QUEUE_CLASS = "scrapy_redis_bloomfilter.queue.SpiderQueue"
# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True


ITEM_PIPELINES = {
   's_redis.pipelines.MongoPipeline': 300,
   'scrapy_redis.pipelines.RedisPipeline': 900,  # 数据保存到redis里
}

#DOWNLOADER_MIDDLEWARES = {
#    's_redis.middlewares.SRedisDownloaderMiddleware': 543,
#}


MAIL_HOST = "smtp.163.com"  # 发送邮件的服务器
MAIL_USER = "biscuit36@163.com"  # 用户名
MAIL_PASS = "fd83ra"  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
MAIL_PORT = 465
MAIL_SSL = True
MAIL_FROM = "biscuit36@163.com"  # 邮件发送者
MAIL_TO = "biscuit36@163.com"

TELNETCONSOLE_PORT = [9002]
