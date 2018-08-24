import redis

REDIS_CLIENT_DB5 = redis.Redis(host='192.168.1.4', port=6379, db=5)
url = 'https://tieba.baidu.com/f?kw=%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4&ie=utf-8&pn='

urls = []
for i in range(0, 10000, 50):
    each_page = url + str(i)
    # urls.append(each_page)
    REDIS_CLIENT_DB5.lpush('tieba2spider:stat_url', each_page)

# REDIS_CLIENT_DB5.lpush('tieba2spider:start_urls', urls)