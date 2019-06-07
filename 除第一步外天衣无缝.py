# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:43:36 2019

@author: kljxn
"""

'''
新增：
1、完善正则表达式的提取
2、用时统计
3、各步骤文字提示
4、源代码内置目标网址改为运行时输入网址
'''

'''
人生第一个python爬虫小程序
版本1.1 by 2019.06.08 01:47
'''


import re
import os
import time
import random
from urllib import request


def get_html():
    
    url = input('请输入要爬取图片的网址：\n')
    while True:
        if re.match(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+',url):
            break
        else:
            url = input('URL格式不正确，请重新输入：\n')

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

    try:
        
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req, timeout=10)
        
        global html
        html = response.read().decode('utf-8')
        print('获取成功！\n')
        return True
        
    except Exception as e:
        print('发生错误：%s' % e)
        return False
    
    
def get_html_name():
    
    print('正在获取网页标题......')
    
    #pattern = re.compile(r'(?<=<span id="thread_subject">).+?(?=</span>)')
    pattern = re.compile(r'(?<=<title>).+?(?=</title>)')
    global html_name
    html_name = pattern.search(html).group()
    
    pattern = re.compile(r'[\\\*\?\|/:"<>]')
    m = pattern.search(html_name)
    while m:
        html_name = html_name[ : m.start()] + html_name[m.start()+1 : ]
        m = pattern.search(html_name)
        
    print('网页标题为：', html_name, '\n')


def make_dir():
    
    print('正在创建文件夹......')
    
    global path
    path = os.path.join('D:\桌面\桃隐', html_name)
    if not os.path.exists(path):
        os.makedirs(path)
        print('已创建文件夹：',path, '\n')
    else:
        print('文件夹已存在，无需再次创建\n')
    

def get_img_urls():
    
    print('正在获取图片网址......')
    
    pattern = re.compile(r'(https://www\.sehuatuchuang\.com/images/\d{4}/\d{2}/\d{2}/.+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp)))|(https://upload.cc/i1/\d{4}/\d{2}/\d{2}/.+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp)))',flags=re.I)
    global img_urls
    img_urls = pattern.finditer(html)
    
    global img_urls_dict
    img_urls_dict = {}
    for i, i_img_url in enumerate(img_urls):
        img_urls_dict[str(i)] = i_img_url.group()
    
    global img_amount
    img_amount = len(img_urls_dict)
    
    print('获取成功！\n')

    
def get_img(img_url, i):
    
    print('正在向第%d张图片发送请求......' % (i+1))
    print('图片网址为：', img_url)
     
    
                    
    headers = {'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
               'Accept-Encoding' : 'deflate, sdch, br',
               'Connection' : 'keep-alive',
               'Pragma' : 'no-cache',
               'Cache-Control' : 'no-cache',
               'Upgrade-Insecure-Requests': '1',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               }
    
    try:
        
        req = request.Request(url=img_url, headers=headers)
        response = request.urlopen(req, timeout=3)
        global img
        img = response.read()
        print('请求成功!')
        return True

    except Exception as e:
        
        print('发生错误：%s\n自动记录并跳过此图片' % e)
        global failed_urls_dict
        failed_urls_dict[str(i)] = img_url
        return False
         

def save_img(img_url, i):
    
    print('正在保存第%d张图片......' % (i+1))
    
    global img_name
    img_name = re.search(r'(?<=\d{4}/\d{2}/\d{2}/).+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))', img_url, flags=re.I).group()
    
    global filepath
    filepath = os.path.join(path, img_name)
    f = open(filepath, 'wb+')
    f.write(img)
    f.close()
        
    print('保存成功！')


def get_and_save_once(run_time):
    
    global failed_urls_dict     
    global img_urls_dict
    # 如果你只是在开始声明了全局变量，但在函数中使用的时候没有声明，系统默认这个变量为局部变量。
    if run_time != 0:
        img_urls_dict = failed_urls_dict
    failed_urls_dict = {}
    
    for i, i_img_url in img_urls_dict.items():
        
        if get_img(i_img_url, int(i)) :
            save_img(i_img_url, int(i))

        parse = random.uniform(0.5, 1.5)
        print('任务暂停%f秒钟\n' % parse)
        time.sleep(parse)
    
    if failed_urls_dict:
        print('%d张图片下载失败：' % len(failed_urls_dict))
        for i in failed_urls_dict:
            print('图%d：' % (int(i)+1), failed_urls_dict[i])
        print()


if __name__ == '__main__':
    
    start = time.perf_counter()
    
    if True:#(get_html()):

        f=open('taoyin.txt','r',encoding='utf-8')
        global html
        html=f.read()
        f.close()
        
        get_html_name()
        make_dir()
        get_img_urls()
        
        for i in range(0,10):    #尝试10次
            get_and_save_once(i)
        
    end = time.perf_counter()
    global failed_urls_dict
    print('任务执行共%.2f秒，共下载%d张图片,失败%d张'% (end-start, img_amount-len(failed_urls_dict), len(failed_urls_dict)))