//获取本地gitlab地址
function getGitlabhost() {
	console.log("http://"+self.location.hostname+":20090")
	self.location.href="http://"+self.location.hostname+":20090"
}