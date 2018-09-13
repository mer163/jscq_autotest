#!/bin/bash

#从进程中找到运行的程序，并杀掉
count=`ps aux |grep 'python3 manage.py runserver' |awk 'END{print NR}'`

if [[ $count -gt 1 ]]; then
  echo '发现flask服务已启动，启动kill杀掉服务'
  kill -9 `ps aux |grep python3 | grep manage|awk '{print $2}'`
else
  echo 'flask服务未启动，准备启动服务'
#重启服务
fi

./start.sh
echo 'flask服务启动成功'


coreservicecount=`ps aux |grep 'coreservice' |awk 'END{print NR}'`

if [[ $coreservicecount -gt 1 ]]; then
  echo '发现coreservice服务已启动，启动kill杀掉服务'
  kill -9 `ps aux |grep coreservice|awk '{print $2}'`
else
  echo '服务未启动，准备启动服务'
#重启服务
fi
./start_coreservice.sh
echo 'coreservice服务启动成功'