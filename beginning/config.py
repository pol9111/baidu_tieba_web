import pymongo

# 请求构造参数
KW = '炉石传说' # 要爬取的贴吧
URL = 'https://tieba.baidu.com'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
PROXIES = { "http":"111.90.145.111:3128"}

# 数据库配置
MONGO_URL = 'localhost'
MONGO_DB = 'baidu'
MONGO_TABLE = 'tieba_tiezi'

# 连接数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
table = db[MONGO_TABLE]




