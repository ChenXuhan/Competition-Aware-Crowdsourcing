#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
from datetime import datetime


def str_to_list(x):
    if type(x) == str:
        if x:
            return x.split(',')
    return []


def str_to_list2(x):
    if type(x) == str:
        if x and len(x) > 2 and x[0]=='<' and x[-1]==">":
            return x[1:-1].split('><')
        else:
            if len(x)>0:
                raise Exception("TagString can't transform to list.", x)
            else:
                raise Exception("length of TagString is 0.")
    return []


def count_day(x):
    if isinstance(x,str):
        timeTuple = datetime.strptime(x[:10], "%Y-%m-%d")
        time0 = datetime.strptime("2008-07-31", "%Y-%m-%d")
        return (timeTuple-time0).days
    if isinstance(x,datetime):
        time0 = datetime.strptime("2008-07-31", "%Y-%m-%d")
        return (x-time0).days
    return 0


def printArray(arr,start='(',end=')',rep=','):
    arrStr = ""
    for obj in arr:
        arrStr += str(obj)+rep
    return start+arrStr[:-1]+end


if __name__ == '__main__':
    # result = str_to_list2("<winforms>")
    # print(result)
    # testArray = [5,6,7,8,9]
    # print(printArray(testArray,'|',"(",')'))
    print(count_day("2008-08-10 17:54:27.777"))