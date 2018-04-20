#!/usr/bin/env python

# _*_ coding = utf-8 _*_
from  flask import Flask,request,jsonify,make_response,abort,redirect,render_template
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_cors import *
import pymysql,xlrd
from flask_restful import reqparse
from datetime import datetime
import configparser
from . import testcases_api
from .Main import main
import json

from .. import db
from ..models import Mock,TestLogs,TestCases


save_path='/var/www/testcase/logs'
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
app=Flask(__name__)
CORS(app, supports_credentials=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@testcases_api.route('/', methods=['GET', 'POST'])
def index():

    # print(request.headers.get('Cookie'))
    # return redirect('http://192.168.10.24/testcase')
    # return redirect('http://192.168.10.24/testcase')

    return render_template('test.html', form=None, posts=None,
                           show_followed=None, pagination=None)


@testcases_api.route('/all.html', methods=['GET'])
def allhtmnl():

    # print(request.headers.get('Cookie'))
    # return redirect('http://192.168.10.24/testcase')
    # return redirect('http://192.168.10.24/testcase')

    return render_template('all.html', form=None, posts=None,
                           show_followed=None, pagination=None)

#inport excel
@testcases_api.route('/importCaseExcel', methods=[ 'POST'])
# @login_required
def importcaseexcel():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
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
                # try:
                #     cur.execute('insert into mock_config values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(None,lvalues[0],lvalues[4],lvalues[3],lvalues[2],lvalues[7],lvalues[5],datetime.now(),0,ischeck,lvalues[1]))
                #     conn.commit()
                # except:
                #     return jsonify({'msg': "fail", "remark": "解析失败"})
        # conn.close()
        return jsonify({'msg': "ok", "remark": "上传成功"})
    else:
        return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})

@testcases_api.route('/searchCase', methods=['GET'])
def searchCase():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('project_name', type=str, required=True)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        title = '%' +args.get('title').strip() +'%'
        caselist=[]
        if args.get('project_name') == str(0):   #x项目名称为空
            if args.get('title')!=str(0):
                # print(test)
                for testcase in TestCases.query.filter(TestCases.title.ilike(title)).all():
                    casedict = {
                        "id": testcase.id,
                        "title": testcase.title,
                        "reqparams": testcase.reqparams,
                        "env": testcase.env,
                        "methods": testcase.methods,
                        "domain": testcase.domain,
                        "description": testcase.description,
                        "update_time": testcase.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "status": testcase.status,
                        "projectName": testcase.projectName,
                        "checkpoint": testcase.checkpoint,
                        "correlation": testcase.correlation
                    }
                    caselist.append(casedict)
        elif args.get('title')!=str('') :   #title不为空
            for testcase in TestCases.query.filter(TestCases.title.ilike(title)).filter(TestCases.projectName==args.get('project_name')).all():
                casedict = {
                    "id": testcase.id,
                    "title": testcase.title,
                    "reqparams": testcase.reqparams,
                    "env": testcase.env,
                    "methods": testcase.methods,
                    "domain": testcase.domain,
                    "description": testcase.description,
                    "update_time": testcase.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": testcase.status,
                    "projectName": testcase.projectName,
                    "checkpoint": testcase.checkpoint,
                    "correlation": testcase.correlation
                }
                caselist.append(casedict)
        else:    #项目不为空，title为空
            for testcase in TestCases.query.filter(TestCases.projectName==args.get('project_name')).all():
                casedict = {
                    "id": testcase.id,
                    "title": testcase.title,
                    "reqparams": testcase.reqparams,
                    "env": testcase.env,
                    "methods": testcase.methods,
                    "domain": testcase.domain,
                    "description": testcase.description,
                    "update_time": testcase.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": testcase.status,
                    "projectName": testcase.projectName,
                    "checkpoint": testcase.checkpoint,
                    "correlation": testcase.correlation
                }
                caselist.append(casedict)
    except Exception as e:
        print(e)
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "", "data": caselist})

# 修改状态
@testcases_api.route('/manageCase',methods=['POST'])
# @login_required
def managecase():
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
        testcase = TestCases.query.filter(TestCases.id == args.get('id')).first()
        testcase.status = args.get('status')
        db.session.add(testcase)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "查询信息失败"})
    return jsonify({'msg': "ok", "remark": ""})

