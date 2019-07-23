#从导出收藏夹的网页中提取出桃隐帖子的网址

import re

f = open('bookmarks_2019_7_23.html', 'r', encoding='utf-8')
content = f.read()
f.close()

pattern = re.compile(r'https?://[^/]*?taoy.+?(?=" ADD_DATE)')
urls = pattern.findall(content)
f = open('taoyin_urls.txt', 'w')
for url in urls:
    f.write(url+'\n')
print('共有%d个目标网址，已保存至本程序所在目录下的taoyin_urls.txt中' % len(urls))
f.close()
