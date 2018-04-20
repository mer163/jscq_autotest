#!/usr/bin/env python

# _*_ coding = utf-8 _*_

from flask import jsonify, Flask,make_response,request
import pymysql,sys
# import ConfigParser
import configparser
# from imp import reload

# reload(sys)
# sys.setdefaultencoding('utf-8')

import sys
import importlib
importlib.reload(sys)
print(sys.getdefaultencoding())
app = Flask(__name__)

cf = configparser.ConfigParser()
path = u'/usr/local/mock/db.config'
#path = u'E:\git\local\mock\db.config'
cf.read(path)
cf.read(path)
secs = cf.sections()
_host= cf.get("database","dbhost")
_port= cf.get("database","dbport")
_dbname=cf.get("database","dbname")
_dbuser=cf.get("database","dbuser")
_dbpassword=cf.get("database","dbpassword")
_path=cf.get("path","filepath")

config ={
        'host':_host,
        'port':int(_port),
        'user':_dbuser,
        'passwd':_dbpassword,
        'db':_dbname,
        'charset':'utf8',
        }

def checksize(domain,method):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    size = cur.execute('select * from mock_config where domain=%s', (domain))  # 校验domain是否存在
    size1 = cur.execute('select * from mock_config where methods=%s', (method))  # 校验method是否存在
    conn.close()
    if size == 0:
        return jsonify({"msg": "请求方法不存在"})
    elif size1 == 0:
        return jsonify({"msg": "请求方法对应的请求模式不存在"})

def gentolist(gen):
    for i in gen:
        yield i

def checkpath(domain,varsvalue,method):
    print("domain %s",domain)
    print("var %s", varsvalue)
    print(type(varsvalue))
    print("method %s", method)
    method=method.lower()

    # 此处增加判断接口请求地址是否存在的方法


    li = list(gentolist(varsvalue))
    # for i in varsvalue:
    #     print(i)
    # test = []
    # test = varsvalue

    li.sort
    checksize(domain,method)#判断请求方法和模式是否匹配
    if len(li) == 0:
        conn = pymysql.connect(**config)
        cur = conn.cursor()

        cur.execute('select resparams from mock_config where status=0 and domain=%s and methods=%s', (domain, method))
        resparams = cur.fetchone()
        conn.close()
        print(type(resparams))

        ##########此处增加拼装原请求，并发送请求，得到相应内容后直接return实际请求结果############
        ##########待实现############


        if resparams is None:
            return jsonify({"msg": "请检查请求接口地址或请求方法有误"})
        # if len(resparams) == 0:
        #     print("resparams is null")
        #     return jsonify({"msg": "数据库查询没有该参数"})
        if resparams[0] == '':
            return jsonify({"msg": "对应请求没有配置预期返回值"})
        else:
            return resparams[0].encode("utf-8")
    else: #进入mock
        varsvalue1=getvar(li)#实际请求
        conn = pymysql.connect(**config)
        cur = conn.cursor()

        cur.execute('select reqparams,resparams,methods,ischeck from mock_config where status=0 and domain=%s and methods=%s',(domain, method))
        reqparams = cur.fetchall()
        if reqparams == ():
            return jsonify({"msg": u"请求方法和参数不匹配"})

        ####判断条件需要修改， 增加ischeck=1 是否校验参数   0不校验，1校验
        elif reqparams[0][3]==0:
            return reqparams[0][1]

        elif reqparams[0][3]==1:
            rdata=checkparams(reqparams,varsvalue1)
        return rdata

def checkparams(reqparams,varsvalue1):
    varsvalue2 = reqparams[0][0]  # 数据库中的预期请求参数
    if reqparams[0][2].lower()=='get' or (reqparams[0][2].lower()=='post' and varsvalue1[0] != '}' and varsvalue1[-2] != '}'):
        arr = varsvalue2.split('&')
        for i in range(len(arr)):
            arr[i] = arr[i] + '&'
        arr.sort(reverse=True)
        str = ''.join(arr)[0:-1]
        if str==varsvalue1:
            return reqparams[0][1].encode("utf-8")
        if reqparams[0][0] == '':
            return jsonify({"msg": u"对应请求没有配置预期返回值"})
        else:
            return jsonify({"msg": u"请求方法和参数不匹配"})
    elif reqparams[0][2].lower()=='post':
        varsvalue1 = varsvalue1.replace("\t", "").replace("\r", "").strip()[:-1]
        varsvalue2 = varsvalue2.replace("\t", "").replace("\r", "").strip()
        if varsvalue1 == varsvalue2:
            return reqparams[0][1].encode("utf-8")
    else:
        return jsonify({"msg": u"暂不支持该类型请求方法"})

def getvar(value):
    value=value[::-1]
    result = ''
    f = 0
    for i in range(len(value)):
        for j in range(len(value[i])):
            if f % 2 == 0:
                result = result + value[i][j] + '='
                f = f + 1
            else:
                result = result + value[i][j] + '&'
                f = f + 1
    return result[0:-1]

@app.route('/<path:path>/<path:path1>', methods=['GET','POST'])
def get_all_task(path,path1):
    npath='/' + path + '/' + path1
    # npath = path + '/' + path1
    print(npath)
    if request.method=='GET':
        request.args.items()
        varsvalue = request.args.items()
        print(type(varsvalue))
    else:
        varsvalue = request.form.items()
        print(type(varsvalue))
    r = checkpath(npath, varsvalue, request.method)
    return r

@app.route('/<path:path>', methods=['GET','POST'])
def get_all_task1(path):
    path='/'+path
    # path =  path
    print(path)
    if request.method=='GET':
        varsvalue = request.args.items()

        # varsvalue.sort()
    else:
        varsvalue = request.form.items()
        # varsvalue.sort()
    r = checkpath(path, varsvalue, request.method)
    return r

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5201,threaded=True)
