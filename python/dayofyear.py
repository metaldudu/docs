#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 显示今天是今年的第几天并进度条展示

import datetime

dayCount = datetime.date.today().timetuple().tm_yday;
percent = ((int(dayCount)+0.001)*100/365);

# print (str(dayCount));

print (str(dayCount) + '/365' + (dayCount//10)*'█' + ((365-dayCount)//10)*'░' + str('%4.2f' % percent) + '% ');
