from  flask import Flask,request,jsonify,make_response,abort,redirect,render_template,request,url_for
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.utils import secure_filename

from app import log,autotestconfig
from app.core import hubs
from app.db import test_case_manage,test_batch_manage,test_suite_manage,test_keyword_manage,test_unittest_manage
import pyecharts

from . import uiautotest
import requests
import logging
import os
import configparser
import subprocess
import json

logging.basicConfig(filename='monitor.log',format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger('manage')

@uiautotest.route('/test_suites', methods=['GET','POST'])
def test_suite():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("uitest/test_suite.html")


@uiautotest.route('/test_cases')
def test_cases():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("uitest/test_cases.html")

        # return jsonify({'msg':'fail',"remark":"请先登录"})
    # return render_template("uitest/test_cases.html")

@uiautotest.route('/add_test_case', methods=['POST', 'GET'])
def save_new_test_case():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:

        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            return render_template("uitest/new_test_cases.html")
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            name =  getInfoAttribute(info,'name')
            module =  getInfoAttribute(info,'module')
            description =  getInfoAttribute(info,'description')
            steps =  getInfoAttribute(info,'steps')
            log.log().logger.info("steps: %s" %steps)
            steps=steps.replace('"',"'")
            log.log().logger.info("steps: %s" %steps)
            type =  getInfoAttribute(info,'type')
            if module == '' or name == '' or steps=='' or type=='':
                return '必填字段不得为空！'
            else:
                if type=='公共用例':
                    isPublic = 1
                else:
                    isPublic = 0
                test_case_manage.test_case_manage().new_test_case(module, name, steps, description, isPublic)
            # return render_template("test_cases.html")
            return redirect('/autotest/test_cases')

@uiautotest.route('/edit_test_case', methods=['POST', 'GET'])
def edit_test_case():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s'%id)
            return render_template("uitest/edit_test_cases2.html", id=id)
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            name =  getInfoAttribute(info,'name')
            module =  getInfoAttribute(info,'module')
            description =  getInfoAttribute(info,'description')
            steps =  getInfoAttribute(info,'steps')
            log.log().logger.info("steps: %s" %steps)
            steps=steps.replace('"',"'")
            log.log().logger.info("steps: %s" %steps)
            type =  getInfoAttribute(info,'type')
            if module == '' or name == '' or steps=='' or type=='':
                return '必填字段不得为空！'
            else:
                if type=='公共用例':
                    isPublic = 1
                else:
                    isPublic = 0
                test_case_manage.test_case_manage().update_test_case(id, ['module', 'name', 'steps', 'description', 'isPublicFunction'], [module, name, steps, description, isPublic])
                return render_template("uitest/test_batch2.html",id=id,type='test_suite')

@uiautotest.route('/copy_test_case', methods=['POST', 'GET'])
def copy_test_case():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        log.log().logger.info(request.method)
        # log.log().logger.info(request.value)
        if request.method == 'GET':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info(id)
            if id=='':
                result = jsonify({'code': 500, 'msg': 'test case is not found!'})
            else:
                result0 = test_case_manage.test_case_manage().copy_test_case(id)
                if result0:
                    result = jsonify({'code': 200, 'msg': 'copy success!'})
                else:
                    result = jsonify({'code': 500, 'msg': 'test case is not found!'})
            return result

@uiautotest.route('/copy_test_suite', methods=['POST', 'GET'])
def copy_test_suite():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        log.log().logger.info(request.method)
        # log.log().logger.info(request.value)
        if request.method == 'GET':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info("id: %s" %id)
            if id=='':
                result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
            else:
                import random, time
                batchId = str(random.randint(10000, 99999)) + str(time.time())
                test_suite_manage.test_suite_manage().copy_test_suite(id, batchId)
                newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
                log.log().logger.info('newid %s' %newId)
                if len(newId):
                    ext = newId[0]['id']
                    log.log().logger.info('ext is: %s, id is: %s' %(ext, id))
                    if ext !='0':
                        test_batch_manage.test_batch_manage().copy_test_batch(ext, id)
                    message = 'success！'
                    code = 200
                    result = jsonify({'code': 200, 'msg': 'copy success!'})
                else:
                    result = jsonify({'code': 500, 'msg': 'test suite is not found!'})
            return result

@uiautotest.route('/delete_test_case', methods=['POST', 'GET'])
def delete_test_case():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/test_cases.html")
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            act =  getInfoAttribute(info, 'act')
            if act == 'del':
                test_case_manage.test_case_manage().update_test_case(id, ['status'], [0])
                code = 200
                message = 'delete success!'
            else:
                code=500
                message = 'act is not del!'
            result = jsonify({'code': code, 'msg': message})
            return result,{'Content-Type': 'application/json'}

@uiautotest.route('/test_case.json', methods=['POST', 'GET'])
def search_test_cases():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' %info)
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            log.log().logger.info('get %s' %limit)
            log.log().logger.info('get  offset %s' %offset)
            id =  getInfoAttribute(info,'id')
            module =  getInfoAttribute(info, 'module')
            type =  getInfoAttribute(info, 'type')
            log.log().logger.info('module: %s' %module)
            module = module.split(',')
            log.log().logger.info(module)
            name =  getInfoAttribute(info, 'name')
            conditionList = ['name']
            valueList = [name]
            if type == 'unattach' and 'public' in module:
                module.remove('public')
            elif type!='test_case':
                if len(module) !=0 and module[0] != 'All' and module[0] != '':
                    conditionList.append('module')
                    valueList.append(module)
                log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module, name, type))
            else:
                conditionList = ['id']
                valueList = [id]
                log.log().logger.info('info content: id- %s, module - %s, name - %s, type - %s' %(id,module,name, type))
            # else:
            fieldlist = []
            rows = 1000
            if type =='unattach':
                caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
            else:
                caseList = test_case_manage.test_case_manage().show_test_cases(conditionList, valueList, fieldlist, rows)
            log.log().logger.info(caseList)
            data = caseList
            if type=='test_case':
                data1 = jsonify({'total': len(data), 'rows': data[0]})
            else:
                data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
            log.log().logger.info('data1: %s' %data1)
            return data1,{'Content-Type': 'application/json'}


