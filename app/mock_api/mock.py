# -*- coding: UTF-8 -*-

import sys

# import importlib
# importlib.reload(sys)

# from imp import reload
# reload(sys)
# sys.setdefaultencoding('utf-8')
# _*_ coding = utf-8 _*_
from  flask import Flask,request,jsonify,make_response,abort,redirect,render_template
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_cors import *
import pymysql,xlrd
from flask_restful import reqparse
from datetime import datetime
from ..models import Mock
from .. import db
from . import mock_api



save_path='/var/www/testcase/logs'
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
app=Flask(__name__)
CORS(app, supports_credentials=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@mock_api.route('/', methods=['GET', 'POST'])
def index():

    # print(request.headers.get('Cookie'))
    # return redirect('http://192.168.10.24/testcase')
    # return redirect('http://192.168.10.24/testcase')

    return render_template('mock.html', form=None, posts=None,
                           show_followed=None, pagination=None)

@mock_api.route('/import_excel', methods=[ 'POST'])
def import_device():
    file = request.files['files[]']
    filename = file.filename
    # 判断文件名是否合规
    if file and allowed_file(filename):
        file.save(save_path+filename)
        excelName = save_path+filename
        bk = xlrd.open_workbook(excelName, encoding_override="utf-8")
        sh = bk.sheets()[0]  # 因为Excel里只有sheet1有数据，如果都有可以使用注释掉的语句
        ncols = sh.ncols#列
        nrows = sh.nrows#行
        # conn = pymysql.connect(**config)
        # cur = conn.cursor()
        for j in range(1,nrows):
            if j+1 == nrows:
                return jsonify({'msg': "ok", "remark": "上传成功"})
            else:
                lvalues = sh.row_values(j+1)
                if lvalues[6]=='是':
                    ischeck = 0
                elif lvalues[6]=='否':
                    ischeck = 1
                else :
                    ischeck = 1
        #         try:
        #             cur.execute('insert into mock_config values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(None,lvalues[0],lvalues[4],lvalues[3],lvalues[2],lvalues[7],lvalues[5],datetime.now(),0,ischeck,lvalues[1]))
        #             conn.commit()
        #         except:
        #             return jsonify({'msg': "fail", "remark": "解析失败"})
        # conn.close()
        return jsonify({'msg': "ok", "remark": "上传成功"})
    else:
        return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})

@mock_api.route('/addinfo',methods=['POST'])
def query_user():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str,required=True)
    parser.add_argument('method', type=str,required=True)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('resparams', type=str, required=True)
    parser.add_argument('des', type=str)
    parser.add_argument('domain', type=str,required=True)
    parser.add_argument('projectName', type=str,required=True)
    parser.add_argument('ischeck', type=int, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})

    try:
        mock_info = Mock(title = args.get('title'),reqparams = args.get('reqparams'),method = args.get('method'),
                   resparams= args.get('resparams'),domain = args.get('domain'),des = args.get('des'),
                    projectName = args.get('projectName'),ischeck = args.get('ischeck'))
        db.session.add(mock_info)
        db.session.commit()
    except :
        return jsonify({'msg': "fail", "remark": "新增数据失败"})
    return jsonify({'msg': "ok","remark":""})

@mock_api.route('/delinfo',methods=['POST'])
def delinfo():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id[]', type=str, required=True,action='append')
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    id=args.get('id[]')

    try:
        for mock_info in Mock.query.filter(Mock.id.in_(id)).all():
            db.session.delete(mock_info)
            db.session.commit()
    except :
        return jsonify({'msg': "fail", "remark": "删除数据失败"})
    return jsonify({'msg': "ok","remark":""})

@mock_api.route('/editinfo',methods=['POST'])
def editinfo():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('method', type=str, required=True)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('resparams', type=str, required=True)
    parser.add_argument('des', type=str)
    parser.add_argument('domain', type=str, required=True)
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('projectName', type=str, required=True)
    parser.add_argument('ischeck', type=int, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        mock_info = Mock.query.filter(Mock.id == args.get('id')).first()
        mock_info.title = args.get('title')
        mock_info.method = args.get('method')
        mock_info.reqparams = args.get('reqparams')
        mock_info.resparams = args.get('methods')
        mock_info.des = args.get('des')
        mock_info.domain = args.get('domain')
        mock_info.projectName = args.get('projectName')
        mock_info.ischeck = args.get('ischeck')
        db.session.add(mock_info)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "编辑数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

# #待优化
# @mock_api.route('/selectinfo',methods=['GET'])
# def selectinfo():
#     parser = reqparse.RequestParser()
#     parser.add_argument('id', type=int, required=True)
#     try:
#         args = parser.parse_args()
#     except:
#         return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
#
#     try:
#         # cur.execute('select title,reqparams,methods,domain,description,resparams,project_name,ischeck from mock_config where id=%s',(args.get('id')))
#         # re= cur.fetchall()
#         # conn.close()
#         key = ('title', 'reqparams', 'methods', 'domain', 'description', 'resparams','project_name','ischeck')
#         # d = [dict(zip(key, value)) for value in re]
#     except:
#         return jsonify({'msg': "fail", "remark": "查询信息失败"})
#     return jsonify({'msg': "ok", "remark": "", 'data':"test"})

@mock_api.route('/manage',methods=['POST'])
def manage():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('status', type=int, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        mock_info = Mock.query.filter(Mock.id == args.get('id')).first()
        mock_info.status = args.get('status')
        db.session.add(mock_info)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "查询信息失败"})
    return jsonify({'msg': "ok", "remark": ""})

