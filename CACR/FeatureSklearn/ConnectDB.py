#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
from CACR.dbConfig import *


def connectDB():
    con = pymysql.connect(**dbcfg)
    # print("Connected to database successfully.")
    return con


def executeSQL(con, sqlstr):
    cur = con.cursor()
    cur.execute(sqlstr)
    rows = cur.fetchall()
    return rows


def connectTest():
    try:
        con = connectDB()
        sqlstr = "INSERT INTO ques_tags (tagId,quesId) VALUES(3,4);"
        # sqlstr = 'select * from answers2 limit 5;'
        answers = executeSQL(con, sqlstr)
        for row in answers:
            print(row)
    except Exception as e:
        print("Execution was failed.")
        print(e)
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    connectTest()