import re, os, time, random, copy, traceback, threading
from textwrap import dedent
import requests
from bs4 import BeautifulSoup


class Spider():
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cookie': '__cfduid=dfbd3bfcc491ef2d524cb01f94678f1a21564466775; UM_distinctid=16c417c9f7d3fb-0a58d345bb1e61-c343162-1fa400-16c417c9f7e997; imalready18y=OK; slimitenter=y; pDXj_2132_saltkey=j1Ne6eAI; pDXj_2132_lastvisit=1564463088; CNZZDATA1255696574=295174311-1564462761-http%253A%252F%252Factive.taoy360.info%252F%7C1564462553; pDXj_2132_st_t=0%7C1564466772%7Ce8e1095e912b4a1e3deb6bb875d0c0a4; pDXj_2132_atarget=1; pDXj_2132_forum_lastvisit=D_36_1564466772; pDXj_2132_st_p=0%7C1564467409%7C99d5834b663cec7eb6d5d4fbba4e496e; pDXj_2132_viewid=tid_815460; pDXj_2132_lastact=1564467552%09forum.php%09ajax',
                }    #桃隐网页
    
    def __init__(self, url=''):
        self.url = url
        self.domain_name = 'wwvv.taoy2.vip'
        self.url_num = 0    #帖子序号
        self.retry = 3    #请求次数
        self.timeout = 10    #超时时间
        self.thread_num = 10    #线程数
        self.html_source_code = ''
        self.html_title = ''
        self.sub_path = ''    #子路径，如：桃隐社区\H漫画同人汉化字幕\以网页标题命名的文件夹
        self.root_path = r''    #默认根目录为本程序所在目录
        self.dir_path = ''
        self.html_type = -1
        self.new_html_source_code = ''
        self.img_amount = 0
        self.img_list = []
        self.success_img_amount = 0
        self.failed_img_list = []    #里面嵌套着多个failed_img_dict = {'url_num':'', 'img_url':'', 'dir_path':''}
        self.rlock = threading.RLock()    #线程锁
    
    
    def correct_url(self):
        while True:
            #输入的是帖子序号
            if re.match(r'\d+',self.url):    
                self.url_num = self.url
                self.url = 'http://' + self.domain_name + '/thread-' + self.url + '-1-1.html'
                print()
                return self.url
            
            #输入的是帖子网址
            url_num = re.search(r'((?<=tid=)\d+)|((?<=thread-)\d+?(?=-1-1))', self.url)    
            if url_num:
                self.url_num = url_num.group()
                self.url = 'http://' + self.domain_name + '/thread-' + url_num.group() + '-1-1.html'
                print()
                return self.url
            
            else:
                if traceback.extract_stack()[-4][2] == 'pages':
                    print('\nURL格式不符合桃隐网址的命名规则，对于本网页的任务中止\n')
                    return False
                else:    #单独运行crawler_for_single_url()时，url不正确则重新输入
                    self.url = input('URL格式不符合桃隐网址的命名规则，请重新输入：\n')
    
    
    #若已爬取、不存在、权限不足，则跳过
    def pass_url(self):
        print('网址：',self.url)
        if os.path.exists('SAVED.txt'):
            with open('SAVED.txt','r', encoding='utf-8') as f:
                for img_num in f:
                    if img_num[:-1] == self.url_num:
                        print('序号为%s的帖子已经爬取过了，对于本网页的任务中止\n' 
                              % self.url_num)
                        return True
        if os.path.exists('NO EXIST.txt'):
            with open('NO EXIST.txt','r', encoding='utf-8') as f:
                for img_num in f:
                    if img_num[:-1] == self.url_num:
                        print('序号为%s的帖子已确认不存在，对于本网页的任务中止\n' 
                              % self.url_num)
                        return True
        if os.path.exists('NO JURISDICTION.txt'):     
            with open('NO JURISDICTION.txt','r', encoding='utf-8') as f:
                for img_num in f:
                    if img_num[:-1] == self.url_num:
                        print('序号为%s的帖子确认无权查看，对于本网页的任务中止\n' 
                              % self.url_num)
                        return True
        return False
            
    
    def repeat_request(self, url, headers={}):
        for _ in range(self.retry):
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout).content
                if len(response) > 500:
                    return response
                    break
            except Exception as e:
                print(e)
                

    def no_alert_error(self):
        soup = BeautifulSoup(self.html_source_code, 'lxml')  
        
        content = soup.find('div', class_='alert_error')
        if content:
            content = content.find('p')
            alert_error = re.sub('\s','',content.text)
            print(alert_error,'，对于本网页的任务中止\n')
            if re.search(r'(指定的主题不存在或已被删除或正在被审核)|(没有找到帖子)'
                         ,alert_error):
                with open('NO EXIST.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_num+'\n')
                    print('已向NO EXIST.txt写入贴子%s不存在的信息'
                          %self.url_num)
            if re.search(r'权限',alert_error):
                with open('NO JURISDICTION.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_num+'\n')
                    print('已向NO JURISDICTION.txt写入贴子%s无权限的信息'
                          %self.url_num)
            return False
        
        content = soup.find('div',class_='alert_info')
        if content:
            content = content.find('p')
            alert_info = re.sub('\s','',content.text)
            print(alert_info,'，对于本网页的任务中止\n')
            if re.search(r'权限',alert_info):
                with open('NO JURISDICTION.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_num+'\n')
                    print('已向NO JURISDICTION.txt写入贴子%s无权限的信息'
                          %self.url_num)
            return False
        return True 
    
    
    def get_html_title(self):
        print('正在获取网页标题......')
        soup = BeautifulSoup(self.html_source_code,'lxml')
        self.html_title = soup.find('title').string
        if self.html_title:
            self.html_title = re.sub(r'^\s+(?=[^\s])','',self.html_title)
            self.html_title = re.sub(r'(?<=[^\s])\s+$','',self.html_title)
            #删掉短段前段后的空白字符
            print('网页<title>为：%s' % self.html_title)
            if len(self.html_title.split(' ')) >= 4 and self.html_title.split(' ')[-3] == '-':    #特例786590：已经绑好了 就等你来了哦 - 国产自拍|偷拍|艳照 桃隐社区
                self.html_title = re.sub(r'[\\\*\?\|/:"<>\.]', '', self.html_title)
                root = self.html_title.split(' ')[-1]
                second = self.html_title.split(' ')[-2]
                self.html_title = re.sub(' - .+?$', '', self.html_title)
                if self.html_title:
                    self.sub_path = os.path.join(root,second,self.html_title)
                print('网页标题为：', self.html_title, '\n')
                return self.html_title
            else:
                print('网页<title>并非"题目 - 子区 桃隐社区"的格式，对于本网页的任务中止\n')
        else:
            print('获取网页标题失败，对于本网页的任务中止\n')
    
    
    def make_dir(self):
        print('正在创建文件夹......')        
        self.dir_path = os.path.join(self.root_path, self.sub_path)
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
            print('已创建文件夹：',self.dir_path, '\n')
        else:
            print('文件夹已存在，无需再次创建\n')
        return self.dir_path
    
    
    def save_html_source_code(self):
        print('正在保存网页源文件......')
        file_name = self.url_num + '：' + self.html_title+ '.txt'
        file_path = os.path.join(self.dir_path, file_name)
        html_source_code_txt = open(file_path, 'w', encoding='utf-8')
        html_source_code_txt.write(self.html_source_code)
        html_source_code_txt.close()
        print('已保存网页源文件：%s\n' % file_name)
        return True
            

    def get_html_type(self):
        '''
        1：无<div class="pattl">，正文内容全部在第一个<td class="t_f"。。。>的标签内
        2：有<div class="pattl">，第一个图片前的文字在第一个<td class="t_f"。。。>标签内，其余正文内容全部在<div class="pattl">内
        '''
        if re.search(r'<div class="pattl">', self.html_source_code):
            print('本网页类型为2，有<div class="pattl">\n')
            self.html_type = 2
        elif re.search(r'<td class="t_f"', self.html_source_code):
            print('本网页类型为1，无<div class="pattl">\n')
            self.html_type = 1
        else:
            self.html_type = 0
        return self.html_type
            
            
    def make_new_html(self):
        html_frame = dedent('''\
                            <html>
                             <head>
                              <title>
                              </title>
                              <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                             </head>
                             <body bgcolor="#00FFFF">
                              <div style="margin:40px ; text-align:center;">
                               <a href="" style="color:red;text-decoration:none;">
                                <h1>
                                </h1>
                               </a>
                              </div>
                             </body>
                            </html>
                            ''')
        if self.html_type == 1:
            soup = BeautifulSoup(self.html_source_code,'lxml')
            content = soup.find('td', class_='t_f')
            [s.extract() for s in content('i')]
            
            img_names = []
            wrong_tag = 0
            for img_name in content.find_all('img'):
                if img_name.has_attr('file'):
                    img_names.append(img_name['file'].split('/')[-1])
                else:
                    wrong_tag+=1
            '''
            发现了一个毒瘤（790614）：
            根据<img>提取出来的图片，还有这种情况，是广告图片，要加个判断
            <img src="static/image/smiley/default/handshake.gif" smilieid="23" border="0" alt="" />
            '''
            
            pre_img_formats = re.findall(r'<img.+?/>',str(content))
            
            self.new_html_source_code = str(content)
            self.new_html_source_code = re.sub(r'<td.+?>','',self.new_html_source_code)
            self.new_html_source_code = re.sub(r'</td>','',self.new_html_source_code)
            
            for i in range(len(pre_img_formats)-wrong_tag):
                after_img_formot = r'<img src="' + img_names[i] + r'"/>'
                self.new_html_source_code = self.new_html_source_code.replace(pre_img_formats[i], after_img_formot)
            
            self.new_html_source_code = html_frame[:html_frame.index('</title>')] + self.html_title + \
                                   html_frame[html_frame.index('</title>'):html_frame.index('" style')] + self.url + \
                                   html_frame[html_frame.index('" style'):html_frame.index('</h1>')] + self.html_title + \
                                   html_frame[html_frame.index('</h1>'):html_frame.index('</div>')] + self.new_html_source_code + \
                                   html_frame[html_frame.index('</div>'):]
            
            new_html_soup = BeautifulSoup(self.new_html_source_code, 'lxml')
            self.new_html_source_code = str(new_html_soup.prettify())
            
            return self.new_html_source_code 
            
        elif self.html_type == 2:
            
            '''
            干扰项太多了，直接把<div class="pattl">和第一个<td class="t_f"...>
            标签的内容“粘贴”到新的html框架中，再将图片标签修改<img src="...(本地路径)...">
            这样网页源代码会很复杂、不简洁，但干扰项的一个个删除太繁琐了
            '''
            
            soup = BeautifulSoup(self.html_source_code,'lxml')
            
            self.new_html_source_code = html_frame[:html_frame.index('</title>')] + self.html_title + html_frame[html_frame.index('</title>'):]
            
            self.new_html_source_code = html_frame[:html_frame.index('</title>')] + self.html_title + \
                                   html_frame[html_frame.index('</title>'):html_frame.index('" style')] + self.url + \
                                   html_frame[html_frame.index('" style'):html_frame.index('</h1>')] + self.html_title + \
                                   html_frame[html_frame.index('</h1>'):]
            
            first_part_soup = soup.find('td', class_='t_f')
            [s.extract() for s in first_part_soup('i')]
            self.new_html_source_code = self.new_html_source_code[:self.new_html_source_code.index('</div>')] + str(first_part_soup) + self.new_html_source_code[self.new_html_source_code.index('</div>'):]
            
            other_part_soup = soup.find('div', class_='pattl')
            self.new_html_source_code = self.new_html_source_code[:self.new_html_source_code.index('</div>')] + str(other_part_soup) + self.new_html_source_code[self.new_html_source_code.index('</div>'):]

            img_list_soup = soup.select('div.mbn.savephotop img')
            img_names = []
            for img_name in img_list_soup:
                if img_name.has_attr('zoomfile'):
                    img_names.append(img_name['zoomfile'].split('/')[-1])
            
            pre_img_formats = [str(img_name) for img_name in img_list_soup]
            
            for i in range(len(pre_img_formats)):
                after_img_formot = r'<img src="' + img_names[i] + r'"/>'
                self.new_html_source_code = self.new_html_source_code.replace(pre_img_formats[i], after_img_formot)

            new_html_soup = BeautifulSoup(self.new_html_source_code, 'lxml')
            self.new_html_source_code = str(new_html_soup.prettify())
            
            return self.new_html_source_code     
        
        else:
            print('网页类型并非1或2，，对于本网页的任务中止\n')
            return None
        
        
    def save_new_html(self):
        print('正在保存净化后的网页源文件......')
        file_path = os.path.join(self.dir_path, self.html_title+'.html')
        new_html_file = open(file_path, 'w', encoding='utf-8')
        new_html_file.write(self.new_html_source_code)
        new_html_file.close()
        print('已保存净化后的网页源文件：%s.html\n' % self.html_title)      
        return True
    

    def get_resource_download_link(self):    #获取资源下载链接
        soup = BeautifulSoup(self.new_html_source_code, 'lxml')
        div = soup.body.div
        [s.extract() for s in soup("h1")]
        [s.extract() for s in soup("ignore_js_op")]
        txt = str(div.text)
        txt = re.sub(r'\n', '', txt)
        txt = re.sub(r' +','\n', txt)
        if re.search(r'[a-zA-z]+://[^\s]*', txt):
            with open('Download Link.txt', 'a+', encoding='utf-8') as f:
                first_line = self.url_num + '：' + self.html_title + '\n'
                f.write(first_line + txt + '\n\n\n')
            print('发现资源下载链接，已以追加方式写入\
                  本程序所在目录下的Download Link.txt\n')
        return True


    def get_img_urls(self):
        print('正在获取图片网址')
        soup = BeautifulSoup(self.html_source_code,'lxml')
        if self.html_type == 1:
            content = soup.find('td', class_='t_f')
            img_urls_list = []
            for img_name in content.find_all('img'):
                if img_name.has_attr('file'):
                    img_urls_list.append(img_name['file'])
        elif self.html_type == 2: 
            img_list_soup = soup.select('div.mbn.savephotop img')
            img_urls_list = []
            for img_name in img_list_soup:
                if img_name.has_attr('zoomfile'):
                    img_urls_list.append(img_name['zoomfile'])
        self.img_amount =len(img_urls_list)
        if self.img_amount == 0:
            print('由于未获取到任一目标图片，对于本网页的任务中止\n')
        else:
            img_dict = {'url_num':'', 'img_url':'', 'dir_path':''}
            self.img_list = []
            for img_number, img_url in enumerate(img_urls_list):
                img_dict['url_num'] = self.url_num
                img_dict['img_url'] = img_url
                img_dict['dir_path'] = self.dir_path
                self.img_list.append(copy.deepcopy(img_dict))    #深拷贝，如果不用copy.deepcopy()，则img_list中的所有元素都会是最后一个赋值的 
            print('获取成功！本网页共有%d张目标图片\n' % self.img_amount)
            return self.img_list
    
    
    def add_error_img(self, img_dict):
        already_added = False
        if os.path.exists('ERROR.txt'):
            with open('ERROR.txt','r', encoding='utf-8') as f:
                for line in f:
                    if str(img_dict) == line[:-1]:
                        already_added = True
        if not already_added:
            with open('ERROR.txt', 'a+', encoding='utf-8') as f:
                f.write(str(img_dict)+'\n')
    
    
    def down_one_img(self, img_url, dir_path):
        img_data = self.repeat_request(img_url)
        if img_data:
            print('请求成功! 正在保存...')
            print(img_url)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            img_name = img_url.split('/')[-1]
            file_path = os.path.join(dir_path, img_name)    
            with open(file_path, 'wb+') as f:
                f.write(img_data)
            print('保存成功！')
            self.success_img_amount += 1
            print('进度%d/%d\n' % (self.success_img_amount, self.img_amount))
            return True
        else:
            print('失败：%s'%img_url)
            return False


    def thread_func(self):
        while True:
            self.rlock.acquire()    #加线程锁，同一时间只能有一个线程运行此段代码
            if len(self.img_list) == 0:
                self.rlock.release()    #释放线程锁
                break
            else:
                img_dict = self.img_list.pop()
                self.rlock.release()    #释放线程锁
                url_num = img_dict['url_num']
                img_url = img_dict['img_url']
                dir_path = img_dict['dir_path']
                try:
                    if not self.down_one_img(img_url, dir_path):
                        print('失败：%s'%img_url)
                        self.add_error_img(img_dict)
                except Exception as e:
                    print(e)
                    print('失败：%s'%img_url)
                    self.add_error_img(img_dict)


    def get_html(self):
        if self.correct_url():
            if not self.pass_url():
                self.html_source_code = (self.repeat_request(self.url, headers=self.headers))
                if self.html_source_code:
                    self.html_source_code = self.html_source_code.decode('utf-8')
                    if self.no_alert_error():
                        if self.get_html_title():
                            if self.make_dir():
                                if self.save_html_source_code():
                                    return True

    def new_html(self):
        if self.get_html_type():
            if self.make_new_html():
                if self.save_new_html():
                    if self.get_resource_download_link():   #网盘链接
                        return True
                    
                    
    def imgs(self):
        if self.get_img_urls():
            thread_list = []
            for _ in range(self.thread_num):
                t = threading.Thread(target=self.thread_func)
                thread_list.append(t)
                t.start()
            for t in thread_list:
                t.join()
            print('图片共%d张，成功%d张，失败%d张'%(self.img_amount, 
                   self.success_img_amount, self.img_amount-self.success_img_amount))
            with open('SAVED.txt','a+', encoding='utf-8') as f:
                f.write(self.url_num+'\n')
            return True

            
def one_page(url):
    spider = Spider(url)
    if spider.get_html():
        if spider.new_html():
            spider.imgs()
                
    
if __name__ == '__main__':
    start = time.perf_counter()
    url = input('请输入网址：')
    one_page(url)
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))
