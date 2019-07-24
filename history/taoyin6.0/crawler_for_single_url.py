from crawler_class import Crawler
import time
import os
import traceback


def crawler_for_single_url(url=''):
    crawler = Crawler()
    if __name__ == '__main__':
        print('注意事项：')
        print('1、请确认目前是否可以通过%s访问桃隐，如不能，请在crawler_class.py的Crawler_class类的成员变量中修改domain_name的值为桃隐的最新域名' % crawler.domain_name)
        print('2、默认根目录为本程序所在目录(为了win和linux平台下都能正常爬取)，如需修改，请在crawler_class.py的Crawler_class类的成员变量中修改default_root_path的值')
        print('3、如果之前曾使用过此爬虫，请将生成的SAVED.txt和ERROR.txt放在本程序所在目录下，从而避免同一网页的重复爬取')
        print('4、如果之前未使用过此爬虫，请删除原有的SAVED.txt和ERROR.txt以及Download Link.txt')
        url = input('请输入要爬取的网页的网址或编号：\n')

    crawler.correct_url(url)
    #获取已保存的、不存在的、无权限的 网页编号列表
    if crawler.url:
        if os.path.exists('SAVED.txt'):
            with open('SAVED.txt','r', encoding='utf-8') as f:
                saved_list = [img_serial_number[:-1] for img_serial_number in f.readlines()]
        else:
            saved_list = []
        if os.path.exists('NO EXIST.txt'):
            with open('NO EXIST.txt','r', encoding='utf-8') as f:
                no_exist_list = [img_serial_number[:-1] for img_serial_number in f.readlines()]
        else:
            no_exist_list = []  
        if os.path.exists('NO JURISDICTION.txt'):
            with open('NO JURISDICTION.txt','r', encoding='utf-8') as f:
                no_jurisdiction_list = [img_serial_number[:-1] for img_serial_number in f.readlines()]
        else:
            no_jurisdiction_list = []
        
        #从获取源代码到保存源代码
        if not crawler.is_saved(saved_list) and not crawler.no_exist(no_exist_list) and not crawler.no_jurisdiction(no_jurisdiction_list):      #如果贴子未保存且贴子存在且有权限
            crawler.get_html_source_code()
            if crawler.html_source_code:
                if crawler.no_alert_error():
                    if crawler.get_html_title():
                        crawler.make_dir()
                        crawler.save_html_source_code()
                        
                        #（净化）制作新的网页
                        crawler.get_html_type()
                        crawler.make_new_html()
                        if crawler.new_html_source_code:
                            crawler.save_new_html()
                            
                            #爬取图片
                            img_list = crawler.get_img_urls()    
                            #img_list内嵌套多个img_dict,每个img_dict都有'url_serial_number', 'img_url', 'img_number', 'dir_path'四个属性，
                            #即：帖子序号、图片网址、图片在本网页内的序号、图片下载所在路径
                            if img_list:
                                '''
                                若第一次请求有失败的图片，则以追加的方式加入ERROR.txt中
                                在之后的请求中若有成功的图片，则从ERROR.txt中删除该图片的信息
                                '''
                                for run_time in range(1,crawler.retry):  
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
                                        print('以下%d张图片下载失败：' % len(crawler.failed_img_list))
                                        for failed_img_dict in crawler.failed_img_list:
                                            print('贴子%s-图%d：%s' % (failed_img_dict['url_serial_number'], failed_img_dict['img_number'], failed_img_dict['img_url']))
                                        print('以上%d张图片下载失败：\n' % len(crawler.failed_img_list))
                                
                                print('本网页共有%d张目标图片，成功下载%d张图片,失败%d张'% (crawler.img_amount, crawler.success_img_amount, crawler.img_amount-crawler.success_img_amount))
                                print('图片保存至%s\n' % crawler.dir_path)
                                if crawler.img_amount-crawler.success_img_amount != 0:
                                    print('失败文件已以追加的方式写入本程序所在目录下的ERROR.txt\n')
                                
                                crawler.get_resource_download_link()    
                                '''
                                为防止多次写入同一网页的链接，必须把该语句放在最靠近SAVED.txt的地方，
                                这样刚保存完就会将贴子序号写入SAVED.txt,下次不会再对该网页操作。
                                而如果该语句放在前面，可能在该语句与SAVED之间程序半途中止运行，
                                下次还会再次向Download Link.txt写入资源链接。
                                '''
                                
                                call = traceback.extract_stack()[-2][2]
                                if call == 'crawler_for_multiple_urls':
                                    crawler.remove_url_from_urls_file()
                                    print('对于网页%s的爬取已经完成，已在%s中删除其url' % (crawler.url, crawler.urls_file))
                                
                                with open(r'SAVED.txt','a+', encoding='utf-8') as f:
                                    f.write(crawler.url_serial_number+'\n')


if __name__ == '__main__':
    start = time.perf_counter()
    crawler_for_single_url()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))