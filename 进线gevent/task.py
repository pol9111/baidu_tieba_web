from config import *

class Task:
    def __init__(self):
        self.redis_client = REDIS_CLIENT_DB2
        self.start_page = START_PAGE
        self.stop_page = STOP_PAGE
        self.start_per_step = START_PER_STEP
        self.stop_per_step = STOP_PER_STEP

    def get_task(self):
        """获取任务"""
        url_list = []
        for i in range(self.start_page, self.stop_page):
            single_task = self.redis_client.lpop('urls')
            url_list.append(single_task)
        return url_list

    def get_urls(self, urls):
        """获取每次循环的url列表"""
        per_step_urls = []
        for each in range(self.start_per_step, self.stop_per_step):
            each_page_url = urls[each]
            per_step_urls.append(each_page_url)
        return per_step_urls

