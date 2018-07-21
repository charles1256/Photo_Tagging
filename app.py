##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-7-18
# @Author  : Charles
from asyncio.base_events import Server

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for

import os
import re
import hashlib
import select_insert_db
import json
import logging
import pymongo

app = Flask(__name__)
app.secret_key = b'\x04\xff\x8c\x931\xe1\xdf\x92\x06\xf5'
app.logger.setLevel(logging.INFO)

# @app.route('/')
# def hello_world():
#     return 'pxxxx!'

@app.route("/")
def index():
    app.logger.info("这里是首页")
    return render_template('index.html',list=arr);
    # 测试
    #  return 'dklasdsak'
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
arr = ''
mydb = myclient["test"]
mycol = mydb["photo_info"]
for x in mycol.find():
   # arr.push(x)
     arr += "<div class='li'>" + (x["folder_name"] ) +  "</div>"
print(arr)


@app.route("/getPhoto",methods=["POST"])
def getPhoto():
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



@app.route("/pro/login", methods=["POST"])
def login():
    app.logger.info("已经来到register页面啦.")
    username = StringField(label = u'用户名',validators =[DataRequired()])
    password = PasswordField(label = u'面',validators =[DataRequired()])
    submir = SubmitFiled(label = u'提交')


    # # 需要直接返回js语句，让页面自动刷新
    # # 接受到请求的json数据
    app.logger.info("来到login页面啦.")
    # accept_json=request.get_data()
    # 接收到的数据必须是 username=charles &password=123456780
    accept_json = request.get_data().decode("utf-8")
    print("接收的数据",accept_json);
    username = re.search(r"=([^&]*)", accept_json).group(1)
    password = re.search(r"&.*?=(.*)$", accept_json).group(1)
    session["user_name"] = username
    # accept_dict=json.loads(accept_json)
    # accept_content=accept_json.decode("utf-8").encode("utf-8").split("&")
    # print(accept_json.decode("utf-8"))

    # 到数据库中检索一下，传输过去，经过加密的数据
    # 是否存在这个账户
    # 存在这个账户，那么登录成功
    # 不存在这个账户，提示重新登录，账号密码有错误
    # 调用函数，处理
    result = handle_data("login", username=username, password=password)

    # 根据result，决定返回值
    # if result:
    #     pass
    # else:#返回正确登录的js
    #     #返回登录错误的js
    #     pass

    response = get_js(task_type="login", request_status=result, username=username)
    app.logger.info(url_for("register"))
    return (response).encode("utf-8")



@app.route("/pro/register", methods=["POST"])
def register():
    app.logger.info("来到register 页面了")
    app.logger.info("已经来到register页面啦.")

    username = StringField(label=u'用户名', validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名必须由字母，数字，下划线组成')])
    password = PasswordField(label=u'面', validators=[DataRequired(),EqualTo('passowrd'),message = 'password must be'])
    submir = SubmitFiled(u'马上注册')

    app.logger.warning("zhehsiygie jinggao ")
    # 需要直接返回js语句，让页面自动刷新
    # 首先要获取发送过来的信息，name,password
    accept_json = request.get_data().decode("utf-8")
    username = re.search(r"=([^&]*)", accept_json).group(1)
    session["user_name"] = username
    password = re.search(r"&.*?=(.*)$", accept_json).group(1)
    # 将其加入到数据库中


    # 进行hex md5 加密
    # 返回js语句，更改状态。
    # 调用函数进行处理
    result = handle_data(task="register", username=username, password=password)
    
    # 判断结果，返回响应的js
    # if result:
    #     #注册成功，返回正确的js
    #     pass
    # else:
    #     #注册失败，返回错误的js
    #     pass
    response = get_js(task_type="register", request_status=result, username=username)
    
    # response_header="HTTP/1.1 200 OK\r\n\r\n"   
    return (response).encode("utf-8")


@app.route("/getPhoto",methods=["POST"])
def get_photo():

    img_title_list=[]
    session["img_count"]=len(img_title_list)
    # app.logger.warning("22222222222222")
    img_title_list=get_img()
    # app.logger.warning("33333333333")
    return img_title_list

def get_img():
    # app.logger.warning("4444444")
    # 连接数据库
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",
                                              user_name=session["user_name"]
                                              )
    #从数据库取得图片的标题

    # app.logger.warning("55555555")
    app.logger.info("--get_img _title")
    app.logger.info(session["img_count"])
    img_title_list=manager_sql.get_user_own_img_title(session["img_count"])
    # app.logger.warning("66666666")
    # session["img_count"]+=len(img_title_list)
    # 直接返回图片的标题
    if len(img_title_list)<=0:
        return ""
    return json.dumps(img_title_list)


