from config import *


class Tasker:

    def __init__(self):
        self.redis_client = REDIS_CLIENT_DB2

    @property
    def check_retries(self):
        if self.redis_client.scard(RETRY_TABLE1):
            return True
        else:
            return False

    @property
    def get_task(self):
        """获取任务"""
        url_list = []
        for i in range(START_PAGE, STOP_PAGE):
            single_task = self.redis_client.lpop('urls')
            url_list.append(single_task)
        return url_list

    def get_perloop(self, urls):
        """获取每次循环的url列表"""
        per_step_urls = []
        for each in range(START_PER_STEP, STOP_PER_STEP):
            each_page_url = urls.pop()
            per_step_urls.append(each_page_url)
        return per_step_urls

    @property
    def get_retry_task(self):
        """获取每次重试任务"""
        retry_num = self.redis_client.scard(RETRY_TABLE1)
        retry_tasks = []
        for i in range(retry_num+1):
            url = self.redis_client.spop(RETRY_TABLE1)
            retry_tasks.append(url)
        return retry_tasks

    def get_perloop_retry(self, urls):
        """获取每次重试循环的url列表"""
        max_num = len(urls)
        retry_list = []
        if max_num > 50:
            per_step = max_num // 2
            retry_list.append(urls[:per_step])
            retry_list.append(urls[:-1])
            return retry_list
        else:
            retry_list = [urls]
            return retry_list

