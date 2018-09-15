import asyncio
from aiohttp import ClientSession
from config import *
import re

class Spider(object):
    async def fetch(self, sem, url, session):
        """下载器"""
        async with sem: # 限制最大操作
            async with session.get(url) as response: # 发送请求
                return await response.read() # 获取响应文件, 注意不是马上获取, 异步操作要加await
                                             # it just returns generator

    async def downloader(self, per_step_urls):
        """运行器, 执行下载"""
        task_list = []
        sem = asyncio.Semaphore(1024) # 设置最大操作
        # 创建可复用的 Session减少开销
        async with ClientSession() as session: # 创建会话
            for each in per_step_urls:
                url = each.decode()
                task = asyncio.ensure_future(self.fetch(sem, url, session)) # 每个预请求
                task_list.append(task)
            # 使用 gather(*tasks) 收集数据，wait(tasks) 不收集数据
            return await asyncio.gather(*task_list)

    async def parse(self, per_step_urls, loop):
        """页面解析"""
        html = await asyncio.gather(asyncio.ensure_future(self.downloader(per_step_urls)))
        result = [d for d in html[0] if d]  # 把单次一个跨度的请求放入列表
        for i in result:
            each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', i.decode('utf-8'))
            for each_one_content in each_page_content:
                try:
                    item = {}
                    item["id"] = re.findall(r'href="(/p/\d+)"', each_one_content)[0]
                    item['title'] = re.findall(r'class="j_th_tit ">(.*?)</a>', each_one_content)[0]
                    item['author'] = re.findall(r'title="主题作者: (.*?)"', each_one_content)[0]
                    item['create_time'] = re.findall(r'创建时间">(.*?)</span>', each_one_content)[0]
                    item['reply_num'] = re.findall(r'"回复">(\d+)</span>', each_one_content)[0]
                    item['last_reply'] = re.findall(r'title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>', each_one_content)[0]
                    item['content'] = re.findall(r'threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>', each_one_content)[0]
                    print(item)
                    await self.save_data(item)
                except:
                    pass

    async def save_data(self, items):
        """数据暂存到redis中"""
        REDIS_CLIENT.sadd('tiezi', items)









