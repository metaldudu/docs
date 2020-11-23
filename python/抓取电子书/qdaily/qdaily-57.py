# coding=utf-8
# 好奇心日报专栏 访谈录
# 20181019
# 20190426更新

import requests
import urllib.request
import re
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime

# 栏目信息
column_name = '好奇心日报-访谈录'
column_id = '57'
column_url = 'http://www.qdaily.com/special_columns/57.html'
dir = 'qdaily' + column_id
os.system('mkdir ' + dir)

# 保存文件函数
def get_mdfile(page_id):

    url = 'http://www.qdaily.com/articles/' + str(page_id) +'.html'
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'lxml')

    maintxt = ''

    # 标题
    title = soup.find("h2")
    maintxt = maintxt + ('# ' + str(title.string) + '\n\n')

    # 时间
    pagetime = soup.find("span", class_="date")
    pagetime = str(pagetime)[47:57]
    maintxt = maintxt + (pagetime+ '\n\n')

    # 梗概
    excerpt = soup.find("p", class_='excerpt')
    maintxt = maintxt + (str(excerpt.string) + '<hr/>\n\n')
    
    # 正文部分
    detail = str(soup.find("div", class_='detail'))
    detail = detail.replace('		','')
    detail = clean_html(detail)
    maintxt = maintxt + detail

    # 建立文件
    filename = dir + '/' + pagetime +'.md'
    filepage = open(filename, 'w')
    filepage.write(maintxt)
    filepage.close()

#函数：清理html标签
def clean_html(html):
    html = html.replace('\\n', '')#去掉换行符，两个斜线反义
    html = html.replace('data-src', 'src')#修改图片加载部分
    html = html.replace('\xa0', ' ')#替换空格
    html = html.replace(' </figure></div>', '')
    html = html.replace('<title>', '')
    html = html.replace('<p>', '')
    html = html.replace('<p class="">', '')
    html = html.replace('</p>', '\n\n')
    html = html.replace('<h3>', '### ')
    html = html.replace('</h3>', '\n\n')
    html = html.replace('<br>', '')
    html = html.replace('"></figcaption>', ')\n\n`')
    html = html.replace('<figcaption>', '\n\n')
    html = html.replace('</figcaption>', '\n\n')
    html = html.replace('<p><strong>', '**')
    html = html.replace('</strong></p>', '**')
    html = html.replace('<strong>', '')
    html = html.replace('</strong>', '')
    html = html.replace('<p class="excerpt">', '')
    html = html.replace('  <div class="detail">  <p finallycleanhtml="true" nocleanhtml="true">', '')
    html = html.replace('\n ', '\n')
    return html

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

# 函数1抓取首页html文件里的子页面id
def get_list1():
    pageurl = column_url
    page = get_page(pageurl)
    pages_id = re.findall(r'/articles/\d{4,5}', page)
    for i in range(len(pages_id)):
        pages_id[i] = str(pages_id[i]).replace('/articles/', '')
        i = i +1
    return pages_id

# 函数2，通过json抓取子页面id，首页包含第一个值： 1523514275 ，之后在json底部
def get_list2(keynum):
     
    keyurl = 'http://www.qdaily.com/special_columns/show_more/' + column_id + '/' + str(keynum)
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
list_keys = ['1523514275']
list_pageid = get_list1()

# 通过循环获得所有的值，写入列表
for i in range(3):
    out = get_list2(list_keys[i])
    list_pageid = list_pageid + out[0]

    if not out[1] == '':
        list_keys.append(out[1])   
        i = i+1
    else:
        break

# 抓取第一页的pageid
def get_first_list():
    page = get_page(column_url)
    pages_id = re.findall(r'articles/\d+', page)
    first_list = []
    for i in pages_id:
        newpage = str(i).replace('articles/', '')
        # print(newpage)
        first_list.append(newpage)
    return first_list

# 加到一起
list_pageid = get_first_list() + list_pageid

#print(list_keys)
pagecount = str(len(list_pageid))
print('文章总数： '+ pagecount)

# 生成文件
for id in tqdm(list_pageid):  
    # pass
    get_mdfile(id)

# 生成最后的log文件
filelog = open(dir + '/2100.md', 'w')
filelog.write('# 【制作信息】\n\n')
filelog.write('栏目名称：' + column_name + '\n\n')
filelog.write('作者：苏琦\n\n专栏地址：' + column_url +'\n\n')
filelog.write('生成时间：' + str(datetime.date.today()) + '\n\n')
filelog.write('文章数：' + pagecount + '\n\n')
filelog.write('@metaldudu')
filelog.close()

# 生成metadata信息
def make_metafile():
    m_file = open(dir + '/metadata.xml',  'w')
    m_file.write('<dc:title>好奇心日报：访谈录</dc:title>\n' )
    m_file.write('<dc:language>zh-CN</dc:language>\n')
    m_file.write('<dc:creator opf:file-as="好奇心日报" opf:role="aut">好奇心日报</dc:creator>\n')
    m_file.write('<dc:date opf:event="publication">2018-09-17</dc:date>\n')
    m_file.close()

make_metafile()

#调用pandoc制作epub，toc指定在h1，设置title（否则报错），读入metadata.xml
epub_title = str(datetime.date.today()) + '-好奇心日报-访谈录.epub'
cmd = 'pandoc ' + dir +'/*.md --toc-depth=2 --epub-metadata=' + dir + '/metadata.xml --metadata title=《好奇心日报：访谈录》 --output ' + epub_title
os.system(cmd)
# os.system('rm -rf ' + dir + '/*.md')
print('epub cteated!')