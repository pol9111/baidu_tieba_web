import pymongo
import redis

# 请求构造参数
KW = '炉石传说' # 要爬取的贴吧
URL = 'https://tieba.baidu.com'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
# PROXIES = { "https":"https://111.90.145.111:3128"}

# 数据库配置
MONGO_URL = pymongo.MongoClient('localhost')
MONGO_DB = MONGO_URL['baidu']
MONGO_TABLE = MONGO_DB['tiezi']

# 连接redis
REDIS_CLIENT = redis.Redis(host='127.0.0.1', port=6379, db=6)
REDIS_CLIENT_DB2 = redis.Redis(host='127.0.0.1', port=6379, db=7)

# 任务配置   LOOP_NUM * STOP_PER_STEP == STOP_PAGE
START_PAGE = 0
STOP_PAGE = 1000
START_PER_STEP = 0
STOP_PER_STEP = 500 # STOP_PER_STEP次数越大存硬盘的次数越少  但占内存空间越大
LOOP_NUM = 5 # loop循环次数越少读存硬盘的次数越少


