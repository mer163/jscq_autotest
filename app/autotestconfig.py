DBtype =  '2'   # '1' : sqlite,  2: mysql
host='192.168.0.24'
port='3306'
user='root'
password='666666'
database='zbmock'

isUseATX=True
ATXHost = 'http://192.168.0.24:20092'
confluenceHost= 'http://192.168.0.24:8090'


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




