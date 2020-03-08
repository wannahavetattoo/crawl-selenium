'''
Created on 2016年11月5日

@author: Administrator
'''


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os, time, queue, urllib, pymysql
import threading
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
#         print ("开启线程：" + self.name)
        process_data(self.name, self.q)
#         print ("退出线程：" + self.name)
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
#             print ("%s processing %s" % (threadName, data))
#             print(data)
            try:
                craw_product_contents(data)
            except:
                print(data)
        else:
            queueLock.release()
#         time.sleep(1)
def saveImgs(driver, img_path, img_url_list):
    img_num = 0
    if not os.path.exists(img_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(img_path)
    
    while img_num < len(img_url_list):
        image_url = img_url_list[img_num]
        save_path = img_path + str(img_num) + '.jpg'
        urllib.request.urlretrieve(image_url, save_path)
        img_num = img_num + 1
    return img_num

def check_exists_by_xpath(driver, xpath):
    try:
        if len(driver.find_element_by_xpath(xpath).text) > 1:
            return False 
    except NoSuchElementException:
        return False
    return True

def craw_product_contents(product_url):
    
    driver = webdriver.PhantomJS()
#     driver = webdriver.PhantomJS()
#     driver.set_page_load_timeout(20)
    product_url = product_url.strip('\n')
    driver.get(product_url)
    

    prodInfo = driver.find_element_by_xpath("//div[@id='prodInfo']")
    sku = prodInfo.find_element_by_xpath('ul/li').text[-6:].strip()
    
    img_number = 0
    prodThumbImgs = driver.find_element_by_xpath("//div[@id='prodImgDefault']/a")
    
    img_list = []
    img_list.append(prodThumbImgs.get_attribute('href'))
    img_number = saveImgs(driver, ROOTPATH + str(sku) + '/', img_list)
    
    driver.quit()
    
ROOTPATH = "C:/Users/Administrator/Desktop/UNIQLO/000/"
category_file = open("C:/Users/Administrator/Desktop/1.txt")

lines = category_file.readlines()

category_file.close()


# threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8", "Thread-9", "Thread-10" \
#               "Thread-11", "Thread-12", "Thread-13", "Thread-14", "Thread-15", "Thread-16", "Thread-17", "Thread-18", "Thread-19", "Thread-20"]
# threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8"]
threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
nameList = lines
queueLock = threading.Lock()
workQueue = queue.Queue(len(nameList) + len(threadList))
threads = []
threadID = 1
 
# # 创建新线程
for tName in range(len(threadList)):
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
 
# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()
 
# # 等待队列清空
while not workQueue.empty():
    pass
 
# # 通知线程是时候退出
exitFlag = 1
 
# # 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

# # db.close()