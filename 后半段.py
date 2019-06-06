import re
import os
from urllib import request


def get_html_name():

    pattern = re.compile(r'(?<=<span id="thread_subject">).+?(?=</span>)')
    global html_name
    html_name = pattern.search(html).group()
    
    pattern = re.compile(r'[\\\*\?\|/:"<>]')
    m = pattern.search(html_name)
    while m:
        html_name = html_name[ : m.start()] + html_name[m.start()+1 : ]
        m = pattern.search(html_name)


def make_dir():
    
    global path
    path = os.path.join('D:\桌面\桃隐', html_name)
    os.makedirs(path)


def get_img_urls():
    
    pattern = re.compile(r'https://www\.sehuatuchuang\.com/images/\d{4}/\d{2}/\d{2}/\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))',flags=re.I)
    global img_urls
    img_urls = pattern.finditer(html)
    
    
def get_img(img_url):
    
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
        print(img_url, '  服务器返回非200')


def save_img(img_url):
    
    global img_name
    img_name = re.search(r'\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))', img_url, flags=re.I).group()

    global filepath
    filepath = os.path.join(path, img_name)
    f = open(filepath, 'wb+')
    f.write(img)
    f.close()


if __name__ == '__main__':
    
    f = open('桃隐.txt', 'r', encoding='utf-8')
    global html 
    html = f.read()
    f.close()

    get_html_name()
    make_dir()
    get_img_urls()
    for img_url in img_urls:
        get_img(img_url.group())
        save_img(img_url.group())
