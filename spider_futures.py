from concurrent import futures
import requests
from config import *
import re
import time

class Spider:
    def __init__(self):
        self.headers = HEADERS
        self.proxies = PROXIES
        self.url = URL
        self.kw = KW
        self.mongo_table = table

    @classmethod
    def get_urls(cls):
        """获取url列表"""
        url_list = []
        for each in range(0, 10000, 50):
            each_page_url = URL + '/f?kw={}&ie=utf-8&pn='.format(KW) + str(each)
            url_list.append(each_page_url)
        return url_list

    def get_resp(self, url):
        """获取响应内容"""
        resp = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=15).text
        self.parse_resp(resp)

    def parse_resp(self, html):
        """解析响应内容"""
        each_page_content = re.findall(r'<div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"', html)
        for each_one_content in each_page_content:
            try:
                item = {}
                item['title'] = re.findall(r'class="j_th_tit ">(.*?)</a>', each_one_content)[0]
                item['author'] = re.findall(r'title="主题作者: (.*?)"', each_one_content)[0]
                item['create_time'] = re.findall(r'创建时间">(.*?)</span>', each_one_content)[0]
                item['reply_num'] = re.findall(r'"回复">(\d+)</span>', each_one_content)[0]
                item['last_reply'] = re.findall(r'title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>', each_one_content)[0]
                item['content'] = re.findall(r'threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>', each_one_content)[0]
                print(item)
                self.save_data(item)
            except:
                pass

    def save_data(self, item):
        """保存数据"""
        table.update({'title': item['title']}, {'$set': item}, True)

if __name__ == '__main__':
    start_time = time.time()

    spider = Spider()
    urls = spider.get_urls()
    with futures.ThreadPoolExecutor(32) as executor:
        executor.map(spider.get_resp, urls)

    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)


