import pymongo
import motor.motor_asyncio
import redis

# 请求构造参数
KW = '炉石传说' # 要爬取的贴吧
URL = 'https://tieba.baidu.com'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
PROXIES = { "http":"109.172.160.93:53281"}

# 连接mongodb
MONGO_CLIENT = pymongo.MongoClient('127.0.0.1', 27017)
MONGO_DB = MONGO_CLIENT['baidu']
MONGO_TABLE = MONGO_DB['tiezi']

# 连接redis
REDIS_CLIENT = redis.Redis(host='127.0.0.1', port=6379, db=7)
REDIS_CLIENT_DB2 = redis.Redis(host='127.0.0.1', port=6379, db=6)
MAX_NUMBER = 2000 # redis内最大数据量

# 任务配置   LOOP_NUM * STOP_PER_STEP == STOP_PAGE 几个进程就乘于几倍 250是50000个帖子
START_PAGE = 0
STOP_PAGE = 250
START_PER_STEP = 0
STOP_PER_STEP = 50 # STOP_PER_STEP次数越大存硬盘的次数越少  但占内存空间越大
LOOP_NUM = 5 # loop循环次数越少读存硬盘的次数越少

# celery配置
BROKER = 'redis://127.0.0.1:6379/4'
BACKEND = 'redis://127.0.0.1:6379/5'