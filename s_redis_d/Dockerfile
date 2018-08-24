FROM   python:3.6
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -i https://pypi.douban.com/simple -r requirements.txt
CMD scrapy crawl tieba 


