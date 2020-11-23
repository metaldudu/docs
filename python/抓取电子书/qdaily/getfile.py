#coding=utf-8
#好奇心日报专栏
import requests
import urllib.request
import re
import os
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner

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

    # 建立文件
    filename = 'tmp/' + str(page_id) +'.md'
    filepage = open(filename, 'w')
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

    filepage.write(maintxt)
    filepage.close()

get_mdfile(61908)