@uiautotest.route('/test_suite.json', methods=['POST', 'GET'])
def search_test_suite():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' %info)
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            log.log().logger.info('get %s' %limit)
            log.log().logger.info('get  offset %s' %offset)
            id =  getInfoAttribute(info,'id')
            type =  getInfoAttribute(info, 'type')
            log.log().logger.info('type %s' %type)
            run_type =  getInfoAttribute(info, 'run_type')
            status =  getInfoAttribute(info, 'status')
            name =  getInfoAttribute(info, 'name')
            if id =='':
                if status == 'All':
                    status = ''
                log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
                conditionList = ['status','run_type','name']
                valueList = [status,run_type,name]
            else:
                if type == 'testview':
                    statusList = test_batch_manage.test_batch_manage().show_test_batch_status(id)
                else:
                    statusList = []
                log.log().logger.info('info content: %s, %s, %s, %s' %(id,status,run_type, name))
                conditionList = ['id']
                valueList = [id]
            fieldlist = []
            rows = 1000
            caseList = test_suite_manage.test_suite_manage().show_test_suites(conditionList, valueList, fieldlist, rows)
            log.log().logger.info(caseList)
            data = caseList
            if id !='':
                data1 = jsonify({'total': len(data), 'rows': data[0],'status':statusList})
            else:
                data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
            log.log().logger.info('data1: %s' %data1)
            return data1,{'Content-Type': 'application/json'}

@uiautotest.route('/add_test_suite.json', methods=['POST', 'GET'])
def save_new_test_suite():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            return render_template("uitest/new_test_suite.html")
        if request.method == 'POST':
            info = request.values
            log.log().logger.info('info :%s' %info)
            name =  getInfoAttribute(info,'name')
            run_type =  getInfoAttribute(info,'run_type')
            description =  getInfoAttribute(info,'description')
            if run_type == '' or name == '' :
                message =  '必填字段不得为空！'
                code = 500
            else:
                import random, time
                batchId = str(random.randint(10000, 99999)) + str(time.time())
                test_suite_manage.test_suite_manage().new_test_suite(name, run_type, description, batchId)
                newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"], [batchId], ['id'], 1)
                log.log().logger.info('newid %s' %newId)
                if len(newId):
                    ext=newId[0]['id']
                    log.log().logger.info('ext %s' %ext)
                    message = 'success！'
                    code = 200
                    # return redirect('attach_test_batch?test_suite_id=%s' %ext)
                else:
                    ext=''
                    message =  'add failed！'
                    code = 500
                result = jsonify({'code': code, 'msg': message,'ext':ext})
                log.log().logger.info(result)
                # log.log().logger.info('code is : %s'%result['code'])
                return result