@app.route("/turn_page/<flag>",methods=["GET"])
def turn_page(flag):
    app.logger.info(session["img_count"])
    app.logger.info(flag)
    if session["img_count"] == 0:
        if flag=="up":
            app.logger.info(session["img_count"])
        elif flag == "down":
            session["img_count"]+=10
            app.logger.info(session["img_count"])
    elif flag == "up":
        session["img_count"]-=10
    elif flag == "down":
        session["img_count"]+=10
    app.logger.info(session["img_count"])
    img_title_list=get_img()

    app.logger.info(json.loads(img_title_list))
    return img_title_list


@app.route("/getPhoto/<image_name>")
def get_one_image(image_name):
    #调用处理函数，返回image,

    # app.logger.info(image_name)
    read_img(image_name)
    response="""
                $(".show_img").empty().html('<img src="%s" width="500" height="500"/>');
    
        """ %session["image_path"]
    # app.logger.info(response)
    return response

def read_img(image_name):
    #连接数据库
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",user_name=session["user_name"])
    #获得路径
    image_path=manager_sql.get_user_own_img_path(image_name)
    session["image_path"]=image_path
    #返回图片
    try:
        f=open(image_path,"rb")
    except Exception:
        return "您好数据出问题啦！".encode("utf-8")
    else:
        image_content=f.read()
        return image_content


@app.route("/images/<image_photo>")
def look_image(image_photo):
    try:
        f=open("images/"+image_photo,"rb")
    except Exception:
        response="打不开"
        app.logger.info("打不开")
    else:
        response=f.read()
        app.logger.info("数据打开成功")

    return response
def handle_data(task, username, password, ):

    app.logger.info("来到数据处理啦")
    '''哈希加密，对数据进行哈希加密，并调用相关的处理方法，操作成功返回True，操做失败返回False'''
    ha_password = hashlib.md5(password.encode("utf-8")).hexdigest()
    app.logger.info(type(ha_password))
    # 创建数据库管理对象，
    manager_sql = select_insert_db.ManagerMysql(table_name="user_infomation", user_name=username, password=ha_password)
    # 根据调用的函数，选择合适的操作，返回True或者
    if task == "register":
        result = manager_sql.add_infomation()
    elif task == "login":
        result = manager_sql.retrieve()
    else:
        result = False
    manager_sql.close_mysql_connect()
    return result


def get_js(task_type, request_status, username):
    app.logger.info("来到返回数据页面啦")
    # 根据task_type判断返回时登录还是注册的js
    page_js = None
    if task_type == "login":
        # 这是登录页面调用的，要返回js
        if request_status:
            page_js = """
                $("#non_login").css("display","none");
                $("#login").css("display","block");                
                $("#two_span").text("注册成功，欢迎!");
                show_title_and_img();
               
               
            """ % username
        else:
            page_js = """
               
                alert("登录失败");
                $("#one_span").css("color","red");
                $("#one_span").text("您好，账号或密码错误，请重新登录");             
            """
            # 根据request_status 返回正确或者失败的js。
    elif task_type == "register":
        # 这是注册页面调用的。
        if request_status:
            page_js = """
                $("#non_login").css("display","none");
                $("#login").css("display","block");                
                $("#two_span").text("欢迎 %s,开始使用!");
                show_title_and_img();
               
            """ % username
        else:
            page_js = """
               
                $("#one_span").css("display","block");
                $("#one_span").text("您好，您注册的账号已经存在，请选择新的账号！");
               
            """

    return page_js

def up_load_photo():
    #创建数据库对象，
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",
                                              user_name=session["user_name"],
                                              img_ascription=session["user_name"],
                                              img_path=session["file_path"],
                                              img_size=session["file_size"],
                                              image_name=session["file_title"])
    result=manager_sql.add_infomation()
    #将数据插入到数据库中，返回True
    return result


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.2')
    livereload = Server(app.wsgi_app)
    livereload.watch('**/*.*')
    livereload.server(open_url = True)
