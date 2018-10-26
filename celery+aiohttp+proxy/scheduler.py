import asyncio
from config import LOOP_NUM
from saver import Saver
from tasker import Tasker
from utils import run_time, ProxyHandler, LogHandler
from workers import app
from tasks import tieba_task


class Scheduler(object):

    def __init__(self):
        # self.proxy_handler = ProxyHandler
        self.tasker = Tasker()
        self.saver = Saver()
        self.log_handler = LogHandler()
        self.tieba_task = tieba_task
        self.loop_num = LOOP_NUM

    def end_task(self, loop):
        # 保存数据到mongodb
        self.saver.run()
        if self.tasker.check_retries():
            self.retry_task(loop)
        else:
            loop.close()
            self.log_handler.logger().info('完成循环')
            print('Finish!!')

    def retry_task(self, loop):
        #已经分片好的每次重试的url列表
        per_step_urls_list = self.tasker.get_perloop_retry()
        for per_step_urls in per_step_urls_list:
            # 待处理
            tasks = tieba_task('retry', per_step_urls)
            # 启动
            loop.run_until_complete(asyncio.gather(*tasks))
        self.end_task(loop)


    # @run_time
    def start_task(self):
        loop = asyncio.get_event_loop()
        # 每次所有任务
        one_task = self.tasker.get_task()
        # self.loop_num: 每个任务循环几次, 避免Semaphore量太大
        for index in range(self.loop_num):
            # 每次循环的urls
            per_step_urls = self.tasker.get_perloop(one_task)
            # 待处理
            tasks = tieba_task(index, per_step_urls)
            # 启动
            loop.run_until_complete(asyncio.gather(*tasks))
        self.end_task(loop)


@app.task
def start_tieba_clawer():
    s = Scheduler()
    s.start_task()