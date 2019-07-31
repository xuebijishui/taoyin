from crawler_class import Crawler
import crawler_for_single_url as single
import copy    #深拷贝
import time
import os


def crawler_for_multiple_urls():
    
    crawler = Crawler()
    
    if __name__ == '__main__':
        print('注意事项：')
        print('1、请确认目前是否可以通过%s访问桃隐，如不能，请在crawler_class.py的Crawler_class类的成员变量中修改domain_name的值为桃隐的最新域名' % crawler.domain_name)
        print('2、默认根目录为本程序所在目录(为了win和linux平台下都能正常爬取)，如需修改，请在crawler_class.py的Crawler_class类的成员变量中修改default_root_path的值')
        print('3、如果之前曾使用过此爬虫，请将生成的SAVED.txt和ERROR.txt放在本程序所在目录下，从而避免同一网页的重复爬取')
        print('4、如果之前未使用过此爬虫，请删除原有的SAVED.txt和ERROR.txt以及Download Link.txt')
        print('5、请将目标urls(也可以是编号)文件(urls间以换行符间隔)与本程序放在同一目录下，并将文件名改为taoyin_urls.txt')
        input('按回车键开始......')
        
    with open(crawler.urls_file, 'r', encoding='utf-8') as f:
        urls_list = f.readlines()
        urls_list = [url[:-1] for url in urls_list]    #行末有'\n'
        urls_amount = len(urls_list)
    
    for url_number, url in enumerate(urls_list):
        print('\n爬虫总进度%d/%d' % (url_number+1, urls_amount))
        single.crawler_for_single_url(url)
    
            
if __name__ == '__main__':   
    start = time.perf_counter()    
    crawler_for_multiple_urls()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))