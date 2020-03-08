# -*- coding: utf-8 -*-

from selenium import webdriver
import urllib, os, pymysql, time
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup



driver = webdriver.Firefox()

driver.get('http://www.asos.com/?hrd=1')

output = driver.find_elements_by_xpath("//a[@class='standard']")
for ele in output:
    print(ele.get_attribute('href'))
