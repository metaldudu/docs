# coding=utf-8
# annie下载b站多P视频，生成网址
# 20200913

import os

# 输入初始url
urlbase = 'https://www.bilibili.com/video/BV1jE411J7hk'

# 输入分p，最大数
pnum = 16

# 生成地址
urls = ''

for i in range(1, pnum+1):
  urlp = urlbase + '?p=' + str(i)
  urls = urlp + ' ' + urls

# 输出
print(urls)

# 执行annie
#cmd = 'annie ' + urls
#os.system(cmd) 
