# -*- coding:utf-8 -*-
'''
Created on 2016年11月3日

@author: Administrator
'''

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, queue
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
            print ("%s processing %s" % (threadName, data))
            crawl(data)
        else:
            queueLock.release()
        time.sleep(1)

def write_page_url(driver, product_url, bread):
    product_list = driver.find_elements_by_xpath("//div[@class='unit']/dl/dt/a")
    for ele_product_list in product_list:
        product_url.write(bread + '\t' + ele_product_list.get_attribute("href") + "\n")

#start of the main function, the input is the category page url

def crawl(page_url):
#     driver = webdriver.PhantomJS()
    x = page_url.split('\t')
    bread = x[0].strip()
    url = x[1].strip('\n')
    
    driver = webdriver.PhantomJS()
    driver.get(url)

    write_page_url(driver, product_url, bread)
    
    driver.quit()
    
product_url = open('C:/Users/Administrator/Desktop/uniqlo_url.txt', 'a')
file = open("C:/Users/Administrator/Desktop/uniqlo.txt")
# url = 'http://www.hm.com/hk/en/product/54618?article=54618-B'
lines = file.readlines()
file.close()
    
# threadList = ["Thread-1", "Thread-2"]
threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8"]

nameList = lines
queueLock = threading.Lock()
workQueue = queue.Queue(len(nameList) + len(threadList))
threads = []
threadID = 1

# 创建新线程
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

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

product_url.close()
file.close()