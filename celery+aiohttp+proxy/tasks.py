from crawler.tieba import TiebaCrawler
import asyncio


def tieba_task(index, per_step_urls):
    """创建异步任务"""
    print('开始下一循环:', index)
    tieba_crawler = TiebaCrawler()
    _tasks = [
        asyncio.ensure_future(tieba_crawler.start_requests(per_step_urls))  # 每次指定一个跨度
    ]
    return _tasks