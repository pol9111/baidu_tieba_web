from scheduler import run
from utils import logger

if __name__ == '__main__':

    run.delay()

    logger = logger()
    logger.info('完成循环')
    print('finish')