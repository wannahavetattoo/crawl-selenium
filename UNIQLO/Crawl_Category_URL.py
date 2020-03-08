# -*- coding:utf-8 -*-
'''
Created on 2016年11月3日

@author: Administrator
'''


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os, time, queue, urllib, pymysql
from selenium.webdriver.common.action_chains import ActionChains


###########


###########
driver = webdriver.Firefox()
page_url = 'http://www.uniqlo.com/hk/'
driver.get(page_url)
time.sleep(5)

category_1 = driver.find_elements_by_xpath("//ul[@id='navHeader']/li")

for ele_category_1 in category_1[0:4]:
    category_string1 = ''
    category_string1 = category_string1 + ele_category_1.find_element_by_xpath('a/img').get_attribute('alt') + '/'
    #鼠标悬停动作*********************
    chain_1 = ActionChains(driver)
    ##执行
    chain_1.move_to_element(ele_category_1).perform()
    
    category_2 = ele_category_1.find_elements_by_xpath("ul/li")
    for ele_category_2 in category_2:
        category_string2 = ''
        category_string2 = category_string1 + ele_category_2.find_element_by_xpath('a/img').get_attribute('alt') + '/'
        #鼠标悬停动作*********************
        chain_2 = ActionChains(driver)
        ##执行
        chain_2.move_to_element(ele_category_2).perform()
        category_3 = ele_category_2.find_elements_by_xpath("ul/li")
        for ele_category_3 in category_3:
            category_string3 = ''
            category_string3 = category_string2 + ele_category_3.find_element_by_xpath('a').text
            
            print(category_string3 + '\t' + ele_category_3.find_element_by_xpath('a').get_attribute('href'))
driver.quit()
