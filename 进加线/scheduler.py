from spider import Spider
from saver import Saver
from concurrent import futures
from tasker import Task
from config import LOOP_NUM
from utils import run_time
import multiprocessing


# TODO: 增量爬取, 测试代理失败重试

class Scheduler:

    def multi_thread(self):
        # 获取任务
        task = Task()
        url_list = task.get_task()

        # 爬取数据
        spider = Spider()
        for i in range(LOOP_NUM):
            print('开始下一循环', end='\n'*3)
            per_step_urls = task.get_urls(url_list)
            with futures.ThreadPoolExecutor(64) as executor:
                executor.map(spider.get_resp, per_step_urls)

        # # 保存数据
        # saver = Saver()
        # saver.run()

    @run_time
    def multi_process(self):
        process = []
        # num_cpus = multiprocessing.cpu_count()
        for i in range(1):  # 以核心数为主, 用cpu_count反而更慢
            p = multiprocessing.Process(target=self.multi_thread)
            p.start()
            process.append(p)
        for p in process:
            p.join()







