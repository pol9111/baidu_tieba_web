import requests
from config import *
import re
from utils import logger

class Spider:
    def __init__(self):
        self.headers = HEADERS
        # self.proxies = PROXIES
        self.url = URL
        self.kw = KW
        self.redis_client = REDIS_CLIENT
        self.logger = logger()

    def get_resp(self, url):
        """获取响应内容"""
        resp = requests.get(url, headers=HEADERS, timeout=15).text
        self.parse_resp(resp)

    def parse_resp(self, html):
        """解析响应内容"""
        each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', html)
        for each_one_content in each_page_content:
            try:
                item = {}
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

# id  //div[@class="threadlist_title pull_left j_th_tit"]/a/@href


