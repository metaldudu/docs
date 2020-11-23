# code=utf-8
# 天下书库网站抓电子书文本
# http://book.txshuku.net/article/51780.html
# 20181024

import os
import urllib.request
from bs4 import BeautifulSoup

book_id = '51780' # 每本书有一个id
book_url = 'http://www.txshuku.net/mulu/' + book_id + '.html' #构造url
print(book_url)

response = urllib.request.urlopen(book_url) #抓取书籍首页
soup = BeautifulSoup(response, 'lxml')
booktitle = soup.find("title")
sublinks = soup.find_all("li", class_='idcc') # 目录列表部分

# 建立文件
filename = 'tmp/' + booktitle.string +'.md'
filepage = open(filename, 'w')


for i in sublinks:
    chapter_url = i.a.get('href')# 获取子页面url   
    chapter_url = chapter_url.replace('/book/', '/chapterfull/') #构造整章url

    # 抓取章节内容
    response2 = urllib.request.urlopen(chapter_url)
    soup2 = BeautifulSoup(response2, 'lxml')

    # 标题
    title = soup2.find("title")
    title = title.string.replace('-天下书库', '')
    print(title)
    # 正文
    detail = soup2.find("div", class_='contentbox')
    detail = str(detail)

    detail = detail.replace('&nbsp;', '')
    detail = detail.replace('<div class="contentbox" id="htmlContent">', '')
    detail = detail.replace('<br/></div>', '')
    detail = detail.replace('<br/><br/>', '\n\n')

    #写入
    filepage.write('# ' + title + '\n\n')
    filepage.write(detail)

filepage.close()