'''
版本2.0 by 2019.06.08 20:31

相较1.0增添了大量内容。

已知不足：
1、自动跳转是否18岁确认按钮，尚未解决此问题
2、未登录，部分权限受限
3、回复可见的内容
4、未将帖子的内容爬下来，特别是下载链接
5、保存网页到本地后，本地打开，也会跳转至18岁确认按钮，不知道怎么跳转的
6、正则表达式仍需改善

截至今天，桃隐帖子的网址有两种，形如：
http://c.taoy66.vip/thread-776837-1-1.html
http://org.taoy66.info/thread-724445-1-1.html
当然也有在上面基础上添加后缀的，如：
http://wvvw.taoy111.info/forum.php?mod=viewthread&tid=648131&extra=&page=1&mobile=2

已失效的网址形如：http://wvvw.taoy111.info/thread-472713-1-1.html
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

    url = re.sub(r'&mobile=2', '', url)

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
               'Cookie' : 'imalready18y=OK;pDXj_2132_auth=884f0oxmVZ%2F2P%2BBd8X%2Bt17USS89dnQrSu7TU38GdSMbCGt090UHeuQ%2BTB0uCjMwbRxBaS2b9kLyJmmRVyNwMMsNDKo4'
               }

    for _ in range(0, 10):    #尝试请求10次
        try:
            req = request.Request(url=url, headers=headers)
            response = request.urlopen(req, timeout=10)
            
            global html
            html = response.read().decode('utf-8')
            print('获取成功！\n')

            return True
            
        except Exception as e:
            if _ < 4:
                pause = random.uniform(0.5, 1.5)
                print('发生错误：%s    %.2f秒后再次尝试' % (e,pause))
                time.sleep(pause)
                print('重新尝试获取网页源代码......')
            else:
                print('获取网页源代码失败,任务中止\n')
            
    return False


def  no_prompt_message():
    
    if re.search(r'抱歉，指定的主题不存在或已被删除或正在被审核', html):
        print('抱歉，指定的主题不存在或已被删除或正在被审核，任务中止\n')
        return False
    elif re.search(r'抱歉，您没有权限访问该版块', html):
        print('抱歉，没有权限访问该版块，任务中止\n')
        return False
    elif re.search(r'提示信息 桃隐社区', html):
        print('“提示信息 桃隐社区”，我没搞懂,任务中止\n')
        return False

    return True
    
    
def get_html_name():
    
    print('正在获取网页标题......')

    pattern = re.compile(r'(?<=<title>).+?(?=</title>)')
    global html_name
    html_name = pattern.search(html).group()
    
    pattern = re.compile(r'[\\\*\?\|/:"<>]')
    m = pattern.search(html_name)
    while m:
        html_name = html_name[ : m.start()] + html_name[m.start()+1 : ]
        m = pattern.search(html_name)

    html_name = re.sub(r' - 国产自拍偷拍艳照 桃隐社区', '', html_name)
        
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


def save_html():
    
    html_filepath = os.path.join(path, html_name+'.txt')
    html_file = open(html_filepath, 'w', encoding='utf-8')
    html_file.write(html)
    html_file.close()
    print('已保存%s\n' % html_filepath)
    

def get_img_urls():
    
    print('正在获取图片网址......')
    
    '''已知的桃隐图片网址上下文：
        onclick="zoom(this, this.src, 0, 0, 0)" class="zoom" file="https://upload.cc/i1/2019/05/08/t31sZ4.jpeg" onmouseover="img_onmouseoverfunc(this)" lazyloadthumb="1" border="0" alt="" /><br />
        onclick="zoom(this, this.src, 0, 0, 0)" class="zoom" file="https://upload.cc/i1/2019/05/08/t31sZ4.jpeg" onmouseover="img_onmouseoverfunc(this)" lazyloadthumb="1" border="0" alt="" /> <br />
        (只发现一例 http://org.taoy66.info/thread-787076-1-1.html)
        src="static/image/common/none.gif" zoomfile="http://img3.taoimg.info/tyupload/forum/201812/03/123547z6ck921xz6htzjeo.jpg" file="http://img3.taoimg.info/tyupload/forum/201812/03/123547z6ck921xz6htzjeo.jpg" class="zoom" onclick="zoom(this, this.src, 0, 0, 0)" width="575"
        (只发现一例 http://org.taoy66.info/thread-694604-1-1.html)
    '''
    re_str = r'((?<=onclick="zoom\(this, this\.src, 0, 0, 0\)" class="zoom" file=").+?(?=" onmouseover="img_onmouseoverfunc\(this\)" lazyloadthumb="1" border="0" alt="" />))|((?<=src="static/image/common/none.gif" zoomfile=").+?(?=" file="))'
    pattern = re.compile(re_str,flags=re.I)
    global img_urls
    img_urls = pattern.finditer(html)
    
    global img_urls_dict
    img_urls_dict = {}
    for i, i_img_url in enumerate(img_urls):
        img_urls_dict[str(i)] = i_img_url.group()
    
    global img_amount
    img_amount = len(img_urls_dict)
    global success_img_amount
    success_img_amount = 0
    
    print('获取成功！本网页共有%d张目标图片\n' % img_amount)

    
def get_img(img_url, i, run_time):
    
    print('正在向图%d发送第%d次请求......' % (i+1,run_time+1))
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
        global success_img_amount
        print('进度%d/%d' % (success_img_amount, img_amount))
        return False
         

def save_img(img_url, i):
    
    print('正在保存图%d......' % (i+1))
    
    global img_name
    img_name = img_url.split('/')[-1]
    
    global filepath
    filepath = os.path.join(path, img_name)

    f = open(filepath, 'wb+')
    f.write(img)
    f.close()
        
    print('保存成功！')
    global success_img_amount
    success_img_amount += 1
    print('进度%d/%d' % (success_img_amount, img_amount))


def get_and_save_once(run_time):
    
    global failed_urls_dict     
    global img_urls_dict
    # 如果你只是在开始声明了全局变量，但在函数中使用的时候没有声明，系统默认这个变量为局部变量。
    if run_time != 0:
        img_urls_dict = failed_urls_dict
    failed_urls_dict = {}
    
    for i, i_img_url in img_urls_dict.items():
        
        if get_img(i_img_url, int(i), run_time) :
            save_img(i_img_url, int(i))

        pause = random.uniform(0.5, 1.5)
        print('任务暂停%f秒钟\n' % pause)
        time.sleep(pause)
    
    if failed_urls_dict:
        print('%d张图片下载失败：' % len(failed_urls_dict))
        for i in failed_urls_dict:
            print('图%d：' % (int(i)+1), failed_urls_dict[i])
        print()


if __name__ == '__main__':
    
    start = time.perf_counter()
    
    if get_html():
        if no_prompt_message():
            get_html_name()
            make_dir()
            save_html()
            get_img_urls()

            for run_time in range(0,10):    #尝试10次
                get_and_save_once(run_time)

            end = time.perf_counter()
            print('任务执行共%.2f秒，共下载%d张图片,失败%d张'% (end-start, img_amount-len(failed_urls_dict), len(failed_urls_dict)))
            print('图片保存至%s' % path)
