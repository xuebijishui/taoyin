### 依赖：

bs4, lxml

### 使用流程介绍：

使用crawler_for_single_url.py或crawler_for_multiple_urls.py爬取图片，
爬取完后会将该网页的桃隐贴子编号存入SAVED.txt，失败图片信息存入ERROR.txt
(即使有爬取失败的图片，但只要按流程走到最后一步，也会将贴子编号存入SAVED.txt)
下次再次使用该程序，若贴子编号在SAVED.txt中，则跳过爬取该网页。
使用crawler_for_img_of_ERRORtxt.py可以下载ERROR.txt中的图片。

### 最新版本文件简介：

主程序：
crawler_class.py                    爬虫类
crawler_for_single_url.py           下载单一网页内的所有目标图片
crawler_for_multiple_urls.py        下载多个网页内的所有目标图片
crawler_for_img_of_ERRORtxt.py      下载之前下载失败的图片（通过读取ERROR.txt）
辅助程序：
get_taoyin_urls_from_favorite.py    从从浏览器导出的收藏夹中提取出桃隐网页
prettify_html_by_BeautifulSoup4.py  美化网页源代码缩进



版本更新：

版本5.0   2019.06.18