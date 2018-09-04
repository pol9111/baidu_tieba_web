import grequests
from config import *
import re
from utils import logger
from task import Task
import requests
import gevent
from gevent import monkey
from gevent.pool import Pool

# monkey.patch_all()

class Spider:
    def __init__(self):
        self.headers = HEADERS
        # self.proxies = PROXIES
        self.url = URL
        self.kw = KW
        self.redis_client = REDIS_CLIENT
        self.logger = logger()
        self.monkey =  monkey.patch_all()

    def fetch_async(self, method, url, req_kwargs):
        resp = requests.request(method=method, url=url, **req_kwargs)
        self.parse_resp(resp.text)


    def async_req(self, per_step_urls):
        """获取响应内容"""
        req_list = []
        pool = Pool(64)
        for url in per_step_urls:
            req = pool.spawn(self.fetch_async, method='get', url=url, req_kwargs={})
            req_list.append(req)
        gevent.joinall(req_list)


    def parse_resp(self, html):
        """解析响应内容"""

        each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', html)
        for each_one_content in each_page_content:
            try:
                item = {}
                item["id"] = re.findall(r'href="(/p/\d+)"', each_one_content)[0]
                item["title"] = re.findall(r'class="j_th_tit ">(.*?)</a>', each_one_content)[0]
                item["author"] = re.findall(r'title="主题作者: (.*?)"', each_one_content)[0]
                item["create_time"] = re.findall(r'创建时间">(.*?)</span>', each_one_content)[0]
                item["reply_num"] = re.findall(r'"回复">(\d+)</span>', each_one_content)[0]
                item["last_reply"] = re.findall(r'title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>', each_one_content)[0]
                item["content"] = re.findall(r'threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>', each_one_content)[0]
                print(item)
                self.save_data(item)
            except Exception as e:
                self.logger.error('页面解析失败'+str(e))
                print(e)
                pass

    def save_data(self, item):
        """暂存数据到内存"""
        self.redis_client.lpush('tiezi', item)




