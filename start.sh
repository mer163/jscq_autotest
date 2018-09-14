#!/bin/bash

#获取服务器本地ip地址
ip=`ifconfig|grep 192.168| awk -F ':' '{print $2}'|awk '{print $1}'`

#启动服务，日志保存至log.log文件中
nohup python3  manage.py  runserver --host $ip --port 20088 >app/log/serverlog.log 2>&1 &
