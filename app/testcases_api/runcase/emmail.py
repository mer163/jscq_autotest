# -*- coding: utf-8 -*-
# @Author  : leizi
import  smtplib,time,os
from  email.mime.text import MIMEText
from email.utils import formataddr,parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
def load_emil_setting():#从配置文件中加载获取email的相关信息
	import yaml
	# data_file = open(r"E:\git\local\interface\\Data\\email.yaml","r")
	print(os.path.join(os.getcwd(),'Data\\email.yaml'))
	data_file = open(os.path.join(os.getcwd(),'data\\email.yaml'), "r")
	datas = yaml.load(data_file)
	data_file.close()
	# print(datas['foremail'])
	# print(datas['password'])
	# print(datas['toeamil'])
	# print(datas['title'])
	# print(datas['smtpaddress'])
	return (datas['foremail'],datas['password'],datas['toeamil'],datas['title'],datas['smtpaddress'],datas['smtpport'])
def sendemali(filepath): #发送email
	from_addr,password,mail_to,mail_body,smtpaddress,smtpport=load_emil_setting()
	msg = MIMEMultipart()
	msg['Subject'] = '接口自动化测试报告'    
	msg['From'] ='自动化测试平台'
	msg['To'] = mail_to
	msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
	att = MIMEText(open(r'%s'%filepath, 'rb').read(), 'base64', 'utf-8')
	att["Content-Type"] = 'application/octet-stream'  
	att["Content-Disposition"] = 'attachment; filename="result.html"'

	txt = MIMEText(open(r'%s'%filepath, 'rb').read(),"html","utf-8") # htnl格式展示
	# txt = MIMEText("这是测试报告的邮件，详情见附件",'plain','gb2312')  #纯文本展示
	msg.attach(txt)
	msg.attach(att)
	smtp = smtplib.SMTP()
	server = smtplib.SMTP_SSL(smtpaddress,smtpport)
	server.login(from_addr, password)
	server.sendmail(from_addr, mail_to, msg.as_string())
	server.quit()
	print("邮件发送成功")


if __name__ == '__main__':
	project_path=r'..\report\result.html'
	sendemali(project_path)