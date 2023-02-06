#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# /*==========================================================
# Program:mysql_op.py
# Author:kouity
# mail:kouity@163.com
# Version: V1.0 First release
# Created: 2021/05/06
#Explain: mysql数据库操作
# /*==========================================================$

import pymysql


class Mysql(object):
    """mysql db operator"""

    def __init__(self, host, user, passwd, db):
        self._conn = pymysql.connect(
            host=host, user=user, password=passwd, database=db)
        self.cursor = self._conn.cursor()

    def queryAll(self, sql):
        # 查询sql返回的所有值
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def queryOne(self, sql):
        # 查询SQL语句返回的第一个值
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def queryBy(self, sql, nameParams={}):
        # 带参数查询sql语句,以list的形式设置参数,不输入参数同queryall
        # sql语句中参数用%s替代
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()

        if hasattr(self, '_conn'):
            self._conn.close()
