# code=utf-8
#  抓凯叔西游记
# 西游记 https://ksfan.net/story/kai-shu-xi-you-ji-quan-ji/page/1/
# 三国演义 https://ksfan.net/story/kai-shu-san-guo-yan-yi/page/1/
# 草房子 https://ksfan.net/story/cao-fang-zi/ 第一页不是/1/
# 201890111

import os
import time
import urllib.request
from bs4 import BeautifulSoup


def getsoup(url):
    headers = {'User-Agent'  :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
    req  = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'lxml')
    return(soup)

base_url = 'https://ksfan.net/story/cao-fang-zi/'


for i in range(6,7): #共14页
    soup = getsoup(base_url)
    soup = soup.find("div", id='playlist')
    for link in  soup.find_all("a"):
        linkmp3 = link.get('data-voiceurl')
        oldname = linkmp3.replace('/kstatic/kstory/story/audio/', '')
        newname = link.string
        newname = newname.replace('\n','')
        newname = newname.replace(' ','')
        newname = newname.replace('(','（')
        newname = newname.replace(')','）')
        newname = newname + '.mp3'

        cmd1 = 'wget https://cdn.kaishuhezi.com' + linkmp3.replace('/kstatic', '')
        print(cmd1)
        os.system(cmd1)
        cmd2 = 'mv ' + oldname + ' ' + newname
        print(cmd2)
        os.system(cmd2)
        time.sleep(2)


print('done!')
