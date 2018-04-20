# #!/usr/bin/env python
#
# # _*_ coding = utf-8 _*_
# from  flask import Flask,request,jsonify,make_response,abort
# from flask_cors import *
# import pymysql,xlrd
# from flask_restful import reqparse
# from datetime import datetime
# import configparser
# from . import testcases_api
# from interfacetest.Main import main
# import sys
#
# # import importlib
# # importlib.reload(sys)
#
# # from imp import reload
# # reload(sys)
# # sys.setdefaultencoding('utf-8')
#
# cf = configparser.ConfigParser()
# # path = 'db.config'
# path = u'E:\git\local\mock\db.config'
# cf.read(path)
# # print(cf.)
# # cf.read(path)
# secs = cf.sections()
# cf.get("database","dbcharset")
# _host= cf.get("database","dbhost")
# _port= cf.get("database","dbport")
# _dbname=cf.get("database","dbname")
# _dbuser=cf.get("database","dbuser")
# _dbpassword=cf.get("database","dbpassword")
# _path=cf.get("path","filepath")
#
# config ={
#         'host':_host,
#         'port':int(_port),
#         'user':_dbuser,
#         'passwd':_dbpassword,
#         'db':_dbname,
#         'charset':'utf8',
#         }
#
#
# @testcases_api.route('/runtest', methods=['GET'])
# def runtest():
#     parser = reqparse.RequestParser()
#
#     parser.add_argument('title', type=str)
#     parser.add_argument('project_name', type=str, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     try:
#         conn = pymysql.connect(**config)
#         cur = conn.cursor()
#         if args.get('projectName') == str(0):
#             sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s'),projectName from testcases where title like %s"
#             value = args.get('title').strip()
#             cur.execute(sql, value + '%%'.strip())
#         else:
#             sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s'),projectName from testcases where title like %s and projectName=%s"
#             values = (args.get('title') + '%%'.strip(), args.get('project_name'))
#             cur.execute(sql, values)
#         re = cur.fetchall()
#         conn.close()
#         key = ('id', 'status', 'title', 'reqparams', 'methods', 'domain', 'description', 'resparams', 'updateTime',
#                'projectName')
#         d = [dict(zip(key, value)) for value in re]
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#     return jsonify({'msg': "ok", "remark": "", "data": d})
#
#
#
# #运行所有测试用例
# @testcases_api.route('/runAllCase',methods=['POST','GET'])
# def runallcase():
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute(
#             "select id,title,reqparams,env,methods,domain,description,date_format(update_time,'%Y-%m-%d %H:%i:%s'),status,projectName,checkpoint,correlation from testcases where status=0")
#         re = cur.fetchall()
#         conn.close()
#         key = ('id', 'title', 'reqparams', 'env', 'methods', 'domain', 'description', 'update_time', 'status',
#                'projectName', 'checkpoint', 'correlation')
#         d = [dict(zip(key, value)) for value in re]
#
#         if d:
#             starttime, endtime, filename,result = main(d)
#             resulturl = 'http://192.168.10.24/testcase/results/result_'+ filename + '.html'
#             logpath = '/var/www/testcase/logs/'
#             conn = pymysql.connect(**config)
#             cur = conn.cursor()
#             cur.execute(
#                 'insert into testlogs (starttime,endtime,logname,logpath,url,result) values (%s,%s,%s,%s,%s,%s) ',
#                 (starttime,endtime,filename,logpath,resulturl,result))
#             conn.commit()
#             conn.close()
#
#
#         # for i in d:
#         #     print(i['id'])
#
#         # for i in range(len(d)):
#         #     print(d[i])
#         #     print(d[i])['id']
#             # print(case['id'])
#
#     except:
#         return jsonify({'msg': "fail", "remark": "服务器出现异常"})
#     return jsonify({'msg': "ok", "remark": "", "resultUrl": resulturl})
#
#
# # 测试结果
# @testcases_api.route('/result',methods=['GET'])
# def result():
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute("select id,starttime,endtime,url,result from testlogs order by id desc")
#         re= cur.fetchall()
#         conn.close()
#         key = ('id','starttime', 'endtime', 'url', 'result')
#         d = [dict(zip(key, value)) for value in re]
#
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#
#     # 处理日期时间字段
#     for data in d:
#         print("starttime:%s", data['starttime'])
#         data['starttime'] = data['starttime'].strftime('%Y-%m-%d %H:%M:%S')
#         data['endtime'] = data['endtime'].strftime('%Y-%m-%d %H:%M:%S')
#     return jsonify({'msg': "ok", "remark": "","data": d})
#
#
# @testcases_api.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)
#
# @testcases_api.errorhandler(500)
# def not_found(error):
#     return make_response("程序报错，可能是因为叙利亚战争导致", 500)
#
# if __name__=="__main__":
#     app.run(host='0.0.0.0',debug=True,threaded=True,port=5202)