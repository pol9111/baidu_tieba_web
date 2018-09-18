from scheduler import Scheduler
from utils import logger

if __name__ == '__main__':

    run = Scheduler()
    run.multi_process()

    log = logger()
    log.info('完成循环')
    print('finish')


