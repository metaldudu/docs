# coding=utf-8
# 喜马拉雅下载图形界面，尝试了tkinter。20190510

import tkinter as tk
import os
import subprocess
import json
import requests
from bs4 import BeautifulSoup

# 专辑详情
# album_url = 'https://www.ximalaya.com/youshengshu/11018641/'

json_url = 'http://www.ximalaya.com/tracks/{}.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

def get_album_info(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    # 专辑名称
    album_title = soup.title.string.replace(' ', '')

    # 节目列表
    mp3_list = []
    mp3_div = soup.find_all('div', {'class': ['text', ' ']})
    for div in mp3_div:
        title = div.a.get('title')  # 获得节目名称
        id = div.a.get('href').split('/')[-1]  # 获得节目ID
        mp3_list.append({'title': title, 'id': id})

    if mp3_list:
        print('--节目清单--\n', mp3_list[0:5])
        album_num = len(mp3_list)
    else:
        print('-没发现节目!-\n', mp3_div[0:5], '-------\n')

    return album_title, album_num, mp3_list #返回专辑名、数量、节目列表

# 下载单个节目
def download_mp3(id,pre):
    mp3_info = requests.get(json_url.format(id), headers=headers).json()
    # 替换文件名中的特殊字符
    title = mp3_info['title'].replace('\"', '“').replace(':', '：').replace(' ', '')
    mp3_url = mp3_info['play_path']

    filepath = os.getcwd()
    filename = pre + '-{}.m4a'.format(title)

    if os.path.exists(filepath+filename):
        return '- {}    已存在\n'.format(title)

    # 用 aira2 下载
    cmd = 'aria2c {} -d {} -o \"{}\"'.format(mp3_url, filepath, filename)
    retcode = subprocess.call(cmd, shell=True)
    if not retcode:
        return '- {}    已下载\n'.format(title)
    else:
        os.remove(filepath+filename)
        return '- {}    下载出错: {}\n'.format(title, retcode)


# 窗口初始化
top = tk.Tk()
top.geometry('600x400+500+200')
top.title('喜马拉雅下载器')



# 标签控件，显示专辑名
labelInfo = tk.Label(top, text = "", fg = "#FF4500")
labelInfo.place(x=20, y=40, height = 25, width = 300)

# 输入框控件，输入专辑地址
entUrl = tk.Entry(top, text = "")
entUrl.place(x=20, y=10,width=320, height=25)

# 列表显示控件
lsbAlbum = tk.Listbox(top, bd=1)
lsbAlbum.place(x=20, y=70, width=550, height=320)

# 信息按钮函数
def btnInfoClicked():
    # out = get_album_info("https://www.ximalaya.com/qita/10345316/")
    out = get_album_info(entUrl.get())
    labelInfo.config(text = out[0])
    # labelInfo.config(text = "这是一个专辑名称、节目数量")
    for item in out[2]:
        lsbAlbum.insert(tk.END, item['title'])

# 下载按钮函数
def btnDownClicked():
    out = get_album_info("https://www.ximalaya.com/qita/10345316/")
    num = len(out[2])

    j = 1 # 添加序号
    for i in out[2][0:num]:
        # print(i['id'])
        prefix = str(j).zfill(3)
        download_mp3(i['id'], prefix)
        j = j+1

# 按钮控件
btnInfo = tk.Button(top, text = "显示信息", command = btnInfoClicked)
btnInfo.place(x=370, y=10, width=80, height=25)

btnDown = tk.Button(top, text = "下载", command = btnDownClicked)
btnDown.place(x=460, y=10, width=80, height=25)


top.mainloop()
