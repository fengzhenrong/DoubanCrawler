项目 豆瓣上最好的电影
=====

项目概述
----

在这个项目中, 你将会学习到如何从豆瓣电影的网页中获取你喜欢的类别，收集各个地区的高评分电影，收集他们的名称、评分、电影页面的链接和电影海报的链接；

备注：原本是项目是打算通过使用库 requests get 函数获取豆瓣电影列表页面信息，但是有些列表需要多页显示，我们需要不断模拟点击加载更多按钮来显示这个列表上的全部电影，所以使用了selenium自动化测试工具来获取html页面内容，如果你不懂怎么安装安装 selenium 和 chromedriver，你可以参考[这份指南](https://www.jianshu.com/p/5a8ddc66b282)。

### 运行环境
Python3.7

Chrome浏览器

### 依赖库
selenium webdriver

bs4 BeautifulSoup

urllib

os

pandas

## 工程目录
movie.py文件，详细记录了如何获取电影信息的并输出表格

expanddouban.py文件，定义了selenium自动化测试工具来获取html的函数

## 运行

cd DoubanCrawler

python movie.py

[我的博客地址](https://www.jianshu.com/p/5a8ddc66b282)有详细的介绍：https://www.jianshu.com/p/8237303b0cfd
