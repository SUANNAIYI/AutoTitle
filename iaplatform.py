import csv
from ctypes import *
# 导入Python的标准库os
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import TextIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, abort, jsonify, request, make_response
from Web_Title import *
from Web_Abstract import *
from flask import Flask, render_template,redirect, url_for, abort, jsonify, request, make_response
#from flask_sqlalchemy import SQLAlchemy  使用flask_sqlalchemy连接失败，换台电脑可以试一下
import datetime
# 利用pymysql连接数据库
import pymysql


app = Flask(__name__)
db = pymysql.connect(host="localhost", user="root",
                     password="123456", db="flask_platform")
cur = db.cursor()

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:5000/platform3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class user(db.Model):
    #表名
    __tablename__ = 'users'
    #字段
    username=db.Column(db.String(15), primary_key=True)
    password=db.Column(db.String(15), unique=True)


class article(db.Model):
    #表名
    __tablename__ = 'articles'
    # 字段
    time = db.Column(db.String(15), primary_key=True)
    content = db.Column(db.String(2000), unique=True)
    title = db.Column(db.String(20), unique=True)
    summary = db.Column(db.String(200), unique=True)
    user_name = db.Column(db.String(15), db.ForeignKey('users.username'))

'''

'''app是Flask的实例，接收包或者模块的名字作为参数，但一般都是传递__name__，
使得flask.helpers.get_root_path函数通过传入这个名字确定程序的根目录，以便获得静态文件和模板文件的目录。'''

# 获取当前文件所在目录
basepath = os.path.dirname(__file__)
# 将字符串按指定字符集转换成字节串
articlepath = bytes(basepath + "put-article.txt", "gbk")
summarypath = bytes(basepath + "out-summary.txt", "gbk")
titlepath = bytes(basepath + "out-title.txt", "gbk")
display = []
summary_result = []
title_result = []
Username = ""

# 使用app.route装饰器会将URL和执行的视图函数的关系保存到app.url_map属性上。
# 处理URL和视图函数的关系的程序就是路由，这里的视图函数就是calculate。

@app.route('/')
def index():
    return render_template('Home_page.html')


# WTF可能用于表单验
# 还未进行表单验证：1、注册时提示账号密码不能为空（即设置表单元素必填），并且账号不能重名且有长度限制（2-10），注册成功有提示信息。现在密码也不能重复，否则会报错，且有长度限制（4-16）（设置密码可以重复且在页面输入密码时设置成******的形式）
#               2、登录时提示账号密码不能为空（即设置表单元素必填），autocomplete记住账号密码，且登录成功有提示信息，登陆失败提示账号后密码错误。
@app.route('/reg', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' :
        # 取得表单中name为   的控件的值
        global Username
        Username = (request.form.get("username"))
        Password = (request.form.get("password"))
        Load = request.form.get("load")
        '''使用SQLAlchemy时的语句'''

        '''
        print(db.session.query(user.username).all())
        print(Username)
        username = (db.session.query(user.username).all())
        password = db.session.query(user.password).filter_by(username=Username).all()
        flag1=0
        if Load == '登录':
            if (Username,) in username:
                flag1 = 2
            else:
                 return "sorry"
            if flag1 == 2:
                if (Password,) in password:
                    return render_template('index.html', usname= Username)
                else:
                    return  "sorry"
        if Load == '注册':
            user1 = user(username=Username, password=Password)
            db.session.add(user1)
            db.session.commit()

    return render_template('login.html')'''
        ''' 使用pysql时的语句 '''
        sql1 = "select * from user"
        cur.execute(sql1)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        for row in results:
            username = row[0]
            password = row[1]
            print(username, password)
        flag1 = 0
        flag2 = 0
        if Load == '登录':
            for row in results:
                username = row[0]
                password = row[1]
                if Username in username:
                    flag1 = 2
                if flag1 == 2:
                    if Password in password:
                        return render_template('index.html', usname=Username)
            return "sorry"
        if Load == '注册':
            for row in results:
                username = row[0]
                password = row[1]
                if Username in username:
                    usernameis=2
                    flag2 == 2
                    return render_template('login.html',usernameis=usernameis)
                if flag2 != 2:
                    if Password in password:
                        usernameis = 2
                        return render_template('login.html',usernameis=usernameis)
            sql2 = "insert into user(username,password) VALUES ('%s','%s')" %(Username, Password)
            cur.execute(sql2)
            db.commit()
    return render_template('login.html')




@app.errorhandler(404)
def handel_error(ig):
    return jsonify('The file has been upload fail!')

@app.route('/data', methods=['POST', 'GET'])
def data():
    sql4 = "select * from article where user_name='%s'" %(Username)
    # 执行sql语句
    cur.execute(sql4)
    # 获取所有的记录
    results = cur.fetchall()
    return render_template('db.html',usname= Username,results=results)



@app.route('/delete', methods=['POST', 'GET'])
def delete():
    sql5 = "delete from article where time='%s'" %(id)
    cur.execute(sql5)
    # 获取所有的记录
    db.commit()
    sql4 = "select * from article where user_name='%s'" % (Username)
    # 执行sql语句
    cur.execute(sql4)
    # 获取所有的记录
    results = cur.fetchall()
    return render_template('db.html',usname= Username,results=results,id=id)

@app.route('/index', methods=['POST', 'GET'])
# 函数content
def content():
    sum_res = ""
    tle_res = ""
    # 采用HTTP的POST连接方式
    if request.method == 'POST':
        # 取得表单中name为type的控件的值
        btn = request.form.get("type")
        # 根据控件的Value值判断当下选择的按钮
        if btn == '上传':
            # 获取上传的文件
            file = request.files['file']
            # 判断文件是否上传成功
            if file is None:
                abort(404)
            # 获取上传文件的文件名
            filename = file.filename
            # 对文件名进行安全检测
            filename = secure_filename(filename)
            # os.path.dirname 去掉文件名，返回目录
            newfilepath = basepath + filename
            file.save(newfilepath)
            new_file = open(newfilepath, encoding='utf-8')
            upload_str = new_file.read()
            new_file.close()
            tmplenu = len(upload_str)
            if tmplenu > 0:
                display.append(upload_str)
            display_str = ''.join(display)
            return render_template('Index.html', dispalytext=display_str, displaysummary=sum_res,
                                   displaytitle=tle_res, usname= Username)

        if btn == '一键生成':
            article = request.form.get("Article-content-text")
            article_input = open("put-article.txt", 'w', encoding='utf-8')
            article_input.write(article)
            article_input.close()
            tmplec = len(article)
            display.clear()
            if tmplec > 0:
                display.append(article)
            display_str = ''.join(display)
            Abstract()
            Title()
            summary_file = open("out-summary.txt", encoding='utf-8')
            summary_str = summary_file.readline()
            tmplens = len(summary_str)
            if tmplens > 0:
                summary_result.append(summary_str)
                sum_res = ''.join(summary_result)
            title_file = open("out-title.txt", encoding='utf-8')
            title_str = title_file.read()
            tmplent = len(title_str)
            if tmplent > 0:
                title_result.append(title_str)
                out = ''.join(title_result)
                tle_res = str(out).replace(" ", "")
            now_time =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql3 = "insert into article(time,content,title,summary,user_name) VALUES ('%s','%s','%s','%s','%s')" % (now_time, display_str,title_str,summary_str,Username)
            cur.execute(sql3)
            db.commit()
            return render_template('Index.html', dispalytext=display_str, displaysummary=sum_res,
                                   displaytitle=tle_res, usname= Username)
        if btn == '清除':
            # 清除文件put-article.txt中的内容
            article_input = open("put-article.txt", 'w')
            article_input.close()
            # 清除控件textare中的内容
            display.clear()
            # 清除文件out-summary.txt中的内容
            summary_file = open("out-summary.txt", 'w')
            summary_file.close()
            # 清除控件textare中的内容
            summary_result.clear()
            sum_res = ''.join(summary_result)
            # 清除文件out-title.txt中的内容
            title_file = open("out-title.txt", 'w')
            title_file.close()
            # 清除控件textare中的内容
            title_result.clear()
            tle_res = ''.join(title_result)
            # 从模版文件夹templates中呈现给定模板index.html的上下文
            return render_template('Index.html', displaytext=display, displaysummary=sum_res,
                                   displaytitle=tle_res, usname= Username)
    # 从模版文件夹templates中呈现给定模板index.html的上下文
    return render_template('Index.html',usname= Username)





# 当其他程序调用此程序模块的时候，不运行main函数；但是当直接运行此程序模块的时候，运行main函数。
if __name__ == '__main__':
    # 监听指定的端口,对收到的request运行app生成response并返回
    app.run(debug=True)

# if __name__ == '__main__':
# app.run()
