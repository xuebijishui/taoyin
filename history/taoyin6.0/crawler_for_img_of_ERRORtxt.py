from crawler_class import Crawler
import time


def crawler_for_img_of_ERRORtxt():
    print('请确保本程序所在目录内存在ERROR.txt，按回车开始......')
    img_dict_file = open(r'ERROR.txt','r', encoding='utf-8').readlines()
    img_list = [eval(img_dict[:-1]) for img_dict in img_dict_file]    #img_list内嵌套多个
    
    crawler = Crawler()
    crawler.img_amount = len(img_list)
    
    max_time = int(input("请输入尝试次数上限："))
    print('\n共有%d张目标图片\n' % crawler.img_amount)
   
    for run_time in range(1, max_time+1):            
        if run_time != 1:                    
            img_list = crawler.failed_img_list
        crawler.failed_img_list = []
                        
        for img_number, img_dict in enumerate(img_list):                     
            is_successful = crawler.get_and_save_img(img_dict, run_time)
            if is_successful:    
                crawler.remove_successful_img_from_ERRORtxt(img_dict)
                
        if crawler.failed_img_list:
            print('以下%d张图片下载失败：' % len(crawler.failed_img_list))
            for failed_img_dict in crawler.failed_img_list:
                print('贴子%s-图%d：%s' % (failed_img_dict['url_serial_number'], failed_img_dict['img_number'], failed_img_dict['img_url']))
            print('以上%d张图片下载失败：' % len(crawler.failed_img_list))
            
    if crawler.failed_img_list:
        f = open(r'ERROR.txt','w', encoding='utf-8')
        for url_information_dict in crawler.failed_img_list:
            f.write(str(url_information_dict)+'\n')
        f.close()
        print('已将下载失败的图片信息保存至本程序所在目录下的ERROR.txt\n')

if __name__ == '__main__':    
    start = time.perf_counter()    
    crawler_for_img_of_ERRORtxt()    
    end = time.perf_counter()    
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))