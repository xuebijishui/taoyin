from down_one import Spider
import time, threading

count = 0
spider = Spider()
spider.retry = 100
thread_num = 100
rlock = threading.RLock()


def remove_ok_img(img_dict):
    rlock.acquire()
    txt = open('ERROR.txt','r', encoding='utf-8',errors='ignore').read()
    txt = txt.replace(str(img_dict)+'\n', '')
    with open('ERROR.txt','w', encoding='utf-8') as f:
        f.write(txt)
        #print('删除', img_dict)
    rlock.release()


def thread_func():
    global count
    global img_list
    while True:
        rlock.acquire()
        if len(img_list) == 0:
            rlock.release()
            break
        else:
            img_dict = img_list.pop()
            rlock.release()
            url_num = img_dict['url_num']
            img_url = img_dict['img_url']
            dir_path = img_dict['dir_path']
            try:
                if spider.down_one_img(img_url, dir_path):
                    count +=1
                    remove_ok_img(img_dict)
            except Exception as e:
                print(e)
                

def error_imgs():
    enter = input('请确保本程序所在目录内存在ERROR.txt，按回车开始......')
    img_dict_file = open('ERROR.txt','r', encoding='utf-8',errors='ignore').readlines()
    global img_list
    img_list = [eval(img_dict.rstrip('\n')) for img_dict in img_dict_file]    #img_list内嵌套多个
    global spider
    spider.img_amount = len(img_list)
    
    thread_list = []
    for i in range(thread_num):
        t = threading.Thread(target=thread_func)
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()


if __name__ == '__main__':   
    start = time.perf_counter()
    error_imgs()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))
