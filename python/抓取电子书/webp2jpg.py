# coding=utf-8
# 下载打包漫画
# 20181112


import os

path = os.getcwd()
folder = os.path.basename(path)
#os.system('rm -rf tmp/')

 #转换webp
for file in os.listdir(path):
    fileext = os.path.splitext(file)[1]
    if fileext == '.webp':
        os.system('dwebp ' + file + ' -o ' + file +'.png' + ' -quiet')

print('--- webp to png ---')

# 转换jpg
os.system('mkdir tmp/')
for file in os.listdir(path):
    fileext = os.path.splitext(file)[1]
    if fileext == '.png':
        os.system('convert -scale 80% -quality 80% ' + file + ' tmp/' + file + '.jpg')
        os.system('rm -rf ' + file)

print('--- png to jpg ---')

# 打包转换
os.system('zip -r tmp.cbz tmp/')

# 转换mobi存在问题：封面会随机选择一个图片，如果添加一个封面为000.jpg，那么会转换成黑白的
os.system('ebook-convert tmp.cbz ' + folder +'.mobi --no-inline-toc')