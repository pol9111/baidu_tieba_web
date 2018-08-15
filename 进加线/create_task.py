from config import *


def create_urls():
    """创建url列表"""
    urls = []
    for each in range(0, 2500000, 50):
        each_page_url = URL + '/f?kw={}&ie=utf-8&pn='.format(KW) + str(each)
        REDIS_CLIENT_DB2.rpush('urls', each_page_url)


if __name__ == '__main__':
    create_urls()
    print('finish')

