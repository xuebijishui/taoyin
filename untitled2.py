from urllib import request 
import re



url = 'https://www.sehuatuchuang.com/images/2019/05/26/000.png'
req = request.Request(url=url, headers=headers)
html = request.urlopen(req).read()

f = open('1.png','wb+')
f.write(html)
f.close()