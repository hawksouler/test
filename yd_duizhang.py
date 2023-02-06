#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# /*==========================================================
# Program:yd_duizhang.py
# Author:kouity
# mail:kouity@163.com
# Version: V1.0 First release
# Created: 2020/11/10
# Explain: mis系统和移动返盘文件自动对账，可以按时间选择。
# eg:	yd_duizhang.py 20200727 20200729
#       不带参数默认当月至当前,带一个参数默认起始时间到当前
#       下载文件保存在./get_yd/目录,输出文件保存在./yd_temp/目录
# /*==========================================================

import sys
import datetime

from dateChange import str2date, date2str, day_range
from datetime import datetime, timedelta
from sftp_yd import ftp_get
from oracle_select import select_between


# 将下载的文件整理为列表形式,yd_list保存明细,ydhz_list保存每日汇总
def data_list(bgn, ecnd):
    begindate = str2date(bgn)
    enddate = str2date(end)
    dayList = day_range(begindate, enddate)
    strDayList = []
    # 将datetime格式转换为str格式
    for str in dayList:
        str = date2str(str)
        strDayList.append(str)

    yd_list = []
    ydhz_list = []

    for date in strDayList:

        path = 'get_yd/{date}'.format(date=date)
        # 下载的对账文件是GBK格式,先转码
        f = open(path, 'r', encoding='GBK')
        str1 = f.read()
        # 如果sftp服务器上不存在

        if len(str1) == 0:
            list1 = []
            list1.append('{date}.DZ文件sftp服务器上不存在'.format(date=date))

        else:
            list1 = str1.strip('\n').split('\n')

        if len(list1) == 1:
            ydhz_list.append(list1)
        else:
            for i in list1[:-1]:
                list2 = i.strip('|').split('|')
                yd_list.append(list2)
            # 汇总行写入一个列表
            ydhz_list.append(list1[-1:][0].strip('|').split('|'))

    return yd_list, ydhz_list


# 将两个渠道得来的数据对比,
def compare(mis_data, yd_data, ydhz_data):
    mis_data = mis_data
    yd_data = yd_data
    ydhz_data = ydhz_data
    yd_id_dict = {}  # 移动数据id为key,位置为value
    output_data = []  # 一致的输出到这个
    output_data_mis = []  # mis多出来的记录
    output_data_yd = []  # 移动多出来的记录
    output_data_diffient = []  # 日期或者金额不一致的

    # 生成以ID为key，以其他字段为value的字典
    for data in yd_data:
        yd_id_dict[data[0]] = data[1:]

    for data in mis_data:
        data = list(data)  # 将元组转换为列表
        # 如果mis数据中ID中在移动数据中存在则进入判断
        if data[0] in yd_id_dict:
            # 如果时间和金额不相等计入diffient列表，在mis数据之后加入移动的时间和金额数据，相同则计入主文件
            if data[4].strftime('%Y-%m-%d') != yd_id_dict[data[0]][0] or data[5] != float(yd_id_dict[data[0]][2]):
                data.extend([yd_id_dict[data[0]][0], yd_id_dict[data[0]][2]])
                output_data_diffient.append(data)
            else:
                data.extend([yd_id_dict[data[0]][0], yd_id_dict[data[0]][2]])
                output_data.append(data)
            # 如果在移动数据中找到ID则在字典中删除此条
            del yd_id_dict[data[0]]
        # 如果mis数据中ID中不存在则写入mis列表
        else:
            output_data_mis.append(data)

    # 如果字典中还有字段，移动数据多出的数据写入yd列表
    if yd_id_dict:
        for key in yd_id_dict:
            yd_id_dict[key].insert(0, key)
            output_data_yd.append(yd_id_dict[key])
    return output_data, output_data_diffient, output_data_mis, output_data_yd

    # 将列表写入同名文件文件
    def write_list(list):
        pass


if __name__ == "__main__":
    # 如果没有参数输入则从本月1日开始计算
    try:
        bgn = sys.argv[1]
    except IndexError:
        now = datetime.now()
        bgn = datetime(now.year, now.month, 1)
        bgn = date2str(bgn)
    # 如果没哟第二的参数默认到昨天
    try:
        end = sys.argv[2]
    except IndexError:
        end = datetime.today()
        end = end - timedelta(days=1)
        end = date2str(end)

    # 下载移动对账文件
    ftp_get(bgn, end)
    # 查询mis数据库对应文件
    mis_data = select_between(bgn, end)
    # 将对账文件整理为列表
    yd_data, ydhz_data = data_list(bgn, end)
    # 将整理好的列表分类整理
    output_data, output_data_diffient, output_data_mis, output_data_yd = compare(
        mis_data, yd_data, ydhz_data)

    # 写入每个文件的标题和文件时间
    f = open('yd_temp/output_data', 'w')
    f.write((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' 对账成功的记录\n')
    f = open('yd_temp/output_data_diffient', 'w')
    f.write((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' 日期或者金额有不同的记录\n')
    f = open('yd_temp/output_data_mis', 'w')
    f.write((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' mis系统多出的记录\n')
    f = open('yd_temp/output_data_yd', 'w')
    f.write((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' 移动对账文件多出的记录\n')
    f = open('yd_temp/output_hzyd', 'w')
    f.write((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' 移动对账日汇总表\n')

    # 将各列表写入文件
    with open('yd_temp/output_data', 'a') as f:
        for line in output_data:
            for word in line:
                f.write(str(word).strip('\n') + ', ')
            f.write('\n')

    with open('yd_temp/output_data_diffient', 'a') as f:
        for line in output_data_diffient:
            for word in line:
                f.write(str(word).strip('\n') + ', ')
            f.write('\n')

    with open('yd_temp/output_data_mis', 'a') as f:
        for line in output_data_mis:
            for word in line:
                f.write(str(word).strip('\n') + ', ')
            f.write('\n')

    with open('yd_temp/output_data_yd', 'a') as f:
        for line in output_data_yd:
            for word in line:
                f.write(str(word).strip('\n') + ', ')
            f.write('\n')

    with open('yd_temp/output_hzyd', 'a') as f:
        count, paid, sales = 0, 0, 0
        for line in ydhz_data:

            # 如果文件不存在则提示对账文件不存在

            for word in line:
                f.write(str(word).strip('\n') + ', ')
            f.write('\n')
            if len(line) != 1:

                count += int(line[2])
                paid += float(line[3])
                sales += float(line[4])
        f.write('\n')
        f.write('笔数:' + str(count) + '合计缴费:' + str(round(paid, 2)) +
                '销账金额' + str(round(sales, 2)) + '\n')
