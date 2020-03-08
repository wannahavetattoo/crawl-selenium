'''
Created on 2016年11月5日

@author: Administrator
'''

import pymysql,os
import shutil


def store_in_database(datalist):
    #start of database updating
    
    if 'women' in str(datalist):
        gender = 0
    else:
        gender = 1
        
    data = (datalist[0].strip().strip('\n'), datalist[1].strip().strip('\n'), datalist[2].strip().strip('\n'), \
            datalist[3].strip().strip('\n'), datalist[4].strip().strip('\n'), datalist[5].strip().strip('\n'), \
            datalist[6].strip().strip('\n'), datalist[7].strip().strip('\n'), datalist[8].strip().strip('\n'), \
            datalist[9].strip().strip('\n'), datalist[10].strip().strip('\n'), gender)
    sql_update_content = """
    INSERT INTO testdb.product(
    product_sku,
    product_title,
    product_url_stat,
    product_website,
    product_craw_time,
    product_price,
    product_url,
    product_breadcrumbs,
    product_desc,
    product_size_detail1,
    product_img_number,
    product_gender)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
 
    cursor.execute(sql_update_content, data)
    db.commit()#需要这一句才能保存到数据库中
    #end of database updating

db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()


sql_query_select = """SELECT product_img_fids, product_sku from testdb.product where idproduct = %s"""

home_folder = "C:/Users/Administrator/Desktop/ASOS/"
new_home_folder = "C:/Users/Administrator/Desktop/new_ASOS/"

idstring = open("C:/Users/Administrator/Desktop/uniqlo_database.txt").readlines()

for ele_idstring in idstring:
    ele_list = ele_idstring.split('\t')
    id = ele_list[0].strip('\n').strip()
    data = ele_list[1].strip('\n').strip()
    datalist = data.split('**')
    print(id)
    store_in_database(datalist)
    
db.close()