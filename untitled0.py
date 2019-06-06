# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:03:20 2019

@author: kljxn
"""

from urllib import request 
import re


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
html = request.urlopen(req).read().decode('utf-8')

pettern = re.compile(r'https://www\.sehuatuchuang\.com/images/\d{4}/\d{2}/\d{2}/.+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))')
photo_urls = pattern.findall(html)
for i in photo_urls:
    print(i)


print(html)