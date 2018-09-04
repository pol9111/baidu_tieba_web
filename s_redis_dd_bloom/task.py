import redis

REDIS_CLIENT_DB5 = redis.Redis(host='localhost', port=6379, db=5)
url = 'https://tieba.baidu.com/f?kw=%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4&ie=utf-8&pn='

urls = []
for i in range(0, 2000000, 50):
    each_page = url + str(i)
    urls.append(each_page)
    # REDIS_CLIENT_DB5.rpush('tieba2spider:stat_url', each_page)


REDIS_CLIENT_DB5.lpush('tieba5spider:start_urls', urls)
print('finish')

