from spider import tieba
import asyncio

def tieba_task(index, per_step_urls, proxies):
    """创建异步任务"""
    print('开始下一循环:', index)
    _tasks = [
        asyncio.ensure_future(tieba.parse(per_step_urls, proxies))  # 每次指定一个跨度
    ]
    return _tasks






