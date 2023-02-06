#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# /*==========================================================
# Program:oracle_select.py
# Author:kouity
# mail:kouity@163.com
# Version: V1.0 First release
#Created: 2020/11/9
#Explain: oracle数据库操作
# /*==========================================================$

import cx_Oracle


class Oracle(object):
    """oracle db operator"""

    def __init__(self, user, passwd, host, db):
        self._conn = cx_Oracle.connect(
            "%s/%s@%s/%s" % (user, passwd, host, db))
        self.cursor = self._conn.cursor()

    def queryTitle(self, sql, nameParams={}):
        # 查询表的列名
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
        else:
            self.cursor.execute(sql)

        colNames = []
        for i in range(0, len(self.cursor.description)):
            colNames.append(self.cursor.description[i][0])
        return colNames

    def queryAll(self, sql):
        # 查询sql返回的所有值
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def queryOne(self, sql):
        # 查询SQL语句返回的第一个值
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def queryBy(self, sql, nameParams=[]):
        # 带参数查询sql语句,以字典的形式设置参数,不输入参数同queryall
        # sql语句中参数以：key的形式出现
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insertBatch(self, sql, nameParams=[]):
        # 批量插入数据
        """batch insert much rows one time,use location parameter"""
        self.cursor.prepare(sql)
        self.cursor.executemany(None, nameParams)
        # self.commit()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()

        if hasattr(self, '_conn'):
            self._conn.close()