#添加测试用例
@testcases_api.route('/addTestCase',methods=['POST'])
# @login_required
def addtestcase():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('env', type=str, required=True)
    parser.add_argument('methods', type=str, required=True)
    parser.add_argument('domain', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('projectName', type=str, required=False)
    parser.add_argument('checkpoint', type=str, required=True)
    parser.add_argument('correlation', type=str, required=False)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        testcase = TestCases(title = args.get('title'),reqparams = args.get('reqparams'),env = args.get('env'),
                    methods = args.get('methods'),domain = args.get('domain'),description = args.get('description'),
                    update_time = datetime.now().strftime('%y-%m-%d %H:%M:%S'),projectName = args.get('projectName'),
                    checkpoint = args.get('checkpoint'),correlation = args.get('correlation'))
        db.session.add(testcase)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": ""})


# 编辑测试用例
@testcases_api.route('/editTestCase',methods=['POST'])
# @login_required
def edittestcase():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True)
    parser.add_argument('title', type=str)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('env', type=str, required=True)
    parser.add_argument('methods', type=str, required=True)
    parser.add_argument('domain', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('projectName', type=str, required=False)
    parser.add_argument('checkpoint', type=str, required=True)
    parser.add_argument('correlation', type=str, required=False)
    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    try:
        testcase = TestCases.query.filter(TestCases.id == args.get('id')).first()
        testcase.title = args.get('title')
        testcase.reqparams = args.get('reqparams')
        testcase.env = args.get('env')
        testcase.methods = args.get('methods')
        testcase.domain = args.get('domain')
        testcase.description = args.get('description')
        testcase.update_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        testcase.projectName = args.get('projectName')
        testcase.checkpoint = args.get('checkpoint')
        testcase.correlation = args.get('correlation')
        db.session.add(testcase)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "编辑数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

#删除测试用例
@testcases_api.route('/delCase',methods=['POST'])
# @login_required
def delcase():
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
        for testcase in TestCases.query.filter(TestCases.id.in_(id)).all():
            db.session.delete(testcase)
            db.session.commit()
    except :
        return jsonify({'msg': "fail", "remark": "删除数据失败"})
    return jsonify({'msg': "ok","remark":""})



#测试用例集合
@testcases_api.route('/searchAllCase',methods=['GET'])
def searchAllCase():
    try:
        caselist = []
        TestCases.query.all()
        testcases = TestCases.query.order_by(TestCases.id.desc())  # id倒叙排列
        for testcase in testcases:
            casedict = {
                "id": testcase.id,
                "title": testcase.title,
                "reqparams": testcase.reqparams,
                "env": testcase.env,
                "methods": testcase.methods,
                "domain": testcase.domain,
                "description": testcase.description,
                "update_time": testcase.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": testcase.status,
                "projectName": testcase.projectName,
                "checkpoint": testcase.checkpoint,
                "correlation": testcase.correlation
            }
            caselist.append(casedict)
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": caselist})

# 项目列表，去重
@testcases_api.route('/searchCaseProject',methods=['GET'])
def searchcaseproject():
    # request.headers.get()
    try:
        projectlist=[]
        for testcase in db.session.query(TestCases.projectName).distinct():
            print(testcase.projectName)
            projectlist.append(testcase.projectName)
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "", "data": projectlist})

#copy测试用例
@testcases_api.route('/copyCase',methods=['POST'])
# @login_required
def copyCase():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)

    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    id = args.get('id')
    try:
        testcase = TestCases.query.filter(TestCases.id==id).first()
        copytestcase = TestCases(title=testcase.title,reqparams=testcase.reqparams,env=testcase.env,methods=testcase.methods,domain=testcase.domain,description=testcase.description,status=testcase.status,
                                 projectName=testcase.projectName,checkpoint=testcase.checkpoint,correlation=testcase.correlation)
        db.session.add(copytestcase)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": ""})

