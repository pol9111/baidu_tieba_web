from config import *


def create_urls():
    """创建url列表"""
    urls = []
    for num in range(0, 100000, 50):
        # each_page_url = URL + '/f?kw={}&ie=utf-8&pn='.format(KW) + str(each)
        REDIS_CLIENT_DB2.rpush('urls', num)


if __name__ == '__main__':
    create_urls()
    print('finish')

