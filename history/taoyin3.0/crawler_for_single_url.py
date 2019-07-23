from crawler_class import Crawler_class
import time

def crawler_for_single_url():

    crawler = Crawler_class()
        
    url = input('请输入要爬取的网页的网址或编号：\n')
    
    url = crawler.correct_url(url)
    
    if not url is None:
    
        html_source_code = crawler.get_html_source_code(url)
        
        if not html_source_code is None:
            
            if crawler.no_alert_error(html_source_code):
                
                html_title = crawler.get_html_title(html_source_code)
                    
                dir_path = crawler.make_dir(html_title)
                    
                crawler.save_html_source_code(dir_path, html_title, html_source_code)
                
                html_type = crawler.get_html_type(html_source_code)
                    
                new_html_source_code = crawler.make_new_html(html_source_code, html_type)
                
                crawler.save_new_html(dir_path, html_title, new_html_source_code)
                    
                img_list = crawler.get_img_urls(html_source_code, html_type, dir_path)    
                #img_list内嵌套多个img_dict,每个img_dict都有'url','img_number','dir_path'三个属性
                
                for run_time in range(10):    #每张图片最多请求十次    
                    
                    if run_time != 0:
                        img_list = crawler.failed_img_list
                    crawler.failed_img_list = []
                    
                    for img_dict in img_list:                        
                        crawler.get_and_save_img(img_dict, run_time)
                    
                    if crawler.failed_img_list != []:
                        print('%d张图片下载失败：' % len(crawler.failed_img_list))
                        for failed_img_dict in crawler.failed_img_list:
                            print('图%d：%s' % (failed_img_dict['img_number'], failed_img_dict['url']))
                        print()
                
                print('本网页共有目标图片%d张，成功下载%d张图片,失败%d张'% (crawler.img_amount, crawler.success_img_amount, crawler.img_amount-crawler.success_img_amount))
                print('图片保存至%s' % dir_path)
                


if __name__ == '__main__':
    
    start = time.perf_counter()
    
    crawler_for_single_url()
    
    end = time.perf_counter()
    print('任务执行共%.2f秒' % (end-start))
