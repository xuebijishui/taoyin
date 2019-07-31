import re, os, time, random, copy, traceback  #copy深拷贝
from textwrap import dedent    #通过缩进美化多行字符串在源代码中的显示
import requests
from bs4 import BeautifulSoup


class Crawler:
    
    def __init__(self, url=''):
        self.url = url
        self.domain_name = 'c.taoy66.vip'
        self.urls_file = 'taoyin_urls.txt'
        self.url_serial_number = 0    #帖子序号
        self.retry = 3    #请求次数
        self.timeout = 10    #超时时间
        self.html_source_code = ''
        self.html_title = ''
        self.sub_path = ''    #子路径，如：桃隐社区\H漫画同人汉化字幕\以网页标题命名的文件夹
        self.root_path = r''    #默认根目录为本程序所在目录
        self.dir_path = ''
        self.html_type = -1
        self.new_html_source_code = ''
        self.img_amount = 0
        self.success_img_amount = 0
        self.failed_img_list = []    #里面嵌套着多个failed_img_dict = {'url_serial_number':'', 'img_url':'', 'img_number':0, 'dir_path':''}


    def correct_url(self,url=''):
        """
        桃隐的域名经常改变，以前收藏的网址会打不开，但是只要从中提取出该网页的编号，拼接到可用的域名中就能再次访问
        桃隐的网址传值方法有两种，如：
        http://c.taoy66.vip/forum.php?mod=viewthread&tid=694604
        http://c.taoy66.vip/thread-694604-1-1.html
        上面两个网址可以进入编号为694604的帖子,本程序默认使用后者
        """
        self.url = url
        while True:
            if re.match(r'\d+',self.url):    #输入的是帖子序号
                self.url_serial_number = self.url
                self.url = 'http://' + self.domain_name + '/thread-' + self.url + '-1-1.html'
                print()
                return self.url

            url_number = re.search(r'((?<=tid=)\d+)|((?<=thread-)\d+?(?=-1-1))', self.url)    #输入的是帖子网址
            if url_number:
                self.url_serial_number = url_number.group()
                self.url = 'http://' + self.domain_name + '/thread-' + url_number.group() + '-1-1.html'
                print()
                return self.url
            else:
                call = traceback.extract_stack()[-3][2]
                if call == 'crawler_for_multiple_urls':
                    print('\nURL格式不符合桃隐网址的命名规则，对于本网页的任务中止\n')
                    self.remove_url_from_urls_file()
                    print('已在%s中删除%s\n' % (self.urls_file, self.url))
                    return False
                else:    #单独运行crawler_for_single_url()时，url不正确则重新输入
                    self.url = input('URL格式不符合桃隐网址的命名规则，请重新输入：\n')
            
            
    def is_saved(self, saved_list):
        if self.url_serial_number in saved_list:
            print('序号为%s的帖子已经爬取过了，对于本网页的任务中止\n' % self.url_serial_number)
            call = traceback.extract_stack()[-3][2]
            if call == 'crawler_for_multiple_urls':
                self.remove_url_from_urls_file()
                print('已在%s中删除%s' % (self.urls_file, self.url))
            return True
        return False
    
    def no_exist(self, no_exist_list):
        if self.url_serial_number in no_exist_list:
            print('序号为%s的帖子已确认不存在，对于本网页的任务中止\n' % self.url_serial_number)
            call = traceback.extract_stack()[-3][2]
            if call == 'crawler_for_multiple_urls':
                self.remove_url_from_urls_file()
                print('已在%s中删除%s' % (self.urls_file, self.url))
            return True
        return False
    
    def no_jurisdiction(self, no_jurisdiction_list):
        if self.url_serial_number in no_jurisdiction_list:
            print('序号为%s的帖子已确认不存在，对于本网页的任务中止\n' % self.url_serial_number)
            call = traceback.extract_stack()[-3][2]
            if call == 'crawler_for_multiple_urls':
                self.remove_url_from_urls_file()
                print('已在%s中删除%s' % (self.urls_file, self.url))
            return True
        return False
    
    
    def get_html_source_code(self):
        print('正在访问%s\n正在获取网页源代码......' % self.url)
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
        for i in range(self.retry):    #尝试请求10次
            try:
                response = requests.get(url=self.url, headers=headers, timeout=self.timeout)
                self.html_source_code = response.content.decode('utf-8')
                print('获取成功！\n')
                return self.html_source_code
            except Exception as e:
                if i < self.retry-1:
                    pause = random.uniform(0.5, 1)
                    print('发生错误：%s    %.2f秒后再次尝试' % (e,pause))
                    time.sleep(pause)
                    print('重新尝试获取网页源代码......')
                else:
                    print('获取网页源代码失败，对于本网页的任务中止\n')
    
    
    def no_alert_error(self):
        '''
        已知有：
        
        150002：抱歉，指定的主题不存在或已被删除或正在被审核
        477429：没有找到帖子
        716202：抱歉，您没有权限访问该版块
        格式如下：
        <div class="alert_error" id="messagetext">
         <p>
          抱歉，指定的主题不存在或已被删除或正在被审核
         </p>
         <script type="text/javascript">
          ...
         </script>
        </div>
        
        745164：抱歉，本帖要求阅读权限高于 5 才能浏览
        maybeALL：例行维护～预计11&#58;00完成
        格式如下：
        <div class="alert_info" id="messagetext">
         <p>
          抱歉，本帖要求阅读权限高于 5 才能浏览
         </p>
        </div>
        '''
        soup = BeautifulSoup(self.html_source_code, 'lxml')    
        
        content = soup.find('div', class_='alert_error')
        if content:
            content = content.find('p')
            alert_error = re.sub('\s','',content.text)
            print(alert_error,'，对于本网页的任务中止\n')
            if re.search(r'(指定的主题不存在或已被删除或正在被审核)|(没有找到帖子)',alert_error):
                with open('NO EXIST.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_serial_number+'\n')
                    print('已向NO EXIST.txt写入贴子%s不存在的信息'%self.url_serial_number)
                call = traceback.extract_stack()[-3][2]
                if call == 'crawler_for_multiple_urls':
                    self.remove_url_from_urls_file()
                    print('已在%s中删除%s\n' % (self.urls_file, self.url))
            if re.search(r'权限',alert_error):
                with open('NO JURISDICTION.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_serial_number+'\n')
                    print('已向NO JURISDICTION.txt写入贴子%s无权限的信息'%self.url_serial_number)
                call = traceback.extract_stack()[-3][2]
                if call == 'crawler_for_multiple_urls':
                    self.remove_url_from_urls_file()
                    print('已在%s中删除%s\n' % (self.urls_file, self.url))
            return False
        
        content = soup.find('div',class_='alert_info')
        if content:
            content = content.find('p')
            alert_info = re.sub('\s','',content.text)
            print(alert_info,'，对于本网页的任务中止\n')
            if re.search(r'权限',alert_info):
                with open('NO JURISDICTION.txt','a+',encoding='utf-8') as f:
                    f.write(self.url_serial_number+'\n')
                    print('已向NO JURISDICTION.txt写入贴子%s无权限的信息'%self.url_serial_number)
                self.remove_url_from_urls_file()
                print('已在%s中删除%s\n' % (self.urls_file, self.url))
            return False
        return True


    def get_html_title(self):
        '''
        我以为通过判断html_source_code是否为空就能知道是否请求成功，但万万没想到校园网太毒瘤了
        断网后仍然能获取网页源码，只不过是下面的源码
        <script>top.self.location.href='http://10.2.5.251/a79.htm?wlanuserip=10.4.18.17&wlanacname=NAS&ssid=Ruijie&nasip=10.2.4.1&mac=302432c506a7&t=wireless-v2-plain&url=http://c.taoy66.vip/thread-2884-1-1.html'</script>
        直接劫持了我的网页请求，但是我就不额外加判断的语句了，自己注意吧
        报错：
        File "D:\桌面\crawler_class.py", line 168, in get_html_title
        html_title = soup.find('title').string
        AttributeError: 'NoneType' object has no attribute 'string'
        源码不为空，且又没有<title>，很容易理解为何报错
        '''
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
        file_name = self.url_serial_number + '：' + self.html_title+ '.txt'
        file_path = os.path.join(self.dir_path, file_name)
        html_source_code_txt = open(file_path, 'w', encoding='utf-8')
        html_source_code_txt.write(self.html_source_code)
        html_source_code_txt.close()
        print('已保存网页源文件：%s\n' % file_name)
        
        
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
        

    def get_resource_download_link(self):    #获取资源下载链接
        '''
        获取正文内容，删除<h1></h1>，对于类型2的网页，
        还要删除<ignore_js_op></ignore_js_op>（当然这个标签内的文字也会被删除），
        但是，下载链接不都应该在文末吗，所以应该不用担心，况且类型2我还真没见到过带有资源下载链接的
        由于各种类型的下载链接都有，还有压缩密码，提取密码等，
        提取时可能会少提取一些，比如落下压缩密码等，所以还是不提取出具体的链接吧，直接把所有的文字搞出来
        '''
        soup = BeautifulSoup(self.new_html_source_code, 'lxml')
        div = soup.body.div
        [s.extract() for s in soup("h1")]
        [s.extract() for s in soup("ignore_js_op")]
        txt = str(div.text)
        txt = re.sub(r'\n', '', txt)
        txt = re.sub(r' +','\n', txt)
        if re.search(r'[a-zA-z]+://[^\s]*', txt):
            with open('Download Link.txt', 'a+', encoding='utf-8') as f:
                first_line = self.url_serial_number + '：' + self.html_title + '\n'
                f.write(first_line + txt + '\n\n\n')
            print('发现资源下载链接，已以追加方式写入本程序所在目录下的Download Link.txt\n')
            
            
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
        print('获取成功！本网页共有%d张目标图片\n' % self.img_amount)
                
        img_dict = {'url_serial_number':'', 'img_url':'', 'img_number':0, 'dir_path':''}
        img_list = []
        for img_number, img_url in enumerate(img_urls_list):
            img_dict['url_serial_number'] = self.url_serial_number
            img_dict['img_url'] = img_url
            img_dict['img_number'] = img_number+1    #下标从1开始
            img_dict['dir_path'] = self.dir_path
            img_list.append(copy.deepcopy(img_dict))    #深拷贝，如果不用copy.deepcopy()，则img_list中的所有元素都会是最后一个赋值的 
        if img_list:
            return img_list
        else:
            print('由于未获取到任一目标图片，对于本网页的任务中止\n')


    def add_failed_img_to_ERRORtxt(self, img_dict):
        '''
        若此图片信息未在ERROR.txt中，则添加此图片信息
          
        失败图片信息已在ERROR.txt中，是因为上一次的爬取任务中途停止了
        若一个页面（记为A）完整地运行完了，则会在SAVED.txt中写入编号，在ERROR.txt中写入失败图片信息
        而一个页面（记为B）只是运行到中途就停止了，并不会在SAVED.txt中写入编号，只是在ERROR.txt中写入失败图片信息
        这样，下次运行程序时，遇到A，直接跳过，而遇到B，会运行，重新开始爬取，这时可能会遇到之前已经写入过的失败图片信息的情况
        （当然B这种情况，可能会重复地下载某些图片，因为下次运行程序，对于B，并不会检测图片下载成功与否，
        但是因为半途中止运行只会使最多一个帖子内的图片重复爬取（前面的都SAVED了），而一个网页内的目标图片并不会太多，也就几十张，所以可以接受）
        （这一步骤的主要目的是为了crawler_for_img_of_ERRORtxt.py的半途中止运行，因为它运行一个循环（指ERROR.txt的所有图片都请求一遍）很耗时间，
        万一半途中止运行，重复爬取的图片量可能会很大。这样一搞，成功的图片会立刻从ERROR.txt中删除，下次再运行并不会再次爬取了）
        '''
        already_added = False
        if os.path.exists('ERROR.txt'):
            with open('ERROR.txt','r', encoding='utf-8') as f:
                for line in f:
                    if str(img_dict) == line[:-1]:
                        already_added = True
        if not already_added:
            with open('ERROR.txt', 'a+', encoding='utf-8') as f:
                f.write(str(img_dict)+'\n')
    
    
    def delete_the_nth_line_in_file(self, file, del_line):    #从网上搞来的轮子,del_line为行数  
        with open(file, 'r', encoding='utf-8') as old_file:
            with open(file, 'r+', encoding='utf-8') as new_file:         
                current_line = 0             
                # 定位到需要删除的行
                while current_line < (del_line - 1):
                  old_file.readline()
                  current_line += 1             
                # 当前光标在被删除行的行首，记录该位置
                seek_point = old_file.tell()             
                # 设置光标位置
                new_file.seek(seek_point, 0)             
                # 读需要删除的行，光标移到下一行行首
                old_file.readline()                 
                # 被删除行的下一行读给 next_line
                next_line = old_file.readline()
                # 连续覆盖剩余行，后面所有行上移一行
                while next_line:
                  new_file.write(next_line)
                  next_line = old_file.readline()
                # 写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉
                new_file.truncate()
    
    
    def remove_successful_img_from_ERRORtxt(self, img_dict):
        finded = False
        if os.path.exists('ERROR.txt'):
            with open('ERROR.txt', 'r', encoding='utf-8') as f:
                for img_number, line in enumerate(f):
                    if line[:-1] == str(img_dict):
                        finded = True
                        break
        if finded:
            self.delete_the_nth_line_in_file('ERROR.txt', img_number+1)    #索引从0来时，行号从1开始

    
    def remove_url_from_urls_file(self):
        #将该url从文本中删除，针对crawler_for_img_multiple_urls.py
        with open(self.urls_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f):
                
                url_serial_number = -1
                
                line = line[:-1]
                
                if re.match(r'\d+',line):    #line是帖子序号
                    url_serial_number = line
                
                url_number = re.search(r'((?<=tid=)\d+)|((?<=thread-)\d+?(?=-1-1))', line)    #line是帖子网址
                if url_number:
                    url_serial_number = url_number.group()
                    
                if url_serial_number == self.url_serial_number:
                    self.delete_the_nth_line_in_file(self.urls_file, line_number+1)
                else:   #提取不出来贴子编号的自然就是错误url
                    if self.url in line:
                        self.delete_the_nth_line_in_file(self.urls_file, line_number+1)


    def get_and_save_img(self, img_dict, run_time):
        url_serial_number = img_dict['url_serial_number']
        img_url = img_dict['img_url']
        img_number = img_dict['img_number']
        img_dir_path = img_dict['dir_path']
        
        print('正在向贴子%s的图%d发送第%d次请求......' % (url_serial_number, img_number, run_time))
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
            response = requests.get(url=img_url, headers=headers, timeout=self.timeout)
            img = response.content
            print('请求成功!')
            print('正在保存图%d......' % (img_number))
            if not os.path.exists(img_dir_path):
                os.makedirs(img_dir_path)      
            img_name = img_url.split('/')[-1]
            file_path = os.path.join(img_dir_path, img_name)    
            with open(file_path, 'wb+') as f:
                f.write(img)
            call = traceback.extract_stack()[-2][2]
            if call == 'crawler_for_multiple_urls' or call == 'crawler_for_img_of_ERROR':
                print('图片已保存至：%s' % img_dir_path)
            else:
                print('保存成功！')
            self.success_img_amount += 1
            print('进度%d/%d\n' % (self.success_img_amount, self.img_amount))
            return True
        except Exception as e:
            call = traceback.extract_stack()[-2][2]
            if call == 'crawler_for_multiple_urls' or call == 'crawler_for_img_of_ERROR':
                print('发生错误：%s' % e)
                print('此图片应位于%s' % img_dir_path)
                print('自动记录并跳过此图片')
            else:
                print('发生错误：%s\n自动记录并跳过此图片' % e)
            self.failed_img_list.append(copy.deepcopy(img_dict))
            print('进度：%d/%d\n' % (self.success_img_amount, self.img_amount))
            return False