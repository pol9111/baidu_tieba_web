import asyncio
from config import LOOP_NUM
from saver import Saver
from tasker import Tasker
from utils import run_time, logger

@run_time
def run():
    # 协程池
    loop = asyncio.get_event_loop()

    tasker = Tasker()
    each_task = tasker.get_task()

    # LOOP_NUM: 每个任务循环几次, 避免Semaphore量太大
    for i in range(LOOP_NUM):
        # 每次循环的urls
        per_step_urls = tasker.get_urls(each_task)
        # 待处理
        tasks = tasker.create_task(i, per_step_urls, loop)
        # 启动
        loop.run_until_complete(asyncio.gather(*tasks))

    # # 保存数据到mongodb
    # saver = Saver()
    # saver.run()

    loop.close()

if __name__ == '__main__':

    run()

    log = logger()
    log.info('完成循环')
    print('finish')






















