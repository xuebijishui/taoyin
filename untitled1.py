import re
from urllib import request

f = open('桃隐.txt', 'r', encoding='utf-8')
html = f.read()
f.close()

headers = {'Host' : 'www.sehuatuchuang.com',
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

pattern = re.compile(r'https://www\.sehuatuchuang\.com/images/\d{4}/\d{2}/\d{2}/\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))',flags=re.I)
img_urls = pattern.finditer(html)

for img_url in img_urls:
    img_name = re.search(r'\w+?\.((png)|(jpg)|(gif)|(bmp)|(jpeg)|(webp))', img_url.group(), flags=re.I).group()
    print(img_name)
    
    
    
    req = request.Request(url=img_url.group(),headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200: 
        html = request.urlopen(req).read()
        f = open(img_name,'wb+')
        f.write(html)
        f.close()