@uiautotest.route('/add_test_suite', methods=['POST', 'GET'])
def add_test_suite():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        return render_template("uitest/new_test_suite.html")


@uiautotest.route('/test_batch.json', methods=['POST', 'GET'])
def search_test_batch():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' %info)
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            log.log().logger.info('get %s' %limit)
            log.log().logger.info('get  offset %s' %offset)
            id =  getInfoAttribute(info,'id')
            name =  getInfoAttribute(info, 'name')
            status =  getInfoAttribute(info, 'status')
            module =  getInfoAttribute(info, 'module')
            ipVal =  getInfoAttribute(info, 'ipVal')
            browser_type =  getInfoAttribute(info, 'browser_type')
            type =  getInfoAttribute(info, 'type')
            log.log().logger.info('module: %s' %module)
            log.log().logger.info('ipVal %s' %ipVal)
            module = module.split(',')
            log.log().logger.info(module)
            valueList = []
            conditionList = []
            if id == '':
                data1 = jsonify({'total': 0, 'rows': []})
            else:
                if name != '':
                    conditionList.append('name')
                    valueList.append(name)
                if status != '':
                    conditionList.append('status')
                    valueList.append(status)
                if len(module) !=0 and module[0] != 'All' and module[0] != '':
                    conditionList.append('module')
                    valueList.append(module)
                ipList = ipVal.split(',')
                for j in range(len(ipList)):
                    if ipList[j] !='':
                        conditionList.append('ip')
                        valueList.append(ipList[j])
                fieldlist = []
                rows = 1000
                if type == "" or type=='test_suite':
                    conditionList.append('test_suite_id')
                    valueList.append(id)
                    caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
                    log.log().logger.info("caseList %s" %caseList)
                    data = caseList
                elif type=='test_case':
                    conditionList.append('test_case_id')
                    valueList.append(id)
                    caseList = test_batch_manage.test_batch_manage().show_test_batch(conditionList, valueList, fieldlist, rows)
                    log.log().logger.info(caseList)
                    data = caseList
                else:
                    caseList = test_case_manage.test_case_manage().show_test_cases_unattach(id, conditionList, valueList, fieldlist, rows)
                    log.log().logger.info(caseList)
                    data = caseList
                data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset)+int(limit)]})
                log.log().logger.info('data1: %s' %data1)
            return data1,{'Content-Type': 'application/json'}

@uiautotest.route('/test_batch_detail_old', methods=['POST', 'GET'])
def test_batch_detail():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'test_suite_id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/test_batch_detail.html",id=id)
            # return render_template("uitest/test_batch_report.html", id=id)
        else:
            return render_template('test_suite.html')

@uiautotest.route('/attach_test_batch', methods=['POST', 'GET'])
def attach_test_batch():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'test_suite_id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/attach_test_batch.html",id=id)
        else:
            return render_template("uitest/test_suite.html")

@uiautotest.route('/attach_test_batch.json', methods=['POST', 'GET'])
def attach_test_batch_to_suite():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'post'})
            return result
        else:
            log.log().logger.info(request.values)
            # log.log().logger.info(request.form)
            info = request.values
            test_suite_id = getInfoAttribute(info,'test_suite_id')
            ipVal = getInfoAttribute(info, 'ipVal')
            browser_list =  getInfoAttribute(info, 'browser_list')
            browser_list = browser_list.split(',')
            rows =  getInfoAttribute(info,'datarow')
            log.log().logger.info("ipVal %s" %ipVal)
            log.log().logger.info('%s, %s' %(test_suite_id,rows))
            rows = rows.split(',')
            log.log().logger.info(rows)
            idrows = []
            for i in range(1,len(rows)):
                idrows.append(rows[i])
            log.log().logger.info(idrows)
            ipList = ipVal.split(',')
            for j in range(len(ipList)):
                if ipList[j] == '':
                    result0 = test_batch_manage.test_batch_manage().batch_new_testcase(test_suite_id, idrows,browser_type_list=browser_list)
                else:
                    result0 = test_batch_manage.test_batch_manage().batch_new_testcase_IP(test_suite_id, idrows, ipList[j])
            if result0 == 0:
                result = jsonify({'code': 500, 'msg': 'error, please check selected test cases!'})
            else:
                result = jsonify({'code': 200, 'msg': 'message'})
            return result


