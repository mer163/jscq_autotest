#!/bin/bash

ip=`ifconfig|grep 192.168| awk -F ':' '{print $2}'|awk '{print $1}'`
nohup python3  manage.py  runserver --host $ip --port 20088 >>log.log 2>&1 &
