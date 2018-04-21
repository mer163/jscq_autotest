# import sys
#
# # import importlib
# # importlib.reload(sys)
#
# # from imp import reload
# # reload(sys)
# # sys.setdefaultencoding('utf-8')
# # _*_ coding = utf-8 _*_
# from  flask import Flask,request,jsonify,make_response,abort,redirect,render_template
# from flask_login import login_user, logout_user, login_required, \
#     current_user
# from flask_cors import *
# import pymysql,xlrd
# from flask_restful import reqparse
# from datetime import datetime
# import configparser
# from . import testcases_api
# from interfacetest.Main import main
#
# cf = configparser.ConfigParser()
# # path = 'config.ini'
# path = u'E:\git\local\mock\config.ini'
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
# save_path=_path
# ALLOWED_EXTENSIONS = ['xls', 'xlsx']
# app=Flask(__name__)
# CORS(app, supports_credentials=True)
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
# @testcases_api.route('/import_excel', methods=[ 'POST'])
# def import_device():
#     file = request.files['files[]']
#     filename = file.filename
#     # 判断文件名是否合规
#     if file and allowed_file(filename):
#         file.save(save_path+filename)
#         excelName = save_path+filename
#         bk = xlrd.open_workbook(excelName, encoding_override="utf-8")
#         sh = bk.sheets()[0]  # 因为Excel里只有sheet1有数据，如果都有可以使用注释掉的语句
#         ncols = sh.ncols#列
#         nrows = sh.nrows#行
#         conn = pymysql.connect(**config)
#         cur = conn.cursor()
#         for j in range(1,nrows):
#             if j+1 == nrows:
#                 return jsonify({'msg': "ok", "remark": "上传成功"})
#             else:
#                 lvalues = sh.row_values(j+1)
#                 if lvalues[6]=='是':
#                     ischeck = 0
#                 elif lvalues[6]=='否':
#                     ischeck = 1
#                 else :
#                     ischeck = 1
#                 try:
#                     cur.execute('insert into mock_config values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(None,lvalues[0],lvalues[4],lvalues[3],lvalues[2],lvalues[7],lvalues[5],datetime.now(),0,ischeck,lvalues[1]))
#                     conn.commit()
#                 except:
#                     return jsonify({'msg': "fail", "remark": "解析失败"})
#         conn.close()
#         return jsonify({'msg': "ok", "remark": "上传成功"})
#     else:
#         return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})
#
# @testcases_api.route('/addinfo',methods=['POST'])
# def query_user():
#     parser = reqparse.RequestParser()
#     parser.add_argument('title', type=str,required=True)
#     parser.add_argument('method', type=str,required=True)
#     parser.add_argument('reqparams', type=str, required=True)
#     parser.add_argument('resparams', type=str, required=True)
#     parser.add_argument('des', type=str)
#     parser.add_argument('domain', type=str,required=True)
#     parser.add_argument('projectName', type=str,required=True)
#     parser.add_argument('ischeck', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     print(args)
#
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute('insert into mock_config (title,reqparams,methods,domain,description,resparams,status,ischeck,project_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ',(args.get('title'),args.get('reqparams'),args.get('method'),args.get('domain'),args.get('des'),args.get('resparams'), 0 , args.get('ischeck'),args.get('projectName')))
#         conn.commit()
#         conn.close()
#     except :
#         return jsonify({'msg': "fail", "remark": "新增数据失败"})
#     return jsonify({'msg': "ok","remark":""})
#
# @testcases_api.route('/delinfo',methods=['POST'])
# def delinfo():
#     parser = reqparse.RequestParser()
#     parser.add_argument('id[]', type=str, required=True,action='append')
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     id=args.get('id[]')
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         for index in range(len(id)):
#             idd=id[index]
#             cur.execute('delete from mock_config where id=%s',(idd))
#         conn.commit()
#         conn.close()
#     except :
#         return jsonify({'msg': "fail", "remark": "删除数据失败"})
#     return jsonify({'msg': "ok","remark":""})
#
# @testcases_api.route('/editinfo',methods=['POST'])
# def editinfo():
#     parser = reqparse.RequestParser()
#     parser.add_argument('title', type=str, required=True)
#     parser.add_argument('method', type=str, required=True)
#     parser.add_argument('reqparams', type=str, required=True)
#     parser.add_argument('resparams', type=str, required=True)
#     parser.add_argument('des', type=str)
#     parser.add_argument('domain', type=str, required=True)
#     parser.add_argument('id', type=int, required=True)
#     parser.add_argument('projectName', type=str, required=True)
#     parser.add_argument('ischeck', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     try:
#         conn = pymysql.connect(**config)
#         cur = conn.cursor()
#         print('update mock_config set title=%s,reqparams=%s,methods=%s,domain=%s,description=%s,resparams=%s,update_time=%s ,project_name=%s ,ischeck=%s'
#                     ' where id=%s',(args.get('title'),args.get('reqparams'),args.get('method'),args.get('domain'), args.get('des'), args.get('resparams'),
#                                    datetime.now().strftime('%y-%m-%d %H:%M:%S'),args.get('projectName'),args.get('ischeck'),args.get('id')))
#
#         cur.execute('update mock_config set title=%s,reqparams=%s,methods=%s,domain=%s,description=%s,resparams=%s,update_time=%s ,project_name=%s ,ischeck=%s'
#                     ' where id=%s',(args.get('title'),args.get('reqparams'),args.get('method'),args.get('domain'), args.get('des'), args.get('resparams'),
#                                    datetime.now().strftime('%y-%m-%d %H:%M:%S'),args.get('projectName'),args.get('ischeck'),args.get('id')))
#         conn.commit()
#         conn.close()
#     except:
#         return jsonify({'msg': "fail", "remark": "编辑数据失败"})
#     return jsonify({'msg': "ok", "remark": ""})
#
# @testcases_api.route('/selectinfo',methods=['GET'])
# def selectinfo():
#     parser = reqparse.RequestParser()
#     parser.add_argument('id', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute('select title,reqparams,methods,domain,description,resparams,project_name,ischeck from mock_config where id=%s',(args.get('id')))
#         re= cur.fetchall()
#         conn.close()
#         key = ('title', 'reqparams', 'methods', 'domain', 'description', 'resparams','project_name','ischeck')
#         d = [dict(zip(key, value)) for value in re]
#     except:
#         return jsonify({'msg': "fail", "remark": "查询信息失败"})
#     return jsonify({'msg': "ok", "remark": "", 'data':d})
#
# @testcases_api.route('/manage',methods=['POST'])
# def manage():
#     parser = reqparse.RequestParser()
#     parser.add_argument('id', type=int, required=True)
#     parser.add_argument('status', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute('update mock_config set status=%s where id=%s',(args.get('status'),args.get('id')))
#         conn.commit()
#         conn.close()
#     except:
#         return jsonify({'msg': "fail", "remark": "查询信息失败"})
#     return jsonify({'msg': "ok", "remark": ""})
#
# @testcases_api.route('/search',methods=['GET'])
# def search():
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
#         if args.get('project_name') == str(0):
#             sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s'),project_name from mock_config where title like %s"
#             value=args.get('title').strip()
#             cur.execute(sql, value+'%%')
#         else:
#             sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s'),project_name from mock_config where title like %s and project_name=%s"
#             values = (args.get('title')+'%%' .strip(),args.get('project_name'))
#             cur.execute(sql,values)
#         re= cur.fetchall()
#         conn.close()
#         key = ('id','status','title', 'reqparams', 'methods', 'domain', 'description', 'resparams','updateTime','projectName')
#         d = [dict(zip(key, value)) for value in re]
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#     return jsonify({'msg': "ok", "remark": "", "data": d})
#
#
# @testcases_api.route('/searchall',methods=['GET'])
# def searchall():
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute("select id,title,reqparams,methods,domain,description,resparams,status,date_format(update_time,'%Y-%m-%d %H:%i:%s') from mock_config")
#         re= cur.fetchall()
#         conn.close()
#         key = ('id','title', 'reqparams', 'methods', 'domain', 'description', 'resparams','status','updateTime')
#         d = [dict(zip(key, value)) for value in re]
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#     return jsonify({'msg': "ok", "remark": "","data": d})
#
# @testcases_api.route('/searchproject',methods=['GET'])
# def searchproject():
#     # request.headers.get()
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT DISTINCT(project_name) from mock_config")
#         re= cur.fetchall()
#         conn.close()
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#     return jsonify({'msg': "ok", "remark": "","data": re})
#
# @testcases_api.route('/copy',methods=['POST'])
# def copy():
#     parser = reqparse.RequestParser()
#     parser.add_argument('id', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#     conn = pymysql.connect(**config)
#     cur = conn.cursor()
#     try:
#         cur.execute("insert into mock_config(title,reqparams,methods,domain,description,resparams,update_time,status,project_name,ischeck) "
#                     "select title,reqparams,methods,domain,description,resparams,update_time,status,project_name,ischeck from mock_config where id=%s",args.get('id'))
#         conn.commit()
#         conn.close()
#     except:
#         return jsonify({'msg': "fail", "remark": "select data fail"})
#     return jsonify({'msg': "ok", "remark": ""})