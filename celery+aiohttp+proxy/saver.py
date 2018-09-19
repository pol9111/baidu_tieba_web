from config import REDIS_CLIENT, MONGO_TABLE
from utils import Log

class Saver:

    def __init__(self):
        self.item_list = []

    def get_item(self):
        """从redis中获取数据"""
        redis_num = REDIS_CLIENT.scard('tiezi')
        if redis_num:
            for i in range(redis_num):
                try:
                    item_ = REDIS_CLIENT.spop('tiezi').decode('utf-8')
                    item = eval(item_)
                    self.item_list.append(item)
                except Exception as e:
                    Log.logger().error('导出redis失败'+str(e))
                    print(e)
                    pass

    def save_item(self):
        """存入mongodb硬盘"""
        if self.item_list:
            MONGO_TABLE.insert_many(self.item_list)
            print('已存入mongoDB')

    def run(self):
        self.get_item()
        self.save_item()


