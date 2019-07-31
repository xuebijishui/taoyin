from crawler_class import Crawler
import time, threading

count = 0

def thread(thread_num, start, end):
    global count
    for img_dict in img_list[start:end]:
        for run_time in range(1, max_time+1):
            is_successful = crawler.get_and_save_img(img_dict, run_time)
            if is_successful:    
                crawler.remove_successful_img_from_ERRORtxt(img_dict)
                break
        count +=1
        print(count)


def crawler_for_img_of_ERRORtxt():
    
    num_thread = 100    #线程
    
    print('请确保本程序所在目录内存在ERROR.txt，按回车开始......')
    img_dict_file = open(r'ERROR.txt','r', encoding='utf-8',errors='ignore').readlines()
    global img_list
    img_list = [eval(img_dict[:-1]) for img_dict in img_dict_file]    #img_list内嵌套多个

    global crawler
    crawler = Crawler()
    crawler.img_amount = len(img_list)
    
    global max_time
    max_time = int(input("请输入尝试次数上限："))
    print('\n共有%d张目标图片\n' % crawler.img_amount)

    thread_list = []
    if img_list:
        part = len(img_list) // num_thread
        for i in range(num_thread):
            start = part * i    #第part个线程的起始url下标
            if i == num_thread - 1:   #最后一块
                end = len(img_list)    #第part个线程的终止url下标
            else:
                end = start + part    #第part个线程的终止url下标
            t = threading.Thread(target=thread, kwargs={'thread_num':i, 'start':start, 'end':end})
            t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for i in thread_list:
            t.join()
        
    print('完事')
            

if __name__ == '__main__':    
    start = time.perf_counter()    
    crawler_for_img_of_ERRORtxt()    
    end = time.perf_counter()    
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))