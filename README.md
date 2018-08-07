# Tieba-tiezi

## 目标

网站: 百度指定贴吧

urls:

- tieba.baidu.com/f?kw=[#]=utf-8&pn=[#+50]

信息:

- 父节点

  ```
  <div class="t_con cleafix">([\s\S]*?)<li class=" j_thread_list clearfix"
  ```


- 帖子标题

  ```
  class="j_th_tit ">([\s\S]*?)</a>
  ```

- 一楼内容

  ```
  threadlist_abs threadlist_abs_onlyline ">\n[\s]*(.*?)\n[\s]*</div>
  ```

- 楼主昵称

  ```
  title="主题作者: (.*?)"
  ```

- 创建时间(多个帖子面没显示, 但是有)

  ```
  创建时间">(.*?)</span>
  ```

- 回复数

  ```
  "回复">(\d+)</span>
  ```

- 最后回复时间

  ```
  title="最后回复时间">\r\n[\s]*?(\d+:\d+|\d+-\d+)[\s]*?</span>
  ```


## 多版本用时测试

单线程
242.61285209655762
多线程
8线程
32.424975872039795

16线程
35.64368152618408 - 8(阻塞了)

32线程
18.901715993881226