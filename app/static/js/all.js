var allData=[];
// 格式化时间
function formatTime(time){
	var date = new Date();
	if (!time && time != '-') {
		return
	}
	var y = date.getFullYear();
	var m = date.getMonth()+1;
	if (m < 10) {
		m = '0' + m;
	}
	var d = date.getDate();
	if (d < 10) {
		d = '0' + d;
	}
	var h = date.getHours();
	if (h < 10) {
		h = '0' + h;
	}
	var min = date.getMinutes();
	if (min < 10) {
		min = '0' + min;
	}
	var mm = date.getSeconds();
	if (mm < 10) {
		mm = '0' + mm;
	}
	return y+'-'+m+'-'+d+' '+h+':'+min+':'+mm;
}

//获取总数据  && 搜索
function getAllData(){
	var _self=$(event.target);	
	var _url="/result";
	$.ajax({
		type:"get",
		url:myUrl+_url,
		async:true,
		dataType:"json",
		data:{},
		success:function(res){
			if(res.msg != "ok"){
				alert(res.msg);
				location.href= location.origin + "/auth/login";
				return;
			}
			var _data=res.data;
			allData=_data;
			currentPage=$(".page-active a").text();
			dataShow(allData,1);
			$('#page').jqPaginator({
				totalCounts: allData.length,
				pageSize:10,
				currentPage: 1,
				activeClass:"page-active",
				disableClass:"page-disabled",
				first: '<li class="first"><a href="javascript:void(0);">首页</a></li>',
				prev: '<li class="prev"><a href="javascript:void(0);">上一页</a></li>',
				next: '<li class="next"><a href="javascript:void(0);">下一页</a></li>',
				last: '<li class="last"><a href="javascript:void(0);">末页</a></li>',
				page: '<li class="page"><a href="javascript:void(0);" currentPage={{page}}>{{page}}</a></li>',
				onPageChange: function (num) {
					if (num>1) {						
						dataShow(allData,num);
					}
				}
			});
		}
	});
}

//数据解析
function dataShow(allData,currentPage){
	$("#msg-table tr:eq(0)").nextAll().remove();
	if(!currentPage){
		currentPage=1;
	}
	var trHTML="";
	for (var i=0;i<allData.length;i++) {
		var data_i=allData[i];
		if(i>=(currentPage-1)*10 && i<=(currentPage*10-1)){
			trHTML+='<tr class="tr-tit" id='+justObj(data_i.id)+'>'+
			'<td><i class="myckbox myckbox-normal" onclick="mycheckbox();"></i></td>'+
			'<td >'+justObj(data_i.id)+'</td>'+
			'<td class="t-starttime">'+justObj(data_i.starttime)+'</td>'+
			'<td class="t-endtime">'+justObj(data_i.endtime)+'</td>'+
			'<td class="t-url"><a href="'+justObj(data_i.url)+'">'+justObj(data_i.url)+'</a></td>'+
			'<td class="t-result'+justObj(data_i.result==1?" success":" fail") +'">'+justObj(data_i.result==1?"成功":"失败")+'</td>'+
			'</tr>';
		}

	}
	$("#msg-table").append(trHTML);
	return
}

//判断对象是否存在
function justObj(obj){
	if(obj && typeof(obj)!="undefined"){
		return obj;
	}else{
		return "-";
	}
}
//checkbox
function mycheckbox(){
	var _self=$(event.target);	
	if(_self.hasClass("myckbox-normal")){
		_self.removeClass("myckbox-normal").addClass("myckbox-visited");
	}else{
		_self.removeClass("myckbox-visited").addClass("myckbox-normal");
	}
	
	var myckbox_all=_self.closest("#msg-table").find("td").find(".myckbox").length;
	var myckbox_vsed=_self.closest("#msg-table").find("td").find(".myckbox-visited").length;
	if(myckbox_vsed<myckbox_all){
		_self.closest("#msg-table").find("#selectAll").removeClass("myckbox-visited").addClass("myckbox-normal");
	}else{
		_self.closest("#msg-table").find("#selectAll").removeClass("myckbox-normal").addClass("myckbox-visited");
	}
}

//select all
function selectAll(parent){
	var _self=$(event.target);
	var _parent=_self.closest(parent);
	if(_self.hasClass("myckbox-normal")){
		_self.removeClass("myckbox-normal").addClass("myckbox-visited");
		_parent.find(".myckbox").removeClass("myckbox-normal").addClass("myckbox-visited");
	}else{
		_self.removeClass("myckbox-visited").addClass("myckbox-normal");
		_parent.find(".myckbox").removeClass("myckbox-visited").addClass("myckbox-normal");
	}
}