@uiautotest.route('/general_test_batch', methods=['POST', 'GET'])
def general_test_batch():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'test_suite_id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/general_test_batch.html",id=id)
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            name =  getInfoAttribute(info,'name')
            run_type =  getInfoAttribute(info,'run_type')
            description =  getInfoAttribute(info,'description')
            if run_type == '' or name == '':
                message =  '必填字段不得为空！'
                code = 500
            else:
                test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
                message = 'success！'
                code = 200
            result = jsonify({'code': code, 'msg': message})
            return render_template("uitest/test_suite.html")

@uiautotest.route('/edit_test_suite', methods=['POST', 'GET'])
def edit_test_suite():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/edit_test_suite.html",id=id)
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            name =  getInfoAttribute(info,'name')
            run_type =  getInfoAttribute(info,'run_type')
            description =  getInfoAttribute(info,'description')
            if run_type == '' or name == '':
                message =  '必填字段不得为空！'
                code = 500
            else:
                test_suite_manage.test_suite_manage().update_test_suite(id, ['name', 'run_type', 'description'], [name, run_type, description])
                message = 'success！'
                code = 200
            result = jsonify({'code': code, 'msg': message})
            return render_template("uitest/test_suite.html")

@uiautotest.route('/delete_test_suite', methods=['POST', 'GET'])
def delete_test_suite():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/test_suite.html")
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            act =  getInfoAttribute(info, 'act')
            if act == 'del':
                test_suite_manage.test_suite_manage().update_test_suite(id, ['isDeleted'], [1])
                code = 200
                message = 'delete success!'
            else:
                code=500
                message = 'act is not del!'
            result = jsonify({'code': code, 'msg': message})
            return result,{'Content-Type': 'application/json'}


@uiautotest.route('/view_test_suite_screenshot', methods=['POST', 'GET'])
def view_test_suite_screenshot():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            test_batch_id =  getInfoAttribute(info, 'test_batch_id')
            type =  getInfoAttribute(info, 'type')
            index =  getInfoAttribute(info, 'index')
            if index=='':
                index = 1
            else:
                index = int(index)+1
            log.log().logger.info('id: %s' %id)
            log.log().logger.info('test_batch_id: %s' %test_batch_id)
            data = test_batch_manage.test_batch_manage().show_test_batch(['id'], [id], ['screenshot'], 1)
            log.log().logger.info(data)
            if data[0]['screenshot'] is None:
                imgUrl0 = []
            elif len(data[0]['screenshot']):
                log.log().logger.info('%s, %s' %(len(data[0]['screenshot']),data[0]['screenshot']))
                imgUrl0 = data[0]['screenshot'].split("'")
            else:
                imgUrl0 = []
            imgUrl = []
            imgTitle=[]
            for i in range(len(imgUrl0)):
                if i>0 and i<len(imgUrl0)-1 and len(imgUrl0[i])>5:
                    imgUrl.append(imgUrl0[i].replace('\\','/'))
                    imgTitle.append(imgUrl0[i])
                    log.log().logger.info('%s, %s, %s '%(imgUrl0[i],len(imgUrl0[i]),i))

            if len(imgUrl)== 0:
                return render_template('uitest/view_test_suite_screenshot.html',imgTitle='no screenshot!', imgCnt =len(imgUrl),id = id,test_batch_id=test_batch_id,type=type )
            else:
                log.log().logger.info(imgUrl)
                index = index % len(imgUrl)
                return render_template('uitest/view_test_suite_screenshot.html', imgUrl =imgUrl[index], index = index, id = id,imgTitle = imgTitle[index],imgCnt =len(imgUrl),test_batch_id=test_batch_id,type=type)



