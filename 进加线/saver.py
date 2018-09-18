from config import *
from utils import logger

class Saver:

    def __init__(self):
        self.redis_client = REDIS_CLIENT
        self.mongo_table = MONGO_TABLE
        self.item_list = []
        self.logger = logger()

    def get_item(self):
        """从内存中获取数据"""
        redis_num = self.redis_client.scard('tiezi')
        if redis_num >= MAX_NUMBER:
            for i in range(redis_num):
                try:
                    cmp = self.redis_client.spop('tiezi').decode('utf-8')
                    item = eval(cmp)
                    self.item_list.append(item)
                except Exception as e:
                    self.logger.error('导出redis失败'+str(e))
                    print(e)
                    pass

    def push_item(self, item):
        """存入mongodb硬盘"""
        self.mongo_table.insert_many(item)
        print('已存入mongoDB')


    def run(self):
        self.get_item()
        self.push_item(self.item_list)




