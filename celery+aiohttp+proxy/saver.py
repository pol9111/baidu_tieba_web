from config import REDIS_CLIENT, MONGO_TABLE
from utils import LogHandler

class Saver(object):

    def __init__(self):
        self.item_list = []
        self.redis_client = REDIS_CLIENT
        self.mongo_table = MONGO_TABLE
        self.log_handler = LogHandler

    def get_item(self):
        """从redis中获取数据"""
        redis_num = self.redis_client.scard('tiezi')
        if redis_num:
            for i in range(redis_num):
                try:
                    item_ = self.redis_client.spop('tiezi').decode('utf-8')
                    item = eval(item_)
                    self.item_list.append(item)
                except Exception as e:
                    self.log_handler.logger().error('导出redis失败'+str(e))
                    print(e)
                    pass

    def save_item(self):
        """存入mongodb硬盘"""
        if self.item_list:
            self.mongo_table.insert_many(self.item_list)
            print('已存入mongoDB')

    def run(self):
        self.get_item()
        self.save_item()