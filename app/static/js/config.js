//请求后端地址配置
// var myUrl="http://localhost:5001/testcases";
// var mockUrl="http://localhost:5001/mock";


// var myUrl="http://192.168.0.24:20088/testcases";
// var mockUrl="http://192.168.0.24:20088/mock";

var urlAndPort=window.location.protocol + "//"+ window.location.host + ":" +window.location.port

var myUrl=urlAndPort + "/testcases"
var mockUrl= urlAndPort +"/mock"