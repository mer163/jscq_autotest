##**自动化平台本地测试环境**

**url:https://github.com/mer163/jscq_autotest**

##**`_技术栈_`：**
1、python3、golang  
2、flask web框架  
3、HTML、css、js  
4、selenium chromedriver firefoxdriver  
5、Python requests     

**_`安装部署`_**  
1、安装依赖  
2、启动主服务./build.sh  
3、启动ui自动化执行服务 ./start_coreservice.sh  
4、内部调用各服务需要单独启动各服务

**`_本地地址：_`** http://192.168.0.24:20088  
 
功能包含：  
UI自动化测试   
1、chrome、firefox浏览器测试  android app测试  
2、测试用例维护  
3、测试suit维护  
4、selenium grid节点维护管理  
5、步骤说明，关键字转command  

**_`本地selenium grid （zalenium 开源 基于selenium grid二次开发）`_**  
1、地址 http://192.168.0.24:4444  
2、目前集成了chrome、firefox浏览器  
3、dashboard 各node节点执行录像回放 http://192.168.0.24:4444/dashboard  
4、node执行时实时画面展示 http://192.168.0.24:4444/grid/admin/live  


**_`接口自动化测试`_** 
1、http接口管理，新增 删除 执行 查看结果  
2、接口自动化mock （提供假数据mock）  

**_`性能测试`_**  
1、集成hitchhiker开源平台 内嵌使用  
2、其他如jmeter等后期增加  

**_`常用工具**_ `  
android电量查看  
1、android 电量查看，基于shell统计当前android设备电量信息  
2、默认从server取第一个在线设备进行页面展示  
3、目前未做数据保存，后期考虑增加数据保存，曲线图展示  

**_`android设备管理`_**  
1、android设备管理，基于atx-server部署在docker容器中，对外暴露20088端口  
2、android设备需要启动atx-agent程序（默认7912端口），通过长连接与server通讯，实时展示当前设备信息  
3、远程控制android手机，如同本地操控手机  
4、远程shell、远程截图、远程视频录制  

**_`android元素定位weditor`_**  
1、远程连接android设备，通过dump获取远程设备xml 解析为hierachy  
2、远程操作设备，页面自动刷新  
3、Python uiautomator脚本自动生成  
4、页面元素信息查看获取  
5、页面元素坐标点计算显示  

**_`fileshare文件共享`_**  
1、共享目录为smb共享目录   
2、远程web页面上传、下载文件至共享server  

**_`测试管理平台`_**  
1、集成jira内嵌  
2、集成testlink内嵌  
3、集成confluence内嵌  
4、集成wiki内嵌  

