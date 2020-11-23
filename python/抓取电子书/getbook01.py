# code=utf-8
# 看到hipda论坛的帖子：https://www.hi-pda.com/forum/viewthread.php?tid=2414544
# 通过分析，发现数据都在json格式存储
# 先想用wget下载，结果是乱码，于是存储json到html
# 再转换md，pandoc打包完工，耗时2小时
# 20181021

# 原始地址，貌似是为了微信阅读而开发的
# http://cdbszn.4008990000.net/scwdebook/menufk.html

import os
import requests
import json

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

list1 = [] #所有文件，列表

for i in range(1,130):
    jsonurl = 'http://cdbszn.4008990000.net/cdwd_ebook/readDetail?xid=' + str(i)
    page = get_page(jsonurl)
    try:
        jsonpage = json.loads(page)

        #print(jsonpage['id'], jsonpage['menu_id'], jsonpage['name'])
        #list1.append(jsonpage)#写入list可以排序，开始想先排序再输出，后来是改文件名然后输出，排序让pandoc搞定
        #list1.sort(key=lambda k:(k.get('menu_id', 0)))# 排序的例子
        
        # 补零的函数，使得epub的目录排序
        id = str(jsonpage['id']).zfill(2)
        mid = str(jsonpage['menu_id']).zfill(2)

        # 写文件
        filename = "tmp/" + mid +"-"+ id +".html"
        f = open(filename, 'w')
        f.write("<h1>" + mid +"-"+ id + str(jsonpage['name']) + "</h1>")
        f.write(str(jsonpage['content'])) #写入内容
        f.close()

        # 转换成md，注意可以取消div/span
        cmd = 'pandoc -f html-native_divs-native_spans -t markdown ' + filename + ' -o ' + filename + '.md'
        os.system(cmd)

    except json.decoder.JSONDecodeError:# 有的id居然是空的，NND
        print('error')
    else:
        print(filename)

# 生成电子书
cmd2 = 'pandoc --toc-depth=1 -o tmp/1.epub tmp/*.md'
os.system(cmd2)