from config import *


class Tasker:

    def __init__(self):
        self.retry_tasks = []

    @staticmethod
    def check_retries():
        if REDIS_CLIENT_DB2.scard(RETRY_TABLE1):
            return True
        else:
            return False

    @staticmethod
    def get_task():
        """获取任务"""
        url_list = []
        for i in range(START_PAGE, STOP_PAGE):
            single_task = REDIS_CLIENT_DB2.lpop('urls')
            url_list.append(single_task)
        return url_list

    @staticmethod
    def get_perloop(urls):
        """获取每次循环的url列表"""
        per_step_urls = []
        for each in range(START_PER_STEP, STOP_PER_STEP):
            each_page_url = urls.pop()
            per_step_urls.append(each_page_url)
        return per_step_urls

    def get_retry_task(self):
        """获取每次重试任务"""
        retry_num = REDIS_CLIENT_DB2.scard(RETRY_TABLE1)
        for i in range(retry_num+1):
            url = REDIS_CLIENT_DB2.spop(RETRY_TABLE1)
            self.retry_tasks.append(url)
        # return cls.retry_tasks

    def get_perloop_retry(self):
        """获取每次重试循环的url列表"""
        self.get_retry_task()
        max_num = len(self.retry_tasks)
        if max_num > 100:
            retry_list = [self.retry_tasks[i:i + max_num//NODE] for i in range(0, max_num, max_num//NODE)]
            return retry_list
        else:
            retry_list = [self.retry_tasks]
            return retry_list

