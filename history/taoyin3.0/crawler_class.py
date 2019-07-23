import re
import os
import time
import random
from urllib import request
from bs4 import BeautifulSoup
from textwrap import dedent    #通过缩进美化多行字符串在源代码中的显示
import copy    #深拷贝



class Crawler_class:
        
    
        
    failed_img_list = []   #里面嵌套着多个failed_img_dict = {'url':'', 'img_number':0, 'dir_path':''}
    success_img_amount = 0
    img_amount = 0
    
    
    def correct_url(self, url):
        
        """
        桃隐的域名经常改变，以前收藏的网址会打不开，但是只要从中提取出该网页的编号，拼接到可用的域名中就能再次访问
        桃隐的网址传值方法有两种，如：
        http://c.taoy66.vip/forum.php?mod=viewthread&tid=694604
        http://c.taoy66.vip/thread-694604-1-1.html
        上面两个网址可以进入编号为694604的帖子,本程序默认使用后者（因为短）
        """
        
        domain_name = 'c.taoy66.vip'
        print('\n请确认目前是否可以通过%s访问桃隐，如不能，请在函数correct_url()中修改domain_name的值为桃隐的最新域名' % domain_name)
        
        counter = 0
        while counter < 20 :    #为防止爬多个网页时碰到一个格式错误的url，会死循环，将错误次数上限定义为20，而不是无限
            
            if re.match(r'\d+',url):    #输入的是帖子序号
                url = 'http://' + domain_name + '/thread-' + url + '-1-1.html'
                return url
            
            url_number = re.search(r'((?<=tid=)\d+)|((?<=thread-)\d+?(?=-1-1))', url)    #输入的是帖子网址
            if url_number:
                url = 'http://' + domain_name + '/thread-' + url_number.group() + '-1-1.html'
                return url
            else:
                url = input('URL格式不符合桃隐网址的命名规则，请重新输入：\n')
                counter += 1
                
        print('键入错误的URL已达20次，此次任务中止')
        return None
    
    
    def get_html_source_code(self,url):
        
        print('\n正在访问%s\n正在获取网页源代码......\n' % url)
        
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
        
        for i in range(0, 10):    #尝试请求10次
            try:
                req = request.Request(url=url, headers=headers)
                response = request.urlopen(req, timeout=10)        #请求超过10秒则停止此次请求
                
                html_source_code = response.read().decode('utf-8')
                print('获取成功！\n')
                return html_source_code
                
            except Exception as e:
                if i < 9:
                    pause = random.uniform(0.5, 1.5)
                    print('发生错误：%s    %.2f秒后再次尝试' % (e,pause))
                    time.sleep(pause)
                    print('重新尝试获取网页源代码......')
                else:
                    print('获取网页源代码失败，对于本网页的任务中止\n')
                
        return None
    
    
    def no_alert_error(self, html_source_code):
    
        '''
        已知有：
        150002：抱歉，指定的主题不存在或已被删除或正在被审核
        477429：没有找到帖子
        ？：没有权限
        '''
        
        soup = BeautifulSoup(html_source_code, 'lxml')    
        content = soup.find('div', class_='alert_error')
        if not content is None:
            content = content.find('p')
            alert_error = re.sub('\s','',content.text)
            print(alert_error,'，对于本网页的任务中止\n')
            return False
    
        return True
    
    
    def get_html_title(self, html_source_code):
    
        print('正在获取网页标题......')
        
        soup = BeautifulSoup(html_source_code,'lxml')
        html_title = soup.find('title').string
        html_title = re.sub(r'[\\\*\?\|/:"<>\s]', '', html_title)
        html_title = re.sub(r'-国产自拍偷拍艳照桃隐社区', '', html_title)
        
        print('网页标题为：', html_title, '\n')
        return html_title
    
    
    def make_dir(self, html_title):
    
        print('正在创建文件夹......')
        dir_path = os.path.join('D:\桌面\桃隐', html_title)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print('已创建文件夹：',dir_path, '\n')
        else:
            print('文件夹已存在，无需再次创建\n')
        return dir_path
    
    
    def save_html_source_code(self, dir_path, html_title, html_source_code):
    
        print('正在保存网页源文件......')
        file_path = os.path.join(dir_path, html_title+'.txt')
        html_source_code_txt = open(file_path, 'w', encoding='utf-8')
        html_source_code_txt.write(html_source_code)
        html_source_code_txt.close()
        print('已保存网页源文件：%s.txt\n' % html_title)
    
    
    def get_html_type(self, html_source_code):
    
        '''
        1：无<div class="pattl">，正文内容全部在第一个<td class="t_f"。。。>的标签内
        2：有<div class="pattl">，第一个图片前的文字在第一个<td class="t_f"。。。>标签内，其余正文内容全部在<div class="pattl">内
        '''
        
        if re.search(r'<div class="pattl">', html_source_code):
            print('本网页类型为2，有<div class="pattl">\n')
            return 2
        else:
            print('本网页类型为1，无<div class="pattl">\n')
            return 1
    
    
    def make_new_html(self, html_source_code, html_type):
    
        if html_type == 1:
            
            soup = BeautifulSoup(html_source_code,'lxml')
            content = soup.find('td', class_='t_f')
            img_names = [img_name['file'].split('/')[-1] for img_name in content.find_all('img')]
            
            pre_img_formats = re.findall(r'<img.+?/>',str(content))
            
            new_html_source_code = str(content)
            new_html_source_code = re.sub(r'<td.+?>','',new_html_source_code)
            new_html_source_code = re.sub(r'</td>','',new_html_source_code)
            
            for i in range(len(pre_img_formats)):
                after_img_formot = r'<img src="' + img_names[i] + r'"/>'
                new_html_source_code = new_html_source_code.replace(pre_img_formats[i], after_img_formot)
            
            html_frame = dedent('''\
                                <html>
                                <title>
                                </title>
                                <body bgcolor="#C0C0C0">
                                </body>
                                </html>
                                ''')
            
            new_html_source_code = html_frame[:html_frame.index('</body>')] + new_html_source_code + html_frame[html_frame.index('</body>'):]
            
            return new_html_source_code
            
        elif html_type == 2:
            pass
    
    
    def save_new_html(self, dir_path, html_title, new_html_source_code):
        print('正在保存净化后的网页源文件......')
        file_path = os.path.join(dir_path, html_title+'.html')
        new_html_file = open(file_path, 'w', encoding='utf-8')
        new_html_file.write(new_html_source_code)
        new_html_file.close()
        print('已保存净化后的网页源文件：%s.html\n' % html_title)
    
    
    def get_img_urls(self, html_source_code, html_type, dir_path):
    
        print('正在获取图片网址')
        
        if html_type == 1:
            
            soup = BeautifulSoup(html_source_code,'lxml')
            content = soup.find('td', class_='t_f')
            img_urls = [img_name['file'] for img_name in content.find_all('img')]
            
            self.img_amount =len(img_urls)
            print('获取成功！本网页共有%d张目标图片\n' % self.img_amount)
            
            
            img_dict = {'url':'', 'img_number':0, 'dir_path':''}
            img_list = []
            for img_number, img_url in enumerate(img_urls):
                img_dict['url'] = img_url
                img_dict['img_number'] = img_number
                img_dict['dir_path'] = dir_path
                img_list.append(copy.deepcopy(img_dict))    #深拷贝，如果不用copy.deepcopy()，则img_list中的所有元素都会是最后一个赋值的
            
            return img_list
        
        elif html_type == 2:
            pass
    
    
    def get_and_save_img(self, img_dict, run_time):
        
        img_url = img_dict['url']
        img_number = img_dict['img_number']
        img_dir_path = img_dict['dir_path']
        
        print('正在向图%d发送第%d次请求......' % (img_number+1, run_time+1))
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
            response = request.urlopen(req, timeout=3)    #请求超过3秒则停止此次请求
            
            img = response.read()
            print('请求成功!')
            
            print('正在保存图%d......' % (img_number+1))
            
            img_name = img_url.split('/')[-1]
            file_path = os.path.join(img_dir_path, img_name)
            
            f = open(file_path, 'wb+')
            f.write(img)
            f.close()
            
            print('保存成功！')
            
            self.success_img_amount += 1
            print('进度%d/%d\n' % (self.success_img_amount, self.img_amount))
            
        except Exception as e:
            
            print('发生错误：%s\n自动记录并跳过此图片' % e)
            self.failed_img_list.append(copy.deepcopy(img_dict))
            print('进度%d/%d\n' % (self.success_img_amount, self.img_amount))