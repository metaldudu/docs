##coding=utf-8
# 20181210 用 pyecharts 显示柱状图

from pyecharts import Line, Bar, Pie, EffectScatter
# 数据
attr =["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", ]
v1 =[5, 20, 36, 10, 10, 100, 36, 10, 10, 100, 11, 11]
v2 =[55, 60, 16, 20, 15, 80]

bar = Bar('豆瓣年度阅读', '2018')
bar.add('数量', attr, v1,  is_label_show=True, area_color='#a3aed5')
bar.show_config()
bar.render(path='book.html')

