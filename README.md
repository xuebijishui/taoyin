### 依赖：

bs4, lxml

### 使用流程介绍：

使用**crawler_for_single_url.py**或**crawler_for_multiple_urls.py**爬取图片，爬取完后会将该网页的桃隐贴子编号存入SAVED.txt，失败图片信息存入ERROR.txt（即使有爬取失败的图片，但只要按流程走到最后一步，也会将贴子编号存入SAVED.txt）下次再次使用该程序，若贴子编号在SAVED.txt中，则跳过爬取该网页。使用**crawler_for_img_of_ERRORtxt.py**可以下载ERROR.txt中的图片。如果程序中途意外中止运行，不必担心，信息存入SAVED.txt和ERROR.txt是即时的，不必担心重复爬取。

### 最新版本文件简介：

##### 主程序：

crawler_class.py                                   爬虫类
crawler_for_single_url.py                   下载单一网页内的所有目标图片
crawler_for_multiple_urls.py             下载多个网页内的所有目标图片
crawler_for_img_of_ERRORtxt.py      下载之前下载失败的图片（通过读取ERROR.txt）

##### 辅助程序：

get_taoyin_urls_from_favorite.py       从从浏览器导出的收藏夹中提取出桃隐网页
prettify_html_by_BeautifulSoup4.py  美化网页源代码缩进

### 版本更新：

##### 版本5.0    2019.06.18

开始生成SAVED.txt, ERROR.txt, Download Link.txt

引入traceback，在被调用函数中获取调用它的函数信息

优化了从网页中提取目标图片时的一个bug

等等

缺点：类内成员变量很乱，类的初始化传值很乱

##### 版本4.0    2019.06.16

添加html_type == 2时的爬取图片策略和制作网页策略

更改存储路径为sub_path = ''    #子路径，如：桃隐社区\H漫画|同人|汉化字幕\以网页标题命名的文件夹

在def no_alert_error(self, html_source_code)中添加了一种情况

美化html_frame

等等

##### 版本3.0    2019.06.1？

基本全部用类重构了一遍，并提供单网页和多网页的选择

开始引入bs4

可以提取目标网页主要内容并制作净化后的网页

等等

##### 版本2.0    2019.06.08 20:31

增添了大量内容

缺点：

1、自动跳转是否18岁确认按钮，尚未解决此问题

2、未登录，部分权限受限

3、回复可见的内容

4、未将帖子的内容爬下来，特别是下载链接

5、保存网页到本地后，本地打开，也会跳转至18岁确认按钮，不知道怎么跳转的

6、正则表达式仍需改善

##### 版本1.1    2018.06.08 01:47

1、完善正则表达式的提取

2、用时统计

3、各步骤文字提示

4、源代码内置目标网址改为运行时输入网址

##### 版本1.0    2019.06.07

人生第一个python爬虫小程序