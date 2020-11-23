#coding=utf-8  
# 安装库 pyscreenshot 以截图
# 豆瓣阅读浏览器在左边，循环抓图到png，然后再ocr。实现了键盘精灵的功能。
# 20190203

import pyscreenshot as ImageGrab
from pykeyboard import PyKeyboard # 键盘模拟
import time

k = PyKeyboard()
# 先切换到chrome浏览器
k.press_key(k.alt_key)
k.tap_key(k.tab_key)
k.release_key(k.alt_key)

# 截图部分

for i in range(1,370):
    fname = j
    print(fname)
    im=ImageGrab.grab(bbox=(120,180,860,1000))
    im.save(fname + '.png')
    k.tap_key('j')
    time.sleep(3)
#im.show()

