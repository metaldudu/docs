# code=utf-8
# 悠讀文學網 抓电子书文本
# https://www.yooread.com/3/16603/
# 20190826 更新

import os
import requests
from bs4 import BeautifulSoup

book_id = '2117' # 每本书有一个id
book_url = 'https://www.yooread.net/6/' + book_id + '/'# 书籍url

headers = {
            "Host": "www.yooread.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}
res = requests.get(book_url, headers=headers) #抓取书籍首页
res.encoding='utf-8'
soup = BeautifulSoup(res.text, 'lxml')
#print(soup.text)
booktitle = soup.find("title") #书名

# 建立文件，逐一抓取章节
filename = 'tmp/' + booktitle.string +'.md'
filepage = open(filename, 'w')

# 抓取章节列表
soup = soup.find("div", id='chapterList') # 章节列表部分
subtables = soup.find_all("table") # 有的书包含多个table，也就是多个章节

# 抓取单页函数
def get_chapter(url):
    res2 = requests.get(url)
    res2.encoding='utf-8'
    soup2 = BeautifulSoup(res2.text, 'lxml')

    # 正文
    detail = soup2.find("div", id='mlfy_main_text')
    detail = str(detail)
    print(detail)

    # 清理
    detail = detail.replace('<h1>', '## ') #写成二级标题
    detail = detail.replace('</h1>', '')
    detail = detail.replace('<hr />', '')
    detail = detail.replace('<p>', '')
    detail = detail.replace('</p>', '\n')
    detail = detail.replace('<div id="mlfy_main_text">', '')
    detail = detail.replace('<div class="read-content" id="TextContent">', '')
    detail = detail.replace(' <dt class="bd"><script>chap_bg();</script></dt>', '')
    detail = detail.replace('<dt class="tp"><script>chap_top();</script></dt>', '')
    detail = detail.replace('<dt class="kw"></dt>', '')
    detail = detail.replace('<dt class="rd"><script>theme();</script></dt>', '')
    detail = detail.replace('    <dt class="bd"><script>chap_bg();</script></dt>', '')
    detail = detail.replace('<div class="main" id="TextContent">', '')
    detail = detail.replace('</div>', '')
    #print(detail)  
    return(detail)

# 循环处理章节并写入
for i in subtables:
    sublinks = i.find_all("li")
    substrong = i.strong.string
    print(substrong)

    filepage.write('# ' + substrong + '\n\n') #写入章节标题

    # 建立列表存放链接以排序
    chapters =[] 

    # 处理每个章节下面的链接
    for j in sublinks:
        try:
            chapter_url = j.a.get('href')# 获取子页面url 
            chapter_url = chapter_url.replace('/6/' + book_id, '')
            if 'html' in chapter_url: # 排除底部其他书籍推荐，抓取的多了
                chapters.append(chapter_url)
        except AttributeError: # 多余表格会填充空格，导致无法抓取
            pass

    chapters.sort() #排序
    for k in chapters:
        print(k)
        urlpage = book_url + k
        filepage.write(get_chapter(urlpage) + '\n\n') #写入单个页面


# 关闭文件
filepage.close()

print('done!')
# 
