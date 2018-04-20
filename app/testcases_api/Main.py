#!/usr/bin/env python
#coding=utf-8

import types
import datetime
import json
import logging
import os
import re
import requests
from app.testcases_api.runcase.run import runTest
# import http.lient,mimetypes
from urllib.parse import urlencode

try:
    import xlrd
except:
    os.system('pip install -U xlrd')
    import xlrd
try:
    from pyDes import *
except:
    os.system('pip install -U pyDes --allow-external pyDes --allow-unverified pyDes')

from app.testcases_api.runcase.py_Html import createHtml
from app.testcases_api.runcase.emmail import sendemali



def main(list):
    # 创建日志文件，以加方式打开创建文件
    datatime=str(datetime.datetime.now().strftime('%Y%m%d%H%m'))
    print(datatime)
    # log_file = os.path.join(
    #     u'E:\git\local\mock\interfacetest\log\log' + datatime + '.txt')
    # log_file = os.path.join('/var/www/testcase/logs/log.txt')
    log_file = os.path.join('/var/www/testcase/logs/log' + datatime + '.txt')
    f = open(log_file, 'a')
    f.write('\r')
    f.close()
    # 创建html报告文件，以加方式打开创建文件
    # result_file = os.path.join(u'E:\git\local\mock\interfacetest\\results\\result' + datatime + '.html')
    # result_file = os.path.join('/var/www/testcase/result.html')
    result_file = os.path.join('/var/www/testcase/results/result_'+ datatime + '.html')
    f = open(result_file, 'a')
    f.write('\r')
    f.close()

    print(log_file)
    print(result_file)
    # if not os.path.exists(log_file):
    #     os.mknod(log_file)
    # if not os.path.exists(result_file):
    #     os.mknod(result_file)

    log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, filename=log_file, filemode='w', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    starttime = datetime.datetime.now()
    print(starttime)
    # list_fail, list_pass, list_json, listurls, listparams, listmethords, listexpects, listids, listrelust, listnames = runTest('TestCase/TestCase.xlsx',sheetindex)
    list_fail, list_pass, list_json, listurls, listparams, listmethords, listexpects, listids, listrelust, listnames = runTest(list)
    # filepath = os.path.join(os.getcwd(),'/results/result.html')
    # filepath = os.path.join(os.getcwd(),'/results/result.html')
    # if os.path.exists(result_file) is False:
    #     os.system(r'touch %s' %result_file)
    endtime = datetime.datetime.now()
    #create result port
    createHtml(titles='接口测试报告',filepath=result_file,starttime=starttime,endtime=endtime,passge=list_pass,fail=list_fail,id=listids,name=listnames,
               param=listparams,url=listurls,meth=listmethords,yuqi=listexpects,json=list_json,relusts=listrelust)

    # 发送邮件
    # html_report = r'report\relult.html'
    # sendemali(html_report)
    status = 1
    if list_fail:
        status=2
        return starttime,endtime,datatime,status
    else:
        return starttime,endtime,datatime,status

if __name__ == '__main__':
    listargs = []
    if len(sys.argv) ==1:
        print("没有任何参数，将读取整个excel中素有表进行测试")
        html_report = r'E:\git\local\mock\interfacetest\result.html'
        sendemali(html_report)
        main(listargs)
    elif len(sys.argv) >=2:
        print("读取到excel表参数")
        for i in range(1,len(sys.argv)):
            print("参数：" + str(i) + "--->名称：" + sys.argv[i] )
            listargs.append(sys.argv[i])
        main(listargs)


    # if len(sys.argv) == 2:
    #     sheetindex = sys.argv[1]
    #     index = 0
    #     try:
    #         index = int(sheetindex)
    #         print(index)
    #     except Exception:
    #         print("类型转换异常" )
    #     if type(index) is int:
    #         main(index)
    #     else:
    #         print("参数类型错误")
    #         sys.exit(1)
    # elif len(sys.argv) ==1:
    #     print("无参数，默认读取excel第一个sheet")
    #     main(0)
    # else:
    #     for i in range(1,len(sys.argv)):
    #         print(str(i) + "-----" + sys.argv[i])
    #         listargs.append(sys.argv[i])
    #
    #
    #     main(listargs)
        # print("参数个数不正确")

    # main()
