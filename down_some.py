from down_one import one_page
import time

def pages():
    urls_file = 'taoyin_urls.txt'
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls_list = f.readlines()
        urls_list = [url.rstrip('\n') for url in urls_list]    #行末有'\n'
    urls_amount = len(urls_list)
    
    for url_number, url in enumerate(urls_list):
        print('\n爬虫总进度%d/%d' % (url_number+1, urls_amount))
        one_page(url)
    
if __name__ == '__main__':
    start = time.perf_counter()
    pages()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60)) 