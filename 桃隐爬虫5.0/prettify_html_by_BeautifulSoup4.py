from bs4 import BeautifulSoup

file = '790614.txt'

f = open(file,'r',encoding='utf-8')
html_doc = f.read()
f.close()

soup = BeautifulSoup(html_doc,'lxml')

f = open(file,'w',encoding='utf-8')
f.write(soup.prettify())
f.close()