@mock_api.route('/search',methods=['GET'])
def search():
    parser = reqparse.RequestParser()

    parser.add_argument('title', type=str)
    parser.add_argument('project_name', type=str, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        title = '%' + args.get('title').strip() + '%'
        mock_inolist = []
        if args.get('project_name') == str(0):  # x项目名称为空
            if args.get('title') != str(0):
                # print(test)
                for mock_info in Mock.query.filter(Mock.title.ilike(title)).all():
                    mock_infodict = {
                        "id": mock_info.id,
                        "title": mock_info.title,
                        "reqparams": mock_info.reqparams,
                        "methods": mock_info.methods,
                        "domain": mock_info.domain,
                        "description": mock_info.description,
                        "update_time": mock_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "status": mock_info.status,
                        "ischeck": mock_info.ischeck,
                        "project_name": mock_info.project_name,
                        "resparams": mock_info.resparams
                    }
                    mock_inolist.append(mock_infodict)
        elif args.get('title') != str(''):  # title不为空
            for mock_info in Mock.query.filter(Mock.title.ilike(title)).filter(
                            Mock.project_name == args.get('project_name')).all():
                mock_infodict = {
                    "id": mock_info.id,
                    "title": mock_info.title,
                    "reqparams": mock_info.reqparams,
                    "methods": mock_info.methods,
                    "domain": mock_info.domain,
                    "description": mock_info.description,
                    "update_time": mock_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": mock_info.status,
                    "ischeck": mock_info.ischeck,
                    "project_name": mock_info.project_name,
                    "resparams": mock_info.resparams
                }
                mock_inolist.append(mock_infodict)
        else:  # 项目不为空，title为空
            for mock_info in Mock.query.filter(Mock.project_name == args.get('project_name')).all():
                mock_infodict = {
                    "id": mock_info.id,
                    "title": mock_info.title,
                    "reqparams": mock_info.reqparams,
                    "methods": mock_info.methods,
                    "domain": mock_info.domain,
                    "description": mock_info.description,
                    "update_time": mock_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": mock_info.status,
                    "ischeck": mock_info.ischeck,
                    "project_name": mock_info.project_name,
                    "resparams": mock_info.resparams
                }
                mock_inolist.append(mock_infodict)
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "", "data":mock_inolist })


@mock_api.route('/searchall',methods=['GET'])
def searchall():

    try:
        mock_infolist = []
        Mock.query.all()
        mock_infos = Mock.query.order_by(Mock.id.desc())  # id倒叙排列
        for mock_info in mock_infos:
            mock_infodict = {
                "id": mock_info.id,
                "title": mock_info.title,
                "reqparams": mock_info.reqparams,
                "methods": mock_info.methods,
                "domain": mock_info.domain,
                "description": mock_info.description,
                "resparams": mock_info.resparams,
                "status": mock_info.status,
                "update_time": mock_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                "project_name": mock_info.project_name,
                "ischeck": mock_info.ischeck
            }
            mock_infolist.append(mock_infodict)
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": mock_infolist})

@mock_api.route('/searchproject',methods=['GET'])
def searchproject():
    try:
        mock_infolist = []
        for mock_info in db.session.query(Mock.project_name).distinct():
            # print(mock_info.projectName)
            mock_infolist.append(mock_info.project_name)
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": mock_infolist})

@mock_api.route('/copy',methods=['POST'])
def copy():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})

    try:
        mock_info = Mock.query.filter(Mock.id == id).first()
        copytestcase = Mock(title=mock_info.title, reqparams=mock_info.reqparams, methods=mock_info.methods,
                            domain=mock_info.domain, description=mock_info.description,resparams = mock_info.resparams,
                            status=mock_info.status, projectName=mock_info.projectName, ischeck=mock_info.ischeck)
        db.session.add(copytestcase)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": ""})