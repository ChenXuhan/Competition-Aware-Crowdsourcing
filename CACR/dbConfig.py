#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
import pymysql
dbcfg = {
    'host': '192.168.7.119',
    'port': 3306,
    'user': 'root',
    'password': 'mysql123',
    'db': 'stackoverflow',
    'cursorclass': pymysql.cursors.DictCursor
}