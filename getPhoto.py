##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-7-18
# @Author  : Charles
# @备注    : 此接口已弃用，已注明！！！


# ！important flask source code（7行代码）
from flask import Flask
import pymongo
app = Flask(__name__)

@app.route('/')
def hello_world():

    return 'Worlds!'

    #连接mongo，读取test数据库下的photo_info表
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient["test"]
    mycol = mydb["photo_info"]

    # 获得前端传递的参数
    # name = request.get_json()
    # return jsonify(request.get_json(force=True))
    brr = ''
    for x in mycol.find():
        # arr.push(x)
        brr += "<img src='" + (x["folder_name"] + '\\' + x["file_name"]) + "'/>"

    return brr


if __name__ == '__main__':
    app.run()
