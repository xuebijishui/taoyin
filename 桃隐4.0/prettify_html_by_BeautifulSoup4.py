from bs4 import BeautifulSoup

f = open('745164.txt','r',encoding='utf-8')
html_doc = f.read()
f.close()

soup = BeautifulSoup(html_doc,'lxml')

f = open('745164.txt','w',encoding='utf-8')
f.write(soup.prettify())
f.close()