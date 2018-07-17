##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-7-18
# @Author  : Charles

import os
import numpy as np
import pandas as pd

from pymongo import MongoClient

path = "C:\\Users\\peng-pc\\Desktop\\images"

def gci(path):
      """this is a statement"""
parents = os.listdir(path)

#返回文件名
for parent in parents:
    child = os.path.join(path, parent)
# print(child)
if os.path.isdir(child):
    gci(child)
# print(child)
else:
     print(child)
gci(path)
# print(gci.__doc__)  # 显示函数声明部分内容(statement)


def function_name(param):
    """"""
    # this is a
    # statement.
    """"""
# 可以使用函数的属性__doc__来返回该声明，如print(function_name.__doc__)
# 使用os.walk方法遍历：

path = "C:\\Users\\peng-pc\\Desktop\\images"
for i in os.walk(path):
    # print(i[2])
   # print(i)
    #  foldername = '\n'.join(i[1])  #  打印目录名：image	images	images1
    #  filename = '\n'.join(i[2])
    #  # print(foldername)
    #  # print(filename)
    list2 = [x for x in i[2] if x != []]
    print(list2)   #打印文件名：['1.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg', '2.jpg', '20.jpg', '21.jpg', '22.jpg', '23.jpg', '24.jpg', '25.jpg', '26.jpg', '27.jpg', '28.jpg', '29.jpg', '3.jpg', '30.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']







