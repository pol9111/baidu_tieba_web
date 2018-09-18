import asyncio
from aiohttp import ClientSession
from config import *
import re
from utils import logger
import random

class Spider(object):
    async def fetch(self, sem, url, session):
        """下载器"""
        async with sem: # 限制最大操作
            async with session.get(url, headers=HEADERS, timeout=10) as response: # 发送请求
                # await asyncio.sleep(random.random())
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
                tasks = asyncio.ensure_future(self.fetch(sem, url, session)) # 每个预请求
                task_list.append(tasks)
            # 使用 gather(*tasks) 收集数据，wait(tasks) 不收集数据
            return await asyncio.gather(*task_list) # 每个循环请求总数
                                                    # gather返回列表
    async def parse(self, per_step_urls):
        """页面解析"""
        tasks = await self.downloader(per_step_urls)
        for html in tasks: # 每个任务总数, 上面总共一个任务, task[0]才是每个循环的所有响应文件
            each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', html.decode())
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
                except Exception as e:
                    log = logger()
                    log.error('页面解析失败' + str(e))
                    print(e)
                    pass

    async def save_data(self, items):
        """数据暂存到redis中"""
        REDIS_CLIENT.sadd('tiezi', items)









