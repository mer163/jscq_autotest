#!/usr/bin/env python
#coding=utf-8

import os
import logging
import sys,re
import requests
from urllib.parse import urlencode
import json

# from interfacetest.Interface import excelUtil

try:
    import xlrd
except:
    os.system('pip install -U xlrd')
    import xlrd

correlationDict = {}

def runTest(list):


    errorCase = []
    # correlationDict['token']= None

    list_pass = 0
    list_fail = 0
    list_json = []
    listresult = []
    listurls = []
    listids = []
    listparams = []
    listmethords = []
    listexpects = []
    listnames = []

    print('type',type(correlationDict))
    print('correlationDict',correlationDict)

    for case in list:
        print(case['id'])
        if case['status'] =='0':
            continue
        num = case['id']
        purpose = case['title']
        api_host = case['env']
        request_url = case['domain']
        request_method = case['methods']
        request_data_type = 'Form'
        request_data = case['reqparams']
        # encryption = sheets[j].cell(i, 7).value.replace('\n', '').replace('\r', '')
        check_point = case['checkpoint']
        str_correlation = case['correlation']
        if str_correlation is None or str_correlation.strip()=='':
            correlation = ''
        else:
           correlation = str_correlation.split(':')  ##读取需要关联的参数
        # correlation = case['correlation'].replace('\n', '').replace('\r', '').split(':')  ##读取需要关联的参数

        # print(case['correlation'])
        # correlation=''
        # if case['correlation'] is None:
        #     print("correlation is null")
        #     # correlation = case['correlation']
        # else:
        #     correlation = case['correlation'].replace('\n', '').replace('\r', '').split(':')


        # if sheets[j].cell(i, 10).value.replace('\n', '').replace('\r', '') != 'Yes':
        #     continue
        # num = str(int(sheets[j].cell(i, 0).value)).replace('\n', '').replace('\r', '')
        # purpose = sheets[j].cell(i, 1).value.replace('\n', '').replace('\n', '')
        # api_host = sheets[j].cell(i, 2).value.replace('\n', '').replace('\r', '')
        # request_url = sheets[j].cell(i, 3).value.replace('\n', '').replace('\r', '')
        # request_method = sheets[j].cell(i, 4).value.replace('\n', '').replace('\r', '')
        # request_data_type = sheets[j].cell(i, 5).value.replace('\n', '').replace('\r', '')
        # request_data = sheets[j].cell(i, 6).value.replace('\n', '').replace('\r', '')
        # encryption = sheets[j].cell(i, 7).value.replace('\n', '').replace('\r', '')
        # check_point = sheets[j].cell(i, 8).value
        # correlation = sheets[j].cell(i, 9).value.replace('\n', '').replace('\r', '').split(':')  ##读取需要关联的参数

        if request_data_type == 'Form':
            print(" Form params")
            if  correlationDict:
                print('进入读取参数化内容循环')
                for keyword in correlationDict:
                    if request_data.find(keyword) > 0:
                        request_data = request_data.replace(keyword, str(correlationDict[keyword]))
            else:
                print('correlationDict 为空')
                correlationDict['token']=''

            # 判断quest_data是否为空
            if (request_data is not None or not request_data.splite()==''):
                print('request_data is not null')
                try:
                    request_data = urlencode(json.loads(request_data))
                except:
                    logging.error(num + purpose + 'params error, please check the request data.')
                    continue
            else:
                print('request_data is not null')

            print('requestdata: ',request_data)
            code, response = interfaceTest(api_host, request_url, request_data, request_method,token=correlationDict['token'])
            print('进入参数关联循环')
            for j in range(len(correlation)):
                param = correlation[j].split('=')
                if len(param) == 2:
                    # 判断格式是否正确
                    if param[1] == '' or not re.search(r'^\[', param[1]) or not re.search(r'\]$', param[1]):
                        logging.error(num + ' ' + purpose + ' 关联参数设置有误，请检查[Correlation]字段参数格式是否正确！！！')
                        continue
                    value = json.loads(response)
                    for key in param[1][1:-1].split(']['):
                        try:
                            temp = value[int(key)]
                        except:
                            try:
                                temp = value[key]
                            except:
                                break
                        value = temp
                    correlationDict[param[0]] = value
            if code == check_point:
                # print('ok')
                listids.append(num)
                listurls.append(request_url)
                listparams.append(request_data)
                listmethords.append(request_method)
                listexpects.append(check_point)
                listnames.append(purpose)
                list_json.append(response)
                listresult.append('pass')
                list_pass += 1
            else:
                print('fail')
                listids.append(num)
                listurls.append(request_url)
                listparams.append(request_data)
                listmethords.append(request_method)
                listexpects.append(purpose)
                listnames.append(purpose)
                list_json.append(response)
                listresult.append('fail')
                list_fail += 1

    return list_fail,list_pass,list_json,listurls,listparams,listmethords,listexpects,listids,listresult,listnames
    # print("test")


def interfaceTest(api_host,request_url,request_data,request_method,token=''):
    # print('start quest.')
    # logging.info('参数：num=' + num + 'purpose:'+ purpose)
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With':'XMLHttpRequest',
               'Connection':'keep-alive',
               'Referer':'http://' + api_host,
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
    #判断token不为空，则添加到header中
    if  token.split()=='':
        print('token is not null')
        print(token)
        headers['Cookie'] = 'token=' + token
        print(headers)
    else:
        print('token is null')

    print('request_method:',request_method)
    if request_method.strip() == 'POST':
        print('进入post')
        if(request_data.split()==''):
            r = requests.post(url=api_host+ request_url,headers=headers)
        else:
            r = requests.post(url=api_host+ request_url, data=request_data,headers=headers)
        ##判断如果返回headers中，如果有token，则进行保存
        print('请求完成：',r.text)
        if re.search("token=", str(r.headers)):
            correlationDict['token'] = r.headers['Set-Cookie'].split(';')[0].split('=')[1]
            print('settoken')
        if r.status_code ==200:
            if re.search('resultCode',r.text):

                print('return:',r.json())
                # json = r.text.json()
                # print(r.json())

                code = r.json()['resultCode']

        return code, r.text

    elif request_method == 'GET':
        r = requests.get(url=api_host+request_url, params=request_data,headers=headers)
        ##判断如果返回headers中，如果有token，则进行保存
        if re.search("token=", str(r.headers)):
            correlationDict['token'] = r.headers['Set-Cookie'].split(';')[0].split('=')[1]

        if r.status_code ==200:
            if re.search('resultCode',r.text):

                # print(r.json())
                # json = r.text.json()
                print(r.json())

                code = r.json()['resultCode']

                return code, r.text
        else:
            logging.error('请求失败，返回状态码 %s',r.status_code)

    else:
        print("未知请求方法",request_method)