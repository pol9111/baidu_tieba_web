# Tieba-tiezi

## 目标

网站: 百度指定贴吧

urls:

- tieba.baidu.com/f?kw=[#]=utf-8&pn=[#+50]


</br>

</br>

## 创建表

create table if not exists tiezi(
	title varchar(200),
	author varchar(20),
	create_time varchar(10),
	reply_num int,
	last_reply varchar(50),
	content varchar(1000)
);
</br>
</br>

### 插入数据

"INSERT INTO tiezi (title, author, create_time, reply_num, last_reply, content) values (%s, %s, %s, %s, %s, %s)", (item['title'], item['author'], item['create_time'], item['reply_num'], item['last_reply'], item['content'])


</br>
</br>


## 多版本用时测试

以炉石传说吧前两百页为例子
</br>

单线程
242.61285209655762     
</br>
</br>

多线程
8线程
35.76421284675598  
</br>

16线程
23.506305932998657    
</br>

32线程
21.40897274017334

</br>
</br>

多线程-future


32线程

18.901715993881226

11.27827763557434(存入redis)

13.140218257904053(响应+解析+存入redis+导入mongoDB)

</br>

64线程
17.94631290435791

5倍, 50000帖子
63.30482363700867(响应+解析+存入redis+导入mongoDB)
升级了带宽
25.028305530548096
升级了固态, 加快读写
20.177664279937744

</br>

异步

6.3642566204071045 (单单请求与响应)

15.007196426391602(响应+解析)

26.224395036697388(响应+解析+redis)

18.901715993881226    
</br>


64线程
17.94631290435791  


</br>  
</br>   

异步

6.3642566204071045 (单单请求与响应)              


异步(存入mysql)
75.84078431129456   

异步请求, 32线程写入
21.274948835372925    

gevent 64线程
23.599619150161743


</br>
</br>

多进程+多线程

54.989933013916016   5万  每个跨度循环结束后保存数据

43.198081493377686   5万  每个进程结束保存数据

103.46190881729126   10万  8进程

27.243698596954346   5万  4进程  大大减少了读存数据的次数

</br>
</br>


celery+gevent
25秒  - 4个worker