#运行测试用例
@testcases_api.route('/runCase',methods=['POST','GET'])
def runCase():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})
    parser = reqparse.RequestParser()
    parser.add_argument('id[]', type=str, required=True, action='append')

    try:
        args = parser.parse_args()
    except:
        return jsonify({'msg':'fail',"message":"参数解析错误，请检查参数是否正确"})
    id = args.get('id[]')
    try:
        caselsit = []
        for testcase in TestCases.query.filter(TestCases.id.in_(id)).all():
            print(testcase.id,testcase.env,testcase.reqparams)
            testcasedic = {
                "id" : testcase.id,
                "title" : testcase.title,
                "reqparams": testcase.reqparams,
                "env": testcase.env,
                "methods": testcase.methods,
                "domain": testcase.domain,
                "description": testcase.description,
                "update_time": testcase.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": testcase.status,
                "projectName": testcase.projectName,
                "checkpoint": testcase.checkpoint,
                "correlation": testcase.correlation
            }
            caselsit.append(testcasedic)
        # result = db.session.query(TestCases).all()
        # results = db.session.query(TestCases).filter_by(status=0)
        # results = TestCases.query.filter(TestCases.env.ilike('%app%').all())
        # results = TestCases.query.filter(id in [69,70,71]).first()
        # results = TestCases.query.filter(TestCases.title.in_(db.session.query(TestCases.env=='http://app.zhhqice.com.cn'))).paginate()
        # logs = TestLogs.query.all()

        if caselsit:
            starttime, endtime, filename,result = main(caselsit)
            resulturl = 'http://192.168.0.24/testcase/results/result_'+ filename + '.html'
            logpath = '/var/www/testcase/logs/'
            # logpath = u'E:\git\local\mock\interfacetest\\results\\result'

            testlog = TestLogs(starttime=starttime,endtime=endtime,logname=filename,logpath=logpath,url=resulturl,result=result)
            db.session.add(testlog)
            db.session.commit()
            # conn = pymysql.connect(**config)
            # cur = conn.cursor()
            # cur.execute(
            #     'insert into testlogs (starttime,endtime,logname,logpath,url,result) values (%s,%s,%s,%s,%s,%s) ',
            #     (starttime,endtime,filename,logpath ,resulturl,result))
            # conn.commit()
            # conn.close()


    except Exception as e:
        print(e)
        return jsonify({'msg': "fail", "remark": "服务器出现异常"  })
    return jsonify({'msg': "ok", "remark": "", "resultUrl": resulturl})


#运行所有测试用例
@testcases_api.route('/runAllCase',methods=['POST','GET'])
# @login_required
def runallcase():
    if not current_user.is_authenticated:
        return jsonify({'msg':'fail',"remark":"请先登录"})

    try:
        # results = TestCases.query.filter_by(status=0).all()
        # results = Mock.query.filter_by(status=0).first()
        # results = db.session.query(TestCases).filter_by(status=0)
        results = db.session.query(TestCases).filter_by(status=0).all()
        list = []
        for result in results:
            dic = {
                "id" : result.id,
                "title" : result.title,
                "reqparams": result.reqparams,
                "env": result.env,
                "methods": result.methods,
                "domain": result.domain,
                "description": result.description,
                "update_time": result.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": result.status,
                "projectName": result.projectName,
                "checkpoint": result.checkpoint,
                "correlation": result.correlation
            }
            list.append(dic)
        if list:
            starttime, endtime, filename,result = main(list)
            resulturl = 'http://192.168.0.24/testcase/results/result_'+ filename + '.html'
            # logpath = u'E:\git\local\mock'
            logpath = '/var/www/testcase/logs/'
            testlog = TestLogs(starttime,endtime,filename,logpath,resulturl,result)
            db.session.add(testlog)
            db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({'msg': "fail", "remark": "服务器出现异常" })
    return jsonify({'msg': "ok", "remark": "", "resultUrl": resulturl})


# 测试结果
@testcases_api.route('/result',methods=['GET'])
def result():
    try:
        logs = TestLogs.query.order_by(TestLogs.id.desc())     #id倒叙排列
        # key = ('id', 'starttime', 'endtime', 'url', 'result')
        list = []
        for log in logs:
            # dic ={}
            # dic["id"] = log.id
            # dic["starttime"] = log.starttime.strftime('%Y-%m-%d %H:%M:%S')
            # dic["endtime"] = log.endtime.strftime('%Y-%m-%d %H:%M:%S')
            # dic["url"] = log.url
            # dic["result"] = log.result
            dic = {
                "id" : log.id,
                "starttime" : log.starttime.strftime('%Y-%m-%d %H:%M:%S'),
                "endtime": log.endtime.strftime('%Y-%m-%d %H:%M:%S'),
                "url": log.url,
                "result": log.result
            }
            list.append(dic)
            # print(log.id)
            # returnlog = (log.id,log.starttime,log.endtime,log.url,log.result)
            # d = [dict(zip(key, value))for key,value in returnlog]
        # d = [dict(zip(key, value)) for value in logs]
        # return jsonify({'msg': "ok", "remark": "", "data": d})
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})

    # 处理日期时间字段
    # for data in d:
    #     print("starttime:%s", data['starttime'])
    #     data['starttime'] = data['starttime'].strftime('%Y-%m-%d %H:%M:%S')
    #     data['endtime'] = data['endtime'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'msg': "ok", "remark": "","data": list})


@testcases_api.route('/test',methods=['GET'])
def result1():
    print('start test')
    mock = Mock.query.filter_by(title='test').first()
    print(mock.reqparams)

    return jsonify({'msg': "ok", "reqparams": mock.reqparams})
    # return jsonify({'msg': "ok", "remark": "","data": d})


@testcases_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@testcases_api.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True,port=5202)
