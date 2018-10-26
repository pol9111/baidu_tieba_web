import aiohttp
import asyncio


class FreeProxy:

    def __init__(self):
        self.proxies = []

    async def fetch(self, sem, url, session):
        """下载器"""
        async with sem:
            async with session.get(url, timeout=10) as response:
                return await response.text()

    async def downloader(self, urls):
        """运行器, 执行下载"""
        task_list = []
        sem = asyncio.Semaphore(1024)
        async with aiohttp.ClientSession() as session:
            for url in urls:
                tasks = asyncio.ensure_future(self.fetch(sem, url, session))
                task_list.append(tasks)
            ips = await asyncio.gather(*task_list)
            await self.save_proxy(ips)

    async def save_proxy(self, ips):
        for ip in ips:
            self.proxies.append(ip)
        self.proxies = list(set(self.proxies))
        # return self.proxies

    def run(self, url):
        loop = asyncio.get_event_loop()
        urls = [url for i in range(100)]
        tasks = [self.downloader(urls)]
        loop.run_until_complete(asyncio.gather(*tasks))



# # Manual
# proxy_worker = FreeProxy()
# proxy_worker.run(PROXY_URL)
# print(proxy_worker.proxies)

# def get_proxies():
#     proxy_worker = FreeProxy()
#     proxy_worker.run(PROXY_URL)
#     proxies = proxy_worker.proxies
#     return proxies

