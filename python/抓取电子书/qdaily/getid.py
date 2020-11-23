#coding=utf-8
#好奇心日报专栏

import requests
import re
import os

#函数：抓取网页
def get_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            response.encoding="utf-8"
            response=response.text
            return response
        else:
            return None
    except RequestException:
        return None


#函数：抓取网页id到列表
def get_list(column_id):
    column_url = 'http://www.qdaily.com/special_columns/' + str(column_id)
    page = get_page(column_url)
    pages_id = re.findall(r'articles/\d+', page)
    return pages_id


# 通过json逐一抓取页面id，首页包含第一个值： 1524264433 ，最后： 1409394840
def get_list2(keynum):
     
    keyurl = 'http://www.qdaily.com/special_columns/show_more/15/' + str(keynum)
    page = get_page(keyurl)
    pages_id = re.findall(r'"id":\d{4,5},"genre"', page)
    for i in range(len(pages_id)):
        pages_id[i] = str(pages_id[i]).replace(',"genre"', '')
        pages_id[i] = str(pages_id[i]).replace('"id":', '')
        i = i +1
    #print(pages_id)
    
    # 匹配下一个json页面值，注意列表格式转换为str
    nextkey = re.findall(r'"last_key":\d*', page)
    nextkey = str(nextkey[0]).replace('"last_key":', '')

    return (pages_id, nextkey)

# 定义列表存储，第一个数字是html内包含的值
list_keys = ['1524264433']
list_pageid = []

# 通过循环获得所有的值，写入列表，目前少于15页
for i in range(15):
    out = get_list2(list_keys[i])
    list_pageid = list_pageid + out[0]

    if not out[1] == '':
        list_keys.append(out[1])   
        i = i+1
    else:
        break

#print(list_keys)
#print(list_pageid)

