from crawler_class import Crawler_class
import time
import os
import traceback


def crawler_for_single_url(urls_file='', url=''):

    global crawler
    crawler = Crawler_class(urls_file)

    if __name__ == '__main__':
        print('注意事项：')
        print('1、请确认目前是否可以通过%s访问桃隐，如不能，请在crawler_class.py的Crawler_class类的成员变量中修改domain_name的值为桃隐的最新域名' % crawler.domain_name)
        print('2、默认根目录为%s，如需修改，请在crawler_class.py的Crawler_class类的成员变量中修改default_root_path的值' % crawler.default_root_path)
        print('3、如果之前曾使用过此爬虫，请将生成的SAVED.txt和ERROR.txt放在本程序所在目录下，从而避免同一网页的重复爬取')
        url = input('请输入要爬取的网页的网址或编号：\n')
    
    url = crawler.correct_url(url)
    
    if url:
        
        if os.path.exists('SAVED.txt'):
            saved_file = open('SAVED.txt','r', encoding='utf-8')
            saved_list = [img_serial_number[:-1] for img_serial_number in saved_file.readlines()]
            saved_file.close()
        else:
            saved_list = []
            
        if not crawler.is_already_saved(saved_list, url):
            
            html_source_code = crawler.get_html_source_code(url)

            if html_source_code:
                
                if crawler.no_alert_error(html_source_code):
                    
                    html_title = crawler.get_html_title(html_source_code)
                    
                    if html_title:
                        
                        dir_path = crawler.make_dir()    #参数为self.sub_path,无需再传入html_title2884
                            
                        crawler.save_html_source_code(dir_path, html_title, html_source_code)
                        
                        html_type = crawler.get_html_type(html_source_code)
                            
                        new_html_source_code = crawler.make_new_html(html_source_code, html_type, url, html_title)
                        
                        if new_html_source_code:
                        
                            crawler.save_new_html(dir_path, html_title, new_html_source_code)
                            
                            img_list = crawler.get_img_urls(html_source_code, html_type, dir_path)    
                            #img_list内嵌套多个img_dict,每个img_dict都有'url_serial_number', 'img_url', 'img_number', 'dir_path'四个属性，
                            #即：帖子序号、图片网址、图片在本网页内的序号、图片下载所在路径
                            
                            if img_list:
                                '''
                                若第一次请求有失败的图片，则以追加的方式加入ERROR.txt中
                                在之后的请求中若有成功的图片，则从ERROR.txt中删除该图片的信息
                                '''
                                for run_time in range(1,3):  
                                    
                                    if run_time != 1:
                                        img_list = crawler.failed_img_list
                                    crawler.failed_img_list = []
                                    
                                    for img_number, img_dict in enumerate(img_list):  
                                        
                                        is_successful = crawler.get_and_save_img(img_dict, run_time)
                                        
                                        if run_time == 1 and not is_successful:
                                            crawler.add_failed_img_to_ERRORtxt(img_dict)
                                        if is_successful:    
                                            crawler.remove_successful_img_from_ERRORtxt(img_dict)
                                            #不管是否run_time=1,都要删除已成功的图片信息，因为上次程序可能半途中止运行

                                    if crawler.failed_img_list:
                                        
                                        print('%d张图片下载失败：' % len(crawler.failed_img_list))
                                        for failed_img_dict in crawler.failed_img_list:
                                            print('贴子%s-图%d：%s' % (failed_img_dict['url_serial_number'], failed_img_dict['img_number'], failed_img_dict['img_url']))
                                        print()
                                            
                                print('本网页共有%d张目标图片，成功下载%d张图片,失败%d张'% (crawler.img_amount, crawler.success_img_amount, crawler.img_amount-crawler.success_img_amount))
                                print('图片保存至%s\n' % dir_path)
                                if crawler.img_amount-crawler.success_img_amount != 0:
                                    print('失败文件已以追加的方式写入本程序所在目录下的ERROR.txt\n')
                                
                                crawler.get_resource_download_link(new_html_source_code, html_title)    
                                '''
                                为防止多次写入同一网页的链接，必须把该语句放在最靠近SAVED.txt的地方，
                                这样刚保存完就会将贴子序号写入SAVED.txt,下次不会再对该网页操作。
                                而如果该语句放在前面，可能在该语句与SAVED之间程序半途中止运行，
                                下次还会再次向Download Link.txt写入资源链接。
                                '''
                                
                                call = traceback.extract_stack()[-2][2]
                                if call == 'crawler_for_multiple_urls':
                                    crawler.remove_successful_url_from_urls_file(urls_file, url)
                                    print('对于网页%s的爬取已经完成，已在%s中删除其url' % (url, urls_file))
                                
                                with open(r'SAVED.txt','a+', encoding='utf-8') as f:
                                    f.write(crawler.url_serial_number+'\n')


if __name__ == '__main__':

    start = time.perf_counter()
    
    crawler_for_single_url()
    
    end = time.perf_counter()
    
    print('任务执行共%.2f秒' % (end-start))