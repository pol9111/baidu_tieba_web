import asyncio
from config import LOOP_NUM
from saver import Saver
from tasker import Tasker
from utils import run_time, get_proxies, logger
from workers import app
from tasks import tieba_task

tasker = Tasker()

def retry(loop):

    per_step_urls_list = tasker.get_perloop_retry(tasker.get_retry_task)

    proxies = get_proxies()

    for per_step_urls in per_step_urls_list:
        # 待处理
        tasks = tieba_task('retry', per_step_urls, proxies)
        # 启动
        loop.run_until_complete(asyncio.gather(*tasks))

    # # 保存数据到mongodb
    # saver = Saver()
    # saver.run()

    if tasker.check_retries:
        retry(loop)

    else:
        loop.close()
        log = logger()
        log.info('完成循环')
        print('Finish!!')



@app.task
@run_time
def run():

    loop = asyncio.get_event_loop()

    proxies = get_proxies()

    # LOOP_NUM: 每个任务循环几次, 避免Semaphore量太大
    for index in range(LOOP_NUM):
        # 每次循环的urls
        per_step_urls = tasker.get_perloop(tasker.get_task)
        # 待处理
        tasks = tieba_task(index, per_step_urls, proxies)
        # 启动
        loop.run_until_complete(asyncio.gather(*tasks))

    # # 保存数据到mongodb
    # saver = Saver()
    # saver.run()

    if tasker.check_retries:
        retry(loop)

    else:
        loop.close()
        log = logger()
        log.info('完成循环')
        print('Finish!!')




















