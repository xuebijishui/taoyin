#从导出收藏夹的网页中提取出桃隐帖子的网址

import re

f = open('bookmarks_2019_6_18.html', 'r', encoding='utf-8')
content = f.read()
f.close()

pattern = re.compile(r'https?://[^/]*?taoy.+?(?=" ADD_DATE)')
urls = pattern.findall(content)
print(len(urls))
f = open('taoyin_urls.txt', 'w')
for url in urls:
    f.write(url+'\n')
f.close()
