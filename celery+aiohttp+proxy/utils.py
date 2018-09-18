import logging
import os
import time
from datetime import datetime
from config import PROXY_URL
from tools.Proxy import FreeProxy


def logger():
    # 创建一个logger
    log = logging.getLogger()

    # Log等级总开关
    log.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    write_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = 'log\\' + write_time + '.log'
    write_log = logging.FileHandler(log_name, mode='a')
    write_log.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    write_log.setFormatter(formatter)

    # 将logger添加到handler里面
    log.addHandler(write_log)
    return log

def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()

        func(*args, **kwargs)

        end_time = datetime.now()
        total_time = end_time - start_time
        print(total_time)
    return new_func

def get_proxies():
    proxy_worker = FreeProxy()
    proxy_worker.run(PROXY_URL)
    proxies = proxy_worker.proxies
    return proxies

