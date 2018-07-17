##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-7-18
# @Author  : Charles
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

#检测数据库
# dblist = myclient.database_names()
# if "test" in dblist:
#   print("数据库已存在！")
arr = ''
mydb = myclient["test"]
mycol = mydb["photo_info"]
for x in mycol.find():
   # arr.push(x)
     arr += (x["folder_name"] + '\\' +  x["file_name"]) + '\n'
print(arr)



#
# 2018.7.18需求：
# 1.取值（文件夹名）
# 2.取值（文件名）
# 3.读取一张，存入一张，通过Gridfs的方式存入图片


# --* coding=utf-8 *--
# from cStringIO import StringIO
from pymongo import MongoClient
import gridfs
import os
import re
import matplotlib.pyplot as plt
import matplotlib.image as iming
import bson.binary
import numpy as np
import pymongo

if __name__ == '__main__':

        myclient = pymongo.MongoClient('mongodb://localhost:27017/')  # 创建连接点
        db = myclient.mydb
        imgput = gridfs.GridFS(db)
        dirs = 'C:\\Users\peng-pc\Desktop\images'
        files = os.listdir(dirs)
        for file in files:
                # 变量跟变量拼接注意
                filesname = '\\' + file
                file_name = filesname.strip().strip(' \ ')
                # print(filesname)
                print(file_name)
                imgfile = iming.imread(filesname)
                # iming.imsave('s.jpg',imgfile)
                # print type(imgfile),imgfile
                # imgfile.shape()
                plt.imshow(imgfile)
                plt.axis('off')
                plt.show()
                f = file.split('.')
                print
                f
                datatmp = open(filesname, 'rb')
                data = StringIO(datatmp.read())
                content = bson.binary.Binary(data.getvalue())
                # print content
                insertimg = imgput.put(data, content_type=f[1], filename=f[0])
                datatmp.close()
