##coding=utf-8\n\

import re
from bs4 import BeautifulSoup
import codecs

with codecs.open('in.html', 'r','utf-8') as fin,open('out.md','w') as fout:
    html=fin.read()
    soup=BeautifulSoup(html,'lxml')
    for tag in soup.find_all('div'):
        if 'bookTitle' in tag['class']:
            fout.write('# 笔记： 《'+tag.string.strip()+'》'+'\n\n')
        if 'authors' in tag['class']:
            fout.write('作者: '+tag.string.strip()+''+'\n')
        if 'noteHeading' in tag['class']:
            if tag.string==None:
                noteh=tag.contents[2].strip()
                #fout.write('\n---\n \n> 标注：'+noteh.split('-')[1]+'\n')
            else:
                fout.write('> 笔记'+'\n')
        if 'noteText' in tag['class']:
                fout.write('\n'+tag.string.strip()+'\n')