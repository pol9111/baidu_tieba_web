from config import *
import re
from crawler import TiebaSpider


async def parse(per_step_urls, proxies):
    """页面解析"""
    spider = TiebaSpider()
    tasks = await spider.downloader(per_step_urls, proxies)
    for html in tasks: # 每个任务总数, 上面总共一个任务, task[0]才是每个循环的所有响应文件
        if html:
            each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', html.decode())
            for each_one_content in each_page_content:
                try:
                    item = dict()
                    item["id"] = re.findall(r'href="(/p/\d+)"', each_one_content)[0]
                    item['title'] = re.findall(r'class="j_th_tit ">(.*?)</a>', each_one_content)[0]
                    item['author'] = re.findall(r'title="主题作者: (.*?)"', each_one_content)[0]
                    item['create_time'] = re.findall(r'创建时间">(.*?)</span>', each_one_content)[0]
                    item['reply_num'] = re.findall(r'"回复">(\d+)</span>', each_one_content)[0]
                    item['last_reply'] = re.findall(r'title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>', each_one_content)[0]
                    item['content'] = re.findall(r'threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>', each_one_content)[0]
                    print(item)
                    await save_data(item)
                except:
                    print('解析失败!!')
                    pass

async def save_data(items):
    """数据暂存到redis中"""
    REDIS_CLIENT.sadd('tiezi', items)









