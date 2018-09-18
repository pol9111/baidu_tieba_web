import pymongo
import motor.motor_asyncio

# 请求构造参数
KW = '炉石传说' # 要爬取的贴吧
URL = 'https://tieba.baidu.com'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
PROXIES = { "http":"109.172.160.93:53281"}

# 数据库配置
MONGO_URL = 'localhost'
MONGO_DB = 'baidu'
MONGO_TABLE = 'tieba_tiezi'

# 连接数据库
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, 27017)
db = client[MONGO_DB]
table = db[MONGO_TABLE]




