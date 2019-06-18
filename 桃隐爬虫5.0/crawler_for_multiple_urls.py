from crawler_class import Crawler_class
import crawler_for_single_url as single
import copy    #深拷贝
import time
import os

def crawler_for_multiple_urls():
    
    #urls_file = input('请将目标urls文件（urls间以换行符间隔）与本程序放在同一目录下，并输入文件名：')
    urls_file = 'taoyin_urls.txt'
    
    crawler = Crawler_class(urls_file)
    
    if __name__ == '__main__':
        print('注意事项：')
        print('1、请确认目前是否可以通过%s访问桃隐，如不能，请在crawler_class.py的Crawler_class类的成员变量中修改domain_name的值为桃隐的最新域名' % crawler.domain_name)
        print('2、默认根目录为%s，如需修改，请在crawler_class.py的Crawler_class类的成员变量中修改default_root_path的值' % crawler.default_root_path)
        print('3、如果之前曾使用过此爬虫，请将生成的SAVED.txt和ERROR.txt放在本程序所在目录下，从而避免同一网页的重复爬取\n')
    
    urls_list = open(urls_file, 'r', encoding='utf-8').readlines()
    urls_list = [url[:-1] for url in urls_list]    #行末有'\n'
    urls_amount = len(urls_list)

    for url_number, url in enumerate(urls_list):
        print('\n爬虫总进度%d/%d' % (url_number+1, urls_amount))
        single.crawler_for_single_url(urls_file, url)
        if single.crawler.failed_img_list:
            for failed_img_dict in single.crawler.failed_img_list:
                crawler.failed_img_list.append(copy.deepcopy(failed_img_dict))
    
    if crawler.failed_img_list:
 
        crawler.img_amount = len(crawler.failed_img_list)
        print('\n\n已完成对所有目标网页的遍历爬取，共有%d张爬取失败的图片，现对失败图片集再次尝试\n' % crawler.img_amount)
        
        for run_time in range(3,5):    #在single.crawler.failed_img_list()内部的向图片的请求次数的基础上
                                
            img_list = crawler.failed_img_list
            crawler.failed_img_list = []
                                
            for img_number, img_dict in enumerate(img_list):                     
                
                is_successful = crawler.get_and_save_img(img_dict, run_time)
                                
                if is_successful:    
                    crawler.remove_successful_img_from_ERRORtxt(img_dict) 
            
            if crawler.failed_img_list:
                print('%d张图片下载失败：' % len(crawler.failed_img_list))
                for failed_img_dict in crawler.failed_img_list:
                    print('贴子%s-图%d：%s' % (failed_img_dict['url_serial_number'], failed_img_dict['img_number'], failed_img_dict['img_url']))
                print()
            '''    
            for img_dict in img_list:                        
                is_successful = crawler.get_and_save_img(img_dict, run_time)
                if run_time == 3 and not is_successful:
                    if os.path.exists('ERROR.txt'):
                                                
                        error_file = open('ERROR.txt','r', encoding='utf-8')
                        error_list = [error[:-1] for error in error_file.readlines()]
                        error_file.close()
                        if img_dict in error_list:
                            error_list.remove(img_dict)
                        else:
                            error_list = []
                                                
                        f = open(r'ERROR.txt','w', encoding='utf-8')
                        for url_information_dict in error_list:
                            f.write(str(url_information_dict)+'\n')
                        f.close()
                                 
            if crawler.failed_img_list:
                                        
                print('%d张图片下载失败：' % len(crawler.failed_img_list))
                for failed_img_dict in crawler.failed_img_list:
                    print('贴子%s-图%d：%s' % (failed_img_dict['url_serial_number'], failed_img_dict['img_number'], failed_img_dict['img_url']))
                print()                                            
              
        if crawler.failed_img_list:
            f = open(r'ERROR.txt','a+', encoding='utf-8')
            for url_information_dict in crawler.failed_img_list:
                f.write(str(url_information_dict)+'\n')
            f.close()
            print('已将下载失败的图片信息以追加方式保存至本程序所在目录下的ERROR.txt\n')
        '''
            
if __name__ == '__main__':
    
    start = time.perf_counter()
    
    crawler_for_multiple_urls()
    
    end = time.perf_counter()
    
    print('任务执行共%.2f秒' % (end-start))