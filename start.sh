#!/bin/bash

nohup python3  manage.py  runserver --host 192.168.0.24 --port 20088 >>log.log 2>&1 &
