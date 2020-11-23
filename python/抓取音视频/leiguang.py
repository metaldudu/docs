# code=utf-8
# 抓取leiguang.cc网上的视频

# ffmpeg -i https://vip.94kuyun.com/20171226/vkIlIYGy/hls/index.m3u8 -c copy -bsf:a aac_adtstoasc output.mp4
# ffmpeg -i https://vip.94kuyun.com/20171226/vkIlIYGy/hls/index.m3u8 -c copy output.ts

import requests
import re
import os

# 整个季页面
url_season = 'https://www.leiguang.cc/emotion/haosiyishengdiyiji/'
url_season_play = url_season + 'meijuplay-0-0.html'


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


# 函数：获取分集播放页面地址
def get_list(url):
    page = get_page(url)
    url_list = re.findall(r'https://vip.94kuyun.com/share/\S{16}', page) # 正则匹配16位字符串
    return(url_list)



#输出部分
list1 = get_list(url_season_play)
num = 1
for i in list1:
    print(num,end=': ')
    print(i)
    num = num +1


# 函数：获取播放列表地址m3u8，下载速度太慢弃用
def get_m3u():
    url = 'https://vip.94kuyun.com/share/d60j8imTMBVIFvNf'
    page = get_page(url)
    url_list = re.findall(r'\S{16}/index.m3u8', page) # 正则匹配16位字符串
    print(url_list)

