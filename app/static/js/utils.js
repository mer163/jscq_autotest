//获取本地gitlab地址
var gitlabport=20090;
var hitchhikerport=20087;
var weditorport=20089;


function gethost(port){
    self.location.href="http://"+self.location.hostname+":20090"
}

function getGitlabhost() {
	self.location.href="http://"+self.location.hostname+":20090"
}

function gethitchhikerhost() {
    return "http://"+self.location.hostname+":20087"
}

function gethost(port){
    return "http://"+self.location.hostname+":"+port
}