@uiautotest.route('/runtest.json', methods=['POST', 'GET'])
def runtest():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        else:
            log.log().logger.info(request.values)
            # log.log().logger.info(request.form)
            info = request.values
            id =  getInfoAttribute(info,'id')
            test_case_id =  getInfoAttribute(info,'test_case_id')
            ipVal =  getInfoAttribute(info, 'ipVal')
            type =  getInfoAttribute(info,'type')
            if type == 'test_suite':
                test_suite_manage.test_suite_manage().new_test_run_list(id)
                result = jsonify({'code': 200, 'msg': 'success!'})
            elif type =='test_suite_rerun_all':
                ipList = ipVal.split(',')
                for i in range(len(ipList)):
                    test_suite_manage.test_suite_manage().new_test_run_list(id)
                    if ipList[i] == '':
                        test_batch_manage.test_batch_manage().rerun_test_batch(id, 'all')
                    else:
                        test_batch_manage.test_batch_manage().rerun_test_batch_Ip(id, 'all', ipList[i])

                result = jsonify({'code': 200, 'msg': 'success!'})
            elif type =='test_suite_rerun_part':
                test_suite_manage.test_suite_manage().new_test_run_list(id)
                test_batch_manage.test_batch_manage().rerun_test_batch(id, 'part')
                result = jsonify({'code': 200, 'msg': 'success!'})
            elif type =='test_batch':
                # test_suite_manage.test_suite_manage().new_test_run_list(id)
                test_batch_manage.test_batch_manage().rerun_test_batch_record(id,test_case_id)
                result = jsonify({'code': 200, 'msg': 'success!'})
            elif type == 'test_case':
                ipList = ipVal.split(',')
                for i in range(len(ipList)):
                    if ipList[i] == '':
                        test_batch_manage.test_batch_manage().batch_new_testcase('0', [id])
                    else:
                        test_batch_manage.test_batch_manage().batch_new_testcase_IP('0', [id], str(ipList[i]))
                result = jsonify({'code': 200, 'msg': 'success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'type is not defined!'})
            return result



@uiautotest.route('/test_case_runhistory', methods=['POST', 'GET'])
def test_case_runhistory():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            if len(test_case_manage.test_case_manage().show_test_cases(['id'], [id], [], 2))==1:
                return render_template("uitest/test_batch2.html",id=id,type='test_case',test_suite_id='')
            else:
                return render_template("uitest/test_cases.html")
        else:
            return render_template("uitest/test_cases.html")

@uiautotest.route('/runall')
def runall():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        import os
        os.system('/opt/flask/flask/runall.sh')
        return render_template("index.html")

@uiautotest.route('/testkeywords')
def testkeywords():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("uitest/test_keywords.html")


@uiautotest.route('/test_keywords.json', methods=['POST', 'GET'])
def test_keywords():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' %info)
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            log.log().logger.info('get %s' %limit)
            log.log().logger.info('get  offset %s' %offset)
            id =  getInfoAttribute(info, 'id')
            keyword =  getInfoAttribute(info, 'keyword')
            if id=='':
                conditionList = ['keyword']
                valueList = [keyword]
            else:
                conditionList = ['id']
                valueList = [id]
            fieldlist = []
            rows = 1000
            caseList = test_keyword_manage.test_keyword_manage().show_test_keywords(conditionList, valueList, fieldlist, rows)
            log.log().logger.info(caseList)
            data = caseList
            data1 = jsonify({'total': len(data), 'rows': data})
            log.log().logger.info('data1: %s' %data1)
            return data1,{'Content-Type': 'application/json'}


@uiautotest.route('/add_test_keyword', methods=['POST', 'GET'])
def new_test_keyword():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("uitest/new_test_keyword.html")


@uiautotest.route('/add_test_keyword.json', methods=['POST', 'GET'])
def save_new_test_keyword():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        info = request.form
        log.log().logger.info('info : %s' %info)
        name =  getInfoAttribute(info,'name')
        paraCount =  getInfoAttribute(info,'paraCount')
        description =  getInfoAttribute(info,'description')
        template =  getInfoAttribute(info,'template')
        example =  getInfoAttribute(info, 'example')
        result0 = test_keyword_manage.test_keyword_manage().new_test_keyword(name, paraCount, description, template,example)
        return redirect('/autotest/testkeywords')

@uiautotest.route('/edit_test_keyword', methods=['POST', 'GET'])
def edit_test_keyword():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s'%id)
            return render_template("uitest/edit_test_keyword.html",id=id)
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            print(info)
            id =  getInfoAttribute(info, 'id')
            name =  getInfoAttribute(info,'name')
            paraCount =  getInfoAttribute(info,'paraCount')
            description =  getInfoAttribute(info,'description')
            template =  getInfoAttribute(info,'template')
            example =  getInfoAttribute(info, 'example')
            result = test_keyword_manage.test_keyword_manage().update_test_keyword(id,["keyword", "paraCount", "description", "template","example"],[name, paraCount, description, template,example])
            return redirect('/autotest/testkeywords')

@uiautotest.route('/copy_test_keyword', methods=['POST', 'GET'])
def copy_test_keyword():
    log.log().logger.info(request)
    log.log().logger.info(request.method)
    # log.log().logger.info(request.value)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info(id)
            if id=='':
                result = jsonify({'code': 500, 'msg': 'test keyword is not found!'})
            else:
                result0 = test_keyword_manage.test_keyword_manage().copy_test_keyword(id)
                if result0:
                    result = jsonify({'code': 200, 'msg': 'copy success!'})
                else:
                    result = jsonify({'code': 500, 'msg': 'test keyword is not found!'})
            return result,{'Content-Type': 'application/json'}

@uiautotest.route('/delete_test_keyword', methods=['POST', 'GET'])
def delete_test_keyword():
    log.log().logger.info(request)
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            return render_template("uitest/test_cases.html")
        if request.method == 'POST':
            info = request.form
            log.log().logger.info('info : %s' %info)
            id =  getInfoAttribute(info, 'id')
            act =  getInfoAttribute(info, 'act')
            if act == 'del':
                test_keyword_manage.test_keyword_manage().update_test_keyword(id, ['status'], [0])
                code = 200
                message = 'delete success!'
            else:
                code=500
                message = 'act is not del!'
            result = jsonify({'code': code, 'msg': message})
            return result,{'Content-Type': 'application/json'}

@uiautotest.route('/test_batch_runhistory_report', methods=['POST', 'GET'])
def test_case_runhistory_report2():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        REMOTE_HOST = "https://pyecharts.github.io/assets/js"
        bar = pyecharts.Pie()
        bar.add("Sports", ["Football", "Basketball", "Baseball", "Tennis", "Swimming"], [23, 34, 45, 56, 67],
                is_more_utils=True)

        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'id')
            log.log().logger.info('id: %s' %id)
            if len(test_case_manage.test_case_manage().show_test_cases(['id'], [id], [], 2))==1:
                return render_template("uitest/test_batch_result.html",id=id,type='test_case',test_suite_id='',
                                       myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
            else:
                return render_template("uitest/test_cases.html")
        else:
            return render_template("uitest/test_cases.html")


@uiautotest.route('/test_batch_detail', methods=['POST', 'GET'])
def test_batch_detail_report():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        REMOTE_HOST = "https://pyecharts.github.io/assets/js"
        bar = pyecharts.Pie()
        bar.width=700
        bar.height=400
        log.log().logger.info(request)
        if request.method == 'GET':
            log.log().logger.info('post')
            info = request.values
            log.log().logger.info('info :  %s' %info)
            id =  getInfoAttribute(info, 'test_suite_id')
            log.log().logger.info('id: %s' %id)
            statusList = test_batch_manage.test_batch_manage().show_test_batch_status(id)
            nameList , valueList = bar.cast(statusList)
            bar.add("results", ['失败','待执行','执行中','成功'], valueList[0:4],
                    is_more_utils=True,is_area_show=True,is_label_show=True,legend_pos="50%")
            return render_template("uitest/test_batch_detail_report.html",id=id,
                                       myechart=bar.render_embed(),host=REMOTE_HOST,script_list=bar.get_js_dependencies())
            # return render_template("uitest/test_batch_report.html", id=id)
        else:
            return render_template('test_suite.html')


@uiautotest.route('/test_public_test_cases.json', methods=['POST', 'GET'])
def test_public_test_cases():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' % info)

            conditionList = ['id']
            valueList = [id]
            fieldlist = []
            rows = 1000
            caseList = test_case_manage.test_case_manage().show_test_public_cases()
            log.log().logger.info(caseList)
            data = caseList
            data1 = jsonify({'total': len(data), 'rows': data})
            log.log().logger.info('data1: %s' % data1)
            return data1, {'Content-Type': 'application/json'}


@uiautotest.route('/test_keywords_options.json', methods=['POST', 'GET'])
def test_keywords_options():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
        if request.method == 'GET':
            info = request.values
            log.log().logger.info('info : %s' % info)

            conditionList = ['id']
            valueList = [id]
            fieldlist = []
            rows = 1000
            caseList = test_keyword_manage.test_keyword_manage().show_test_keywords_options()
            log.log().logger.info(caseList)
            data = caseList
            data1 = jsonify({'total': len(data), 'rows': data})
            log.log().logger.info('data1: %s' % data1)
            return data1, {'Content-Type': 'application/json'}







# ###########################
#####
#####utils



#############################


#单元测试列表
@uiautotest.route('/unittest_record.json', methods=['POST', 'GET'])
def test_unittest_result():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        else:
            info = request.values
            log.log().logger.info('info :  %s' %info)
            name = getInfoAttribute(info, 'name')
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name], [], 100)
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
            log.log().logger.info('data1: %s' %data1)
            return data1, {'Content-Type': 'application/json'}

