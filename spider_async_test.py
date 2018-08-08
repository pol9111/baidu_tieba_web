import asyncio
from aiohttp import ClientSession
from async_config import *
import time
import re

start_time = time.time()


# 下载器
async def fetch(sem, url, session):
    async with sem: # 限制最大操作
        async with session.get(url) as response: # 发送请求
            return await response.read() # 获取响应文件, 注意不是马上获取, 异步操作要加await
                                         # it just returns generator
# 运行器
async def run(start, stop):
    """获取url列表"""
    url_list = []
    sem = asyncio.Semaphore(1024) # 设置最大操作
    # 创建可复用的 Session，减少开销
    async with ClientSession() as session: # 创建会话
        for each in range(start, stop, 50):
            each_page_url = URL + '/f?kw={}&ie=utf-8&pn='.format(KW) + str(each)
            task = asyncio.ensure_future(fetch(sem, each_page_url, session)) # 每个预请求
            url_list.append(task)
        # 使用 gather(*tasks) 收集数据，wait(tasks) 不收集数据
        return await asyncio.gather(*url_list)


# 页面解析, 并保存到数据库
async def save_to_database(start, stop):
    html = await asyncio.gather(asyncio.ensure_future(run(start, stop)))
    # print('单次解析数量:',len(html))
    result = [d for d in html[0] if d] # 把单次一个跨度的请求放入列表
    # print('rs长度',len(result))
    for i in result:
        each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', i.decode('utf-8'))
        for each_one_content in each_page_content:
            try:
                item = {}
                item['title'] = re.findall(r'class="j_th_tit ">(.*?)</a>', each_one_content)[0]
                item['author'] = re.findall(r'title="主题作者: (.*?)"', each_one_content)[0]
                item['create_time'] = re.findall(r'创建时间">(.*?)</span>', each_one_content)[0]
                item['reply_num'] = re.findall(r'"回复">(\d+)</span>', each_one_content)[0]
                item['last_reply'] = \
                re.findall(r'title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>', each_one_content)[0]
                item['content'] = \
                re.findall(r'threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>', each_one_content)[0]
                print(item)
                await table.update({'title': item['title']}, {'$set': item}, True)
            except:
                pass


# 创建数据库任务
def get_database_tasks(index):
    print('index::',index)
    _tasks = [
        asyncio.ensure_future(
            save_to_database(start=index, stop=index+5000) # 每次指定一个跨度
        )
    ]
    return _tasks


# 实例化
loop = asyncio.get_event_loop()
for i in range(0, 10000, 5000):
    # 待处理
    tasks = get_database_tasks(i)
    # 启动
    loop.run_until_complete(asyncio.gather(*tasks))




end_time = time.time()
total_time = end_time - start_time
print(total_time)










