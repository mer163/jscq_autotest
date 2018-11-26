DBtype =  '2'   # '1' : sqlite,  2: mysql
host='192.168.0.24'
port='3306'
user='root'
password='666666'
database='zbmock'

isUseATX=True
ATXHost = 'http://172.16.1.160:8002/'
confluenceHost= 'http://172.16.1.229:8090/#all-updates'
gitlabHost = 'http://gitlab.hudong.net'
hitchhikerHost= 'http://172.16.1.160:20087/'
jiraHost= 'http://192.168.0.24:8080/secure/Dashboard.jspa'
mitmproxHost= 'http://192.168.0.24:28081/'
testlinkHost= 'http://172.16.1.160:8000/'
weditorHost = 'http://172.16.1.160:8006/'
wikiHost='http://wiki.zbwxkj.office/'
mantis='http://172.16.1.210/bug/main_page.php'


import os,platform
currentPath = os.path.dirname(os.path.abspath(__file__))
print(currentPath)
if platform.system()=='Windows':
    logPath = currentPath + '\\log\\'
    reportPathWin = currentPath + '\\templates\\reports\\'
    unittestPathWin = currentPath + '\\test\\'
    screen_shot_path = currentPath + '\\static\\screenshot\\'
else:
    reportPathLinux =currentPath + '/templates/reports/'
    unittestPathLinux = currentPath + '/test/'
    logPath = currentPath + '/log/'
    screen_shot_path = currentPath +'/static/screenshot/'




