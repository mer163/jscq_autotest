#!/bin/bash


echo '拉取最新代码'
git fetch --all
git reest --hard
git pull

echo '切换至dev分支'
git checkout dev

echo '最近3条更新日志'
git log -3

echo '覆盖修改配置文件'
cp -rf /app_code/config.ini  .
cp -rf /app_code/autotestconfig.py /app_code/platform/jscq_autotest/app/

#停掉服务，并重启服务
./restart.sh

