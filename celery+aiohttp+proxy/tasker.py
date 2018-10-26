from config import REDIS_CLIENT_DB2, RETRY_TABLE1, STOP_PAGE, START_PAGE, START_PER_STEP, STOP_PER_STEP, NODE


class Tasker(object):

    def __init__(self):
        self.retry_tasks = []
        self.redis_client_db2 = REDIS_CLIENT_DB2
        self.retry_table1 = RETRY_TABLE1
        self.stop_page = STOP_PAGE
        self.start_page = START_PAGE
        self.start_per_step = START_PER_STEP
        self.stop_per_step = STOP_PER_STEP

    def check_retries(self):
        if self.redis_client_db2.scard(self.retry_table1):
            return True
        else:
            return False

    def get_task(self):
        """获取任务"""
        url_list = []
        for i in range(self.start_page, self.stop_page):
            single_task = self.redis_client_db2.lpop('urls')
            url_list.append(single_task)
        return url_list

    def get_perloop(self,urls):
        """获取每次循环的url列表"""
        per_step_urls = []
        for each in range(self.start_per_step, self.stop_per_step):
            each_page_url = urls.pop()
            per_step_urls.append(each_page_url)
        return per_step_urls

    def get_retry_task(self):
        """获取每次重试任务"""
        retry_num = self.redis_client_db2.scard(self.retry_table1)
        for i in range(retry_num+1):
            url = self.redis_client_db2.spop(self.retry_table1)
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