# 单元测试详情
@uiautotest.route('/unittest')
def unittest_records():
    return render_template("util/unittest_records.html")

#新增电量统计html，嵌入当前页面中
@uiautotest.route('/power')
def power():
    return render_template("util/power.html")

#新增文件共享
@uiautotest.route('/fileshare')
def fileshare():

    return render_template("util/fileshare.html")

#新增上传apk到蒲公英
@uiautotest.route('/uploadapk',methods=[ 'GET', 'POST'])
def uploadapk():

    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(os.getcwd(), 'app/log',
        secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        #保存成功，开始调用蒲公英api上传app
        config_path = os.path.join(os.getcwd(), 'config.ini')
        # 读取数据库配置文件
        config = configparser.ConfigParser()
        config.read(config_path)

        apikey = str(config.get('path', 'api_key'))

        cmd="curl -F 'file=@" + upload_path + "' " + "-F '_api_key=" + apikey + "' https://www.pgyer.com/apiv2/app/upload"
        print(cmd)
        output = subprocess.getoutput(cmd)
        print(output)
        return render_template("util/uploadapk.html")
    else:
        print('not post')
        return render_template("util/uploadapk.html")

    # return redirect(url_for('upload'))
    # return render_template('upload.html')

@uiautotest.route('/upload')
def upload():
    return render_template('util/upload.html')

#新增Hitchhiker接口自动化
@uiautotest.route('/hitchhiker')
def hitchhiker():
    return render_template("util/hitchhiker.html")

#新增wedtor元素chakan
@uiautotest.route('/weditor')
def weditor():
    return render_template("util/weditor.html")

#新增mitmproxy代理
@uiautotest.route('/mitmproxy')
def mitmproxy():
    return render_template("util/mitmproxy.html")

#新增gitlab
@uiautotest.route('/gitlab')
def gitlab():
    return render_template("util/gitlab.html")

@uiautotest.route('/interfacetestcases')
def interfacecases():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("util/interfacetestcases.html")

@uiautotest.route('/interfacemock')
def interfacemock():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("util/interfacemock.html")

@uiautotest.route('/jira')
def jira():
    return render_template("util/jira.html")

@uiautotest.route('/testlink')
def tetlink():
    return render_template("util/testlink.html")

@uiautotest.route('/confluence')
def confluence():
    return render_template("util/confluence.html")

@uiautotest.route('/wiki')
def wiki():
    return render_template("util/wiki.html")

#获取设备列表
@uiautotest.route('/getDeviceList')
def getDeviceList():
    r =requests.get('http://192.168.0.24:20092/list')
    #content = json.loads(r)
    # deviceList = []
    # for device in content:
    #     if device['present']:
    #         deviceList.append(device['ip'] + ':7912')
    #     else:
    #         # log.log().logger.info(device['ip'] + ' is not ready!')
    #         pass
    # return deviceList
    return jsonify(r.text)

# 单元测试详情
@uiautotest.route('/view_unitest_result')
def view_unitest_result():
    info = request.values
    log.log().logger.info('info : %s' %info)
    id = getInfoAttribute(info, 'id')
    # from app import test_unittest_manage
    data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
    if len(data):
        filename = data[0]['file_name']
        return render_template("util/unittest_detail.html",file_name='/view_unitest_results?id='+id)
    else:
        return render_template("util/unittest_records.html")

# 单元测试详情
@uiautotest.route('/view_unitest_results')
def view_unitest_results():
    info = request.values
    log.log().logger.info('info : %s' %info)
    id = getInfoAttribute(info, 'id')
    # from app import test_unittest_manage
    data = test_unittest_manage.test_unittest_manage().show_unittest_records(['id'], [id], [], 100)
    if len(data):
        filename = data[0]['file_name']
        return render_template("reports/"+filename)
    else:
        return render_template("util/unittest_records.html")


@uiautotest.route('/run_unittest.json', methods=['POST', 'GET'])
def run_unittest():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        log.log().logger.info('run unittest')
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        else:
            from app.test import test_run_all
            log.log().logger.info('start run unittest')
            test_run_all.run_all()
            result = jsonify({'code': 200, 'msg': 'success!'})

            return result


# 节点管理
@uiautotest.route('/testhubs')
def testhubs():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("util/hubs.html",port=4444)

@uiautotest.route('/check_hubs.json', methods=['POST', 'GET'])
def check_hubs():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        log.log().logger.info(request)
        log.log().logger.info('check_hubs')
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        else:
            log.log().logger.info('start checking hubs')
            hubs.hubs().checkHubs()
            result = jsonify({'code': 200, 'msg': 'success!'})

            return result


@uiautotest.route('/add_hub.json', methods=['POST', 'GET'])
def add_hub():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        info = request.values
        log.log().logger.info('info : %s' %info)
        host = getInfoAttribute(info, 'host')
        port = getInfoAttribute(info, 'port')
        status=getInfoAttribute(info, 'status')
        hubs.hubs().updateHub(host,port,'0',status)
        result = jsonify({'code': 200, 'msg': '新增成功'})
        return result, {'Content-Type': 'application/json'}



#新增节点
@uiautotest.route('/add_hub')
def new_hub():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        return render_template("util/new_hub.html",port=4444)

#新增节点
@uiautotest.route('/edit_hub')
def edit_hub():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        info = request.values
        id = getInfoAttribute(info, 'id')
        data = hubs.hubs().searchHubs(id)
        if len(data):
            host = data[0]['ip']
            port = data[0]['port']
        else:
            host = ''
            port = 4444
        return render_template("util/new_hub.html", host=host,port=port)


#节点列表
@uiautotest.route('/search_hubs.json', methods=['POST', 'GET'])
def search_hubs():
    if not current_user.is_authenticated:
        response = redirect('/auth/login',code=302,Response=None)
        return response
    else:
        if request.method == 'POST':
            log.log().logger.info('post')
            result = jsonify({'code': 500, 'msg': 'should be get!'})
            return result
        else:
            info = request.values
            log.log().logger.info('info :  %s' %info)
            # name = getInfoAttribute(info, 'name')
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            from app.core import hubs
            # data= test_unittest_manage.test_unittest_manage().show_unittest_records(['name'], [name],[],100)
            data = hubs.hubs().searchHubs()
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
            log.log().logger.info('data1: %s' %data1)
            return data1, {'Content-Type': 'application/json'}

# 测试节点详情详情
@uiautotest.route('/view_hub')
def view_hub():
    # print(request.host)
    # print(request.host_url)
    # print(request.base_url)
    # print(request.url)
    # print(request.url_root)
    # print(request.remote_addr)
    # print("host",request.host_url.split(":")[1])
    # return render_template("util/view_hub.html", host=autotestconfig.ATXHost)
    return render_template("util/view_hub.html",host=request.host_url.split(":")[1]+":20092")



#检查登录信息是否正确
@uiautotest.route('/getDevicesList.json', methods=['POST', 'GET'])
def getDevicesList():
    #获取列表
    from app.core import hubs
    list=hubs.hubs().getDevicesList()
    log.log().logger.info('list %s' %list)
    result = jsonify({'msg': list})
    return result, {'Content-Type': 'application/json'}

def hBody(j, needRE):
    import json,re
    body = json.dumps(j, default=lambda j: j.__dict__, sort_keys=True, skipkeys=True)
    if needRE == '1':
        body = re.sub(r'\\', '', body)
        body = json.loads(body)
    return body



def getInfoAttribute(info,field):
    try:
        value = info.get(field)
    except:
        value = ''
    if value == None:
        value = ''
    return value
