from spider import Spider
from saver import Saver
from task import Task
from config import LOOP_NUM
import time
from utils import logger
import multiprocessing
from datetime import datetime
from workers import app

# TODO: 定时任务, 增量爬取, 分布式

logger = logger()


@app.task
def run():
    start_time = time.time()

    # 获取任务
    task = Task()
    url_list = task.get_task()

    # 爬取数据
    for i in range(LOOP_NUM):
        per_step_urls = task.get_urls(url_list)
        print('开始下一循环', end='\n' * 3)
        spider = Spider()
        spider.async_req(per_step_urls)

        # 保存数据
        # saver = Saver()
        # saver.run()


    logger.info('完成循环')
    print('finish')

    total_time = time.time() - start_time
    print(total_time)
    logger.info('结束时间: {}'.format(datetime.now()))
    logger.info('总共费时: {}'.format(total_time))



