'''
Created on 2016年11月4日

@author: Administrator
'''
import pymysql,os
import shutil
# dir = 'C:/Users/Administrator/Desktop/UNIQLO'
# files = os.listdir(dir)  
# for f in files:  
#     print (f)  

def find_productIDList_by_category(category):
    website = 'www.zalora.com.hk'
    sql = 'Select idproduct from testdb.product where product_breadcrumbs = %s AND product_website = %s'
    data = (category, website)
    
    cursor.execute(sql, data)
    fetch_result = cursor.fetchall()
    result = ''
    if fetch_result is not None:
        for ele in fetch_result:
            if ele is not None:
                try:
                    result = result + str(ele[0]) + ';' 
                except:
                    print('ele[0] error')
    result = result.strip(';')
    return result


def find_sku_by_id(id):
    sql = 'select product_sku from testdb.product where idproduct = %s'
    cursor.execute(sql, id)
    fetch_result = cursor.fetchone()
    return fetch_result[0]

def select_info_by_id(id):
    sql = 'select product_img_number from testdb.product where idproduct = %s'
    
    cursor.execute(sql, id)
    fetch_result = cursor.fetchone()
    return fetch_result[0]

def get_folder_path_by_IMG_id(imgid):
    imgid = str(imgid)
    string_path = ''
    for ele in imgid:
        string_path = string_path + ele + '/'
    return string_path

def get_product_img_fids(product_img_number, img_id_start):
    string_fids = ''
    img_id_end = img_id_start + int(product_img_number)
    while img_id_start < img_id_end:
        string_fids = string_fids + str(img_id_start) + ";"
        img_id_start = img_id_start + 1
    return img_id_start, string_fids.rstrip(";")

def update_fids(id, fidstring):
    sql = 'UPDATE testdb.product SET product_img_fids = %s WHERE idproduct = %s'
    data = (fidstring, id)
    
    cursor.execute(sql, data)
    db.commit()#需要这一句才能保存到数据库中


db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()


img_id_start = 576230


home_folder = "F:/UNIQLO/"
new_home_folder = "F:/new_UNIQLO/"

idstring = open("C:/Users/Administrator/Desktop/idstring.txt").readlines()

# for ele in idstring:
#     ele = ele.strip('\n')
#     print(ele)
#     img_id_start, fidstring = get_product_img_fids(select_info_by_id(ele), img_id_start)
#     update_fids(ele, fidstring)


for ele_idstring in idstring:
    ele_idstring = ele_idstring.strip('\n')
    print(ele_idstring)
     
    result = ele_idstring.split(',')
    product_img_string = result[0]
    product_sku = result[1]
#     print(product_img_string + '\t' +product_sku)
    if product_img_string != '':
        img_list = product_img_string.split(';')
        img_nmber = 0
        for ele in img_list:
            new_path_ = ''
            new_path_ = new_home_folder + get_folder_path_by_IMG_id(ele)
            if not os.path.exists(new_path_):  ###判断文件是否存在，返回布尔值
                os.makedirs(new_path_)
            shutil.copy(home_folder + product_sku + "/" + str(img_nmber) + ".jpg", new_path_ + str(ele) + ".jpg")
            img_nmber = img_nmber + 1
          
db.close()