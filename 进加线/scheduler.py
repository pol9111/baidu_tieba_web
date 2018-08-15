from spider import Spider
from saver import Saver
from concurrent import futures
from task import Task
from config import LOOP_NUM
import time
from utils import logger
import multiprocessing


# TODO: Scheduler多进程, 日志, 定时任务, 爬取队列, spider一个跨度一个跨度的爬, 增量爬取, 分布式


def run():
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

        # 保存数据
        saver = Saver()
        saver.run()



if __name__ == '__main__':
    start_time = time.time()

    process = []
    # num_cpus = multiprocessing.cpu_count()
    for i in range(4):
        p = multiprocessing.Process(target=run)
        p.start()
        process.append(p)
    for p in process:
        p.join()


    logger = logger()
    logger.info('完成循环')
    print('finish')


    total_time = time.time() - start_time
    print(total_time)

