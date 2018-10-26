import aiohttp
import asyncio
import random
from config import HEADERS, REDIS_CLIENT_DB2, RETRY_TABLE1


class TiebaSpider(object):

    def __init__(self):
        self.headers = HEADERS
        self.redis_client_db2 = REDIS_CLIENT_DB2
        self.retry_table1 = RETRY_TABLE1

    async def fetch(self, sem, url, session):
        """下载器"""
        # proxy = 'http://' + random.choice(proxies) or None
        async with sem: # 限制最大操作
            try:
                async with session.get(url, headers=self.headers, timeout=15) as response: # 发送请求
                    if response.status == 200:
                        return await response.read() # 获取响应文件, 注意不是马上获取, 异步操作要加await
                    else:
                        print('响应错误:', url)
                        self.redis_client_db2.sadd(self.retry_table1, url)
            except (aiohttp.ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                print('请求失败!!', url)
                self.redis_client_db2.sadd(self.retry_table1, url)

    async def downloader(self, per_step_urls):
        """运行器, 执行下载"""
        task_list = []
        sem = asyncio.Semaphore(1024) # 设置最大操作
        async with aiohttp.ClientSession() as session:
            for each in per_step_urls:
                try:
                    url = each.decode()
                    tasks = asyncio.ensure_future(self.fetch(sem, url, session))  # 每个预请求
                    task_list.append(tasks)
                except Exception:
                    pass
            return await asyncio.gather(*task_list) # 每个循环请求总数 gather返回列表