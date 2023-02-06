# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# /*==========================================================
# Program:csv_to_emal.py
# Author:kouity
# mail:kouity@163.com
# Version: V1.0 First release
# Created: 2022/06/15
# Explain: 发送指定的csv文件给固定的email
# /*==========================================================$


import datetime
import pandas as pd

import oracle_op
from email_op import MyEmail
from datetime_op import get_last_month

dt = str(get_last_month(datetime.date.today()))

# 建立mis数据库连接，建立游标
file_path = 'F:\Pythontest\pytest_liunx\mydata\\'
mis = oracle_op.Oracle('lymis', 'lyzls', '192.168.0.2:1521', 'orcl')
key = ["碧桂园天荟", "长兴府", "时代城", "珑悦"]
att_list = []
for i in range(len(key)):
    sql = "select a.hh,b.khmc,b.txdz,a.scsl\
                from cb_slb a,da_khxx b \
                where a.hh=b.khh and b.txdz like '%{key}%' \
                and sfyf=date'{date}' order by a.hh" .format(key=key[i], date=dt)
    # print(sql)
    data = mis.queryBy(sql)
    mis_df = pd.DataFrame(data)
    mis_df.columns = [['户号', '户名', '装表位置', '水量']]
    # print(mis_df)
    file_name = file_path + key[i] + dt + '.csv'
    mis_df.to_csv(file_name, encoding="utf_8_sig")
    att_list.append(file_name)
# 创建邮件
emailsubject = '发送本月{key}水量数据'.format(key='碧桂园')
text1 = '{date}的{key}水量情况表'.format(date=dt, key='碧桂园')
SendOut = MyEmail(att=att_list, emailsubject=emailsubject,
                  text=text1, receivers=['35950375@qq.com'])
# mytest.text='now test'
SendOut.sendmail()
