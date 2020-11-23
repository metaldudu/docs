# coding=utf-8
# 好奇心日报专栏-万物简史
# 20181017
# 20190426 更新清除html、进度条，输出格式

import requests
import urllib.request
import re
import os
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
import datetime
from tqdm import tqdm

# 清除多余html元素
def clean_html(html):
    cleaner = Cleaner(
                page_structure=True,
                meta=True,
                embedded=True,
                links=True,
                style=True,
                processing_instructions=True,
                inline_style=True,
                scripts=True,
                javascript=True,
                comments=True,
                frames=True,
                forms=True,
                annoying_tags=True,
                remove_unknown_tags=True,
                safe_attrs_only=True,
                safe_attrs=frozenset(['src', 'color', 'href', 'title', 'class', 'name', 'id']),
                remove_tags=('span', 'font', 'div', 'img', 'a')
            )
    return cleaner.clean_html(html)

# 生成文件函数
def get_mdfile(page_id):

    url = 'http://www.qdaily.com/articles/' + str(page_id) +'.html'
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'lxml')

    maintxt = ''

    # 标题
    title = soup.find("h2")
    maintxt = maintxt + ('# ' + (str(title.string).replace('「万物简史」','')) + '\n\n')

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
    filename = 'tmp/' + pagetime +'.md'
    filepage = open(filename, 'w')
    filepage.write(maintxt)
    filepage.close()


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

# 通过json逐一抓取页面id，以下部分
# <div class="packery-container articles" data-lastkey="1544310793" data-columnid="15">
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
list_keys = ['1544310793']
list_pageid = []

# 通过循环获得所有的值，写入列表，目前11页
for i in range(18):
    out = get_list2(list_keys[i])
    list_pageid = list_pageid + out[0]

    if not out[1] == '':
        list_keys.append(out[1])   
        i = i+1
    else:
        break

# 抓取第一页的pageid
def get_first_list():
    page = get_page('http://www.qdaily.com/special_columns/15.html')
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
    # print(id)
    get_mdfile(id)

# 生成最后的log文件
filelog = open('tmp/2100.md', 'w')
filelog.write('# 【制作信息】\n\n作者：苏琦\n\n专栏地址：http://www.qdaily.com/special_columns/15.html\n\n')
filelog.write('生成时间：' + str(datetime.date.today()) + '\n\n')
filelog.write('文章数：' + pagecount + '\n\n')
filelog.write('@metaldudu')
filelog.close()


# 生成metadata信息
def make_metafile():
    m_file = open('tmp/metadata.xml',  'w')
    m_file.write('<dc:title>好奇心日报：万物简史</dc:title>\n' )
    m_file.write('<dc:language>zh-CN</dc:language>\n')
    m_file.write('<dc:creator opf:file-as="好奇心日报" opf:role="aut">好奇心日报</dc:creator>\n')
    m_file.write('<dc:date opf:event="publication">2018-09-17</dc:date>\n')
    m_file.close()

make_metafile()

#调用pandoc制作epub，toc指定在h1，设置title（否则报错），读入metadata.xml
epub_title = str(datetime.date.today()) + '-好奇心日报-万物简史.epub'
cmd = 'pandoc tmp/*.md --toc-depth=2 --epub-metadata=tmp/metadata.xml --metadata title=《好奇心日报：万物简史》 --output ' + epub_title
os.system(cmd)
#os.system('rm -rf tmp/*.md')
print('epub cteated!')