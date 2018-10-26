import random
import pymongo
import redis
from tools.UserAgent import USERAGENT

KW = '炉石传说' # 要爬取的贴吧
URL = 'https://tieba.baidu.com'
HEADERS = {'UserAgent': random.choice(USERAGENT)}

# 连接mongodb
MONGO_CLIENT = pymongo.MongoClient('127.0.0.1', 27017)
MONGO_DB = MONGO_CLIENT['baidu']
MONGO_TABLE = MONGO_DB['tiezi']

# 连接redis
REDIS_CLIENT = redis.StrictRedis(host='127.0.0.1', port=6379, db=7)
REDIS_CLIENT_DB2 = redis.StrictRedis(host='127.0.0.1', port=6379, db=6)
MAX_NUMBER = 2500 # redis内最大数据量
RETRY_TABLE1 = 'retry1' # 失败重试表
NODE = 2 # 重试列表要分成几段循环

# 任务配置   LOOP_NUM * STOP_PER_STEP == STOP_PAGE 几个进程就乘于几倍 250是50000个帖子
START_PAGE = 0
STOP_PAGE = 250
START_PER_STEP = 0
STOP_PER_STEP = 50 # STOP_PER_STEP次数越大存硬盘的次数越少  但占内存空间越大
LOOP_NUM = 5 # loop循环次数越少读存硬盘的次数越少

# celery配置
BROKER = 'redis://127.0.0.1:6379/4'
BACKEND = 'redis://127.0.0.1:6379/5'

# Proxy-url
PROXY_URL = 'http://47.75.52.39:5555/random'