#!/bin/bash

#从进程中找到运行的程序，并杀掉
kill -9 `ps aux |grep python3 | grep manage|awk '{print $2}'`

#重启服务
./start.sh
