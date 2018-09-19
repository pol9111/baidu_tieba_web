import asyncio
from config import LOOP_NUM
from saver import Saver
from tasker import Tasker
from utils import run_time, Proxy, Log
from workers import app
from tasks import tieba_task



def retry(loop):

    #已经分片好的每次重试的url列表
    per_step_urls_list = Tasker().get_perloop_retry()

    proxies = Proxy.get_proxies()

    for per_step_urls in per_step_urls_list:
        # 待处理
        tasks = tieba_task('retry', per_step_urls, proxies)
        # 启动
        loop.run_until_complete(asyncio.gather(*tasks))

    # 保存数据到mongodb
    Saver().run()

    if Tasker.check_retries():
        retry(loop)

    else:
        loop.close()
        Log.logger().info('完成循环')
        print('Finish!!')



@app.task
@run_time
def run():

    loop = asyncio.get_event_loop()

    proxies = Proxy.get_proxies()

    # 每次所有任务
    one_task = Tasker.get_task()

    # LOOP_NUM: 每个任务循环几次, 避免Semaphore量太大
    for index in range(LOOP_NUM):
        # 每次循环的urls
        per_step_urls = Tasker.get_perloop(one_task)
        # 待处理
        tasks = tieba_task(index, per_step_urls, proxies)
        # 启动
        loop.run_until_complete(asyncio.gather(*tasks))

    # 保存数据到mongodb
    Saver().run()

    if Tasker.check_retries():
        retry(loop)

    else:
        loop.close()
        Log.logger().info('完成循环')
        print('Finish!!')




















