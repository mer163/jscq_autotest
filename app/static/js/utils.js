//获取本地gitlab地址
var gitlabport=20090;
var hitchhikerport=20087;
var weditorport=20089;
var confluenceport=8090;
var jiraport=8080;
var mitmproxyport=28081;


function gethost(port){
    self.location.href="http://"+self.location.hostname+":20090"
}

function getGitlabhost() {
	self.location.href="http://gitlab.hudong.net"
}

function gethitchhikerhost() {
    return "http://"+self.location.hostname+":20087"
}

function gethost(port){
    return "http://"+self.location.hostname+":"+port
}