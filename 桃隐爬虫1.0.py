'''
人生第一个python爬虫小程序
版本1.0 by 2019.06.07
'''

import re
import os
from urllib import request


def get_html():
    
    print('正在获取网页源代码......')
    
    headers = {'Host' : 'c.taoy66.vip',
               'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
               'Accept-Encoding' : 'deflate, sdch, br',
               'Connection' : 'keep-alive',
               'Pragma' : 'no-cache',
               'Cache-Control' : 'no-cache',
               'Upgrade-Insecure-Requests': '1',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Cookie' : 'imalready18y=OK'
           }  
    url = 'http://c.taoy66.vip/thread-781456-1-1.html'
    req = request.Request(url=url, headers=headers)
    global html
    html = request.urlopen(req).read().decode('utf-8')


def get_html_name():
    
    print('正在获取网页标题......')
    
    pattern = re.compile(r'(?<=<span id="thread_subject">).+?(?=</span>)')
    global html_name
    html_name = pattern.search(html).group()
    
    pattern = re.compile(r'[\\\*\?\|/:"<>]')
    m = pattern.search(html_name)
    while m:
        html_name = html_name[ : m.start()] + html_name[m.start()+1 : ]
        m = pattern.search(html_name)


def make_dir():
    
    print('正在创建文件夹......')
    
    global path
    path = os.path.join('D:\桌面\桃隐', html_name)
    os.makedirs(path)


def get_img_urls():
    
    print('正在获取图片网址......')
    
    pattern = re.compile(r'https://www\.sehuatuchuang\.com/images/\d{4}/\d{2}/\d{2}/\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))',flags=re.I)
    global img_urls
    img_urls = pattern.finditer(html)
    
    
def get_img(img_url):
    
    print('正在连接第%d张图片......' % n)
    
    headers = {'Host' : 'www.sehuatuchuang.com',
               'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
               'Accept-Encoding' : 'deflate, sdch, br',
               'Connection' : 'keep-alive',
               'Pragma' : 'no-cache',
               'Cache-Control' : 'no-cache',
               'Upgrade-Insecure-Requests': '1',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               }
            
    req = request.Request(url=img_url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200: 
        global img
        img = request.urlopen(req).read()
    else:
        print('连接第%d张图片时服务器返回非200状态码' % n)


def save_img(img_url):
    
    print('正在保存第%d张图片......' % n)
    
    global img_name
    img_name = re.search(r'\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))', img_url, flags=re.I).group()

    global filepath
    filepath = os.path.join(path, img_name)
    f = open(filepath, 'wb+')
    f.write(img)
    f.close()


if __name__ == '__main__':
    
    get_html()
    get_html_name()
    make_dir()
    get_img_urls()
    n = 1
    for img_url in img_urls:
        get_img(img_url.group())
        save_img(img_url.group())
        n += 1