import crawler_for_single_url as crawler


def get_and_save_one_img(url, i, run_time, success):

    get_img(url, i,run_time)


if __name__ == '__main__':

    f = 'taoyin_urls.txt'
    urls_list = []
    for url in open(f):
        urls_list.append(url[:-1])  #切掉'\n'

    failed_urls_dict = {}
    no_img_urls = []
    
    for i, url in enumerate(urls_list):

        print('第%d个网页\n网址为%s\n' % (i+1, url))
        crawler.crawler_for_single_url(url)

        
        if crawler.failed_img_urls_dict:
            for img_url in crawler.failed_img_urls_dict.values():
                failed_urls_dict[img_url] = crawler.path

        
        if crawler.img_amount == 0:
            no_img_urls.append(url)
            
    print('\n\n\n有以下图片下载失败：')
    for i, url in enumerate(failed_urls_dict):
        print('图%d:%s' % (i+1, url))

    print('\n尝试重新下载：')
    for run_time in range(0,40):  #加上之前的10次，最高尝试次数可达50次
        for i, url in enumerate(failed_urls_dict.values()):
            get_and_save_one_img(url, i, run_time+10)
