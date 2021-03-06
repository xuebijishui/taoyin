# 桃隐社区图片爬虫

桃隐的域名变换频繁，请通过地址发布器获取。

此程序仅用于交流学习，**严禁用于非法用途**，否则后果自负。

（前排吐槽写这个网站的程序员GG，代码写的好乱，好几套模板不说，还到处飘bug，感觉就是修修补补，最后网站可以正常运行，只是对于爬图片的人来说头都大了。更何况这是我第一个爬虫程序。）

## 依赖：

requests，bs4，lxml

## 使用介绍：

&emsp;&emsp;使用**down_one.py**或**down_some.py.py**爬取图片，爬取完后会将该网页的桃隐贴子编号存入SAVED.txt，失败图片信息存入ERROR.txt，若页面内存在资源下载链接，则信息存入Download Link.txt（即使有爬取失败的图片，但只要按流程走到最后一步，也会将贴子编号存入SAVED.txt）下次再次使用该程序，若贴子编号在SAVED.txt中，则跳过爬取该网页。使用**down_error.py**可以下载ERROR.txt中的图片。如果程序中途意外中止运行，不必担心，信息存入SAVED.txt和ERROR.txt是即时的，不必担心重复爬取。

## 最新版本文件简介：

#### 主程序：

**down_one.py**　　下载单一网页内的所有目标图片

**down_some.py**　　下载多个网页内的所有目标图片

**down_error.py**&emsp;&emsp;下载之前下载失败的图片（通过读取ERROR.txt）

#### 辅助程序：

**get_taoyin_urls_from_favorite.py**&emsp;&emsp;从从浏览器导出的收藏夹中提取出桃隐网页

**prettify_html_by_BeautifulSoup4.py**&emsp;&emsp;美化网页源代码缩进

#### 其他文件

**taoyin_urls.txt** 通过使用**crawler_for_multiple_urls.py** 爬取此文件内的网址的内容

**SAVED.txt** 已爬取的贴子的编号，即使存在部分图片未爬取成功，也会写入此文件

**NO EXIST.txt** 不存在或已删除的贴子的编号

**NO JURISDICTION.txt** 没有权限的贴子的编号

**ERROR.txt** 失败图片的信息，有贴子编号，图片网址，图片序号，图片下载地址

**Download Link.txt** 若网页中含有下载链接，则存入此文件

## 版本更新：

* #### 版本8.0　　2019.07.31

   * 代码重构
   * 增添多线程
   * 更换新域名以及对应headers

* #### **~~由于时间关系，此后只修bug，不再增新~~ ,存在以下遗憾：**

  - 未登录导致部分贴子游客权限不够
  - 未登录并回复导致部分贴子无法爬取全部图片
  - ~~没有多线程~~

* #### 版本7.0        2019.07.24

  * **在8.0中取消的文件**

    crawler_class.py&emsp;&emsp;爬虫类

    crawler_for_single_url.py&emsp;&emsp;下载单一网页内的所有目标图片

    crawler_for_multiple_urls.py&emsp;&emsp;下载多个网页内的所有目标图片

    crawler_for_img_of_ERRORtxt.py&emsp;&emsp;下载之前下载失败的图片（通过读取ERROR.txt）

  * 给crawler_for_img_of_ERRORtxt.py增添了多线程，另外两个程序因为担心多线程会导致写入文件出现问题，没有写多线程（~~才不是因为懒呢~~）

* #### 版本6.0        2019.07.23

  * 完善类的成员变量，完整框架，修复bug

  * 开始生成NO EXIST.txt，NO JURISDICTION.txt

* #### 版本5.0&emsp;&emsp;2019.06.18

   * 开始生成SAVED.txt, ERROR.txt, Download Link.txt

   * 引入traceback，在被调用函数中获取调用它的函数信息

   * 优化了从网页中提取目标图片时的一个bug

   * 等等

   * 缺点：类内成员变量很乱，类的初始化传值很乱

   * BUG：回复可见类型的，如725217。

* #### 版本4.0&emsp;&emsp;2019.06.16

   * 添加html_type == 2时的爬取图片策略和制作网页策略

   * 更改存储路径为sub_path = ''    #子路径，如：桃隐社区\H漫画|同人|汉化字幕\以网页标题命名的文件夹

   * 在def no_alert_error(self, html_source_code)中添加了一种情况

   * 美化html_frame

   * 等等

* #### 版本3.0&emsp;&emsp;2019.06.1？

   * 基本全部用类重构了一遍，并提供单网页和多网页的选择

   * 开始引入bs4

   * 可以提取目标网页主要内容并制作净化后的网页

   * 等等

* #### 版本2.0&emsp;&emsp;2019.06.08 20:31

   * 增添了大量内容

   * 缺点：

      * 自动跳转是否18岁确认按钮，尚未解决此问题

      * 未登录，部分权限受限

      * 回复可见的内容

      * 未将帖子的内容爬下来，特别是下载链接

      * 保存网页到本地后，本地打开，也会跳转至18岁确认按钮，不知道怎么跳转的

      * 正则表达式仍需改善

* #### 版本1.1&emsp;&emsp;2018.06.08 01:47

   * 完善正则表达式的提取

   * 用时统计

   * 各步骤文字提示

   * 源代码内置目标网址改为运行时输入网址

* #### 版本1.0&emsp;&emsp;2019.06.07

   人生第一个python爬虫小程序