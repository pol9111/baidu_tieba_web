import logging
import os
import time

def logger():
    # 创建一个logger
    log = logging.getLogger()

    # Log等级总开关
    log.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    write_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = write_time + '.log'
    write_log = logging.FileHandler(log_name, mode='a')
    write_log.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    write_log.setFormatter(formatter)

    # 将logger添加到handler里面
    log.addHandler(write_log)
    return log



