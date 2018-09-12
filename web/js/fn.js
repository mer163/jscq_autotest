var allData=[];
//获取项目名称
function projectNameList(){
	$.ajax({
		type:"get",
		url:myUrl+"/searchCaseProject",
		async:true,
		dataType:"json",
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			var _data=res.data;
			var optionHtml="";
			for (var i=0;i<_data.length;i++) {
				optionHtml+='<option value='+_data[i]+'>'+_data[i]+'</option>'
			}
			$(".product-name").append(optionHtml);
		}
	})
}
//获取总数据  && 搜索
function getAllData(){
	var _self=$(event.target);
	var condition=$(".search-box input").val();
	var _project_name=$(".product-name option:selected").attr("value");
	// var _url="/search";
	var _url="/searchCase";
	/* 问题
		** 1 _project_name == 0 如果用 !_project_name 是false
		** 2 !condition && !_project_name 有问题
		** 3 searchall这个接口 返回的所属项目 为--
		**  
		*/
		if(!condition && _project_name == 0){
		// _url="/searchall";
		_url="/searchAllCase";
	}
	$.ajax({
		type:"get",
		url:myUrl+_url,
		async:true,
		dataType:"json",
		data:{
			title:condition,
			project_name:_project_name
		},
		success:function(res){
			if(res.msg!="ok"){
				alert(res.remark);
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
					dataShow(allData,num);
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
			'<td class="t-title">'+justObj(data_i.title)+'</td>'+
			'<td class="t-methods">'+justObj(data_i.methods)+'</td>'+
			'<td class="t-projectName">'+justObj(data_i.projectName)+'</td>'+
			'<td class="t-env">'+justObj(data_i.env)+'</td>'+
			'<td class="t-checkpoint">'+justObj(data_i.checkpoint)+'</td>'+
			'<td class="t-rel">'+justObj(data_i.correlation)+'</td>'+
			'<td class="t-domain">'+justObj(data_i.domain)+'</td>'+
			'<td class="describle">'+justObj(data_i.description)+'</td>'+
			'<td >'+justObj(data_i.updateTime)+'</td>'+
			'<td >'+
			'	<i class='+'"'+((data_i.status==0)? 'activation left on' : "activation off")+'"'+' onclick="activation();">'+
			'		<i class="activa-bar"></i>'+
			'	</i>'+
			'</td>'+
			'<td  class="no-padding">'+
			'	<i class="edit left mr5" onclick="edit();"></i>'+
			'	<i class="copy left" onclick="copyHandle();"></i>'+
			'</td>'+
			'</tr>'+
			'<tr class="hidden">'+
			'<td colspan="8">'+
			'<div class="tr-detail">'+
			'<div class="dt-cont">'+
			'<b>请求参数：</b><span class="dt-cont-s">'+justObj(data_i.reqparams)+'</span>'+
			'</div>'+
			'<div class="dt-cont" style="display:none">'+
			'<b>预期返回：</b><span class="dt-cont-y">'+justObj(data_i.resparams)+'</span>'+
			'</div>'+
			'</div>'+
			'</td>'+
			'</tr>';
		}
	}
	$("#msg-table").append(trHTML);
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
//activation
function activation(){
	var _self=$(event.target);
	var _id=_self.closest("tr").attr("id");
	var current_status="";
	
	if(_self.hasClass("activa-bar")){
		_self=$(event.target).parent();
	}
	if(_self.hasClass("off")){
//		_self.removeClass("off").addClass("on");
current_status=0;
}else{
//		_self.removeClass("on").addClass("off");
current_status=1;
}
$.ajax({
	type:"post",
	url:myUrl+"/manageCase",
	async:true,
	dataType:"json",
	data:{
		id:parseInt(_id),
		status:current_status
	},
	success:function(res){
		if(res.msg!="ok"){
			alert(res.remark);
			return;
		}
		getAllData();
	}
});
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
}//新增
function add(){
	var type=$(".sure").attr("data-type");
	var _id=$(".ctrl-pop").attr("current_id");
	// by@myj 更新addinfo 、editinfo接口为addTestCase
	if(type=="add"){
		// var reqUrl=myUrl+"/addinfo";
		var reqUrl=myUrl+"/addTestCase";
	}else{
		// var reqUrl=myUrl+"/editinfo";
		var reqUrl=myUrl+"/editTestCase";
	}
	$.ajax({
		type:"post",
		url:reqUrl,
		async:true,
		dataType:"json",
		data:{
			id:_id?_id:"",
			title:$(".r-title").val(),
			methods:$(".r-method option:selected").text(),
			projectName:$(".source-object").val(),
			reqparams:$(".r-reqparams").val(),
			// resparams:$(".r-resparams").val(),
			description:$(".r-des").val(),
			domain:$(".r-domain").val(),
			env: $(".r-env").val(),
			checkpoint: $(".check-point").val(),
			correlation: $(".r-rel").val()
			// ischeck:$(".isJYrequst").hasClass("myckbox-visited") ? 1 : 0
		},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			getAllData();
			$(".ctrl-pop").addClass("hidden");
		}
	})
}
//删除
function del(){
	var ids=[];
	$(".msg-table tr").each(function(){
		if($(this).find(".myckbox").hasClass("myckbox-visited")){
			var _id=$(this).attr("id");
			ids.push(parseInt(_id));
		}
	})
	$.ajax({
		type:"post",
		url:myUrl+"/delCase ",
		async:true,
		dataType:"json",
		data:{id:ids},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("删除成功！");
			getAllData();
		}
	})
}
//执行 所选
function run(){
	var ids=[];
	$(".msg-table tr").each(function(){
		if($(this).find(".myckbox").hasClass("myckbox-visited")){
			var _id=$(this).attr("id");
			ids.push(parseInt(_id));
		}
	})
	$.ajax({
		type:"post",
		url:myUrl+"/runCase ",
		async:true,
		dataType:"json",
		data:{id:ids},
		success:function(res){
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("提交成功！");
			getAllData();
		}
	})
}
//执行 所有
function runAll(){
	$.ajax({
		type:"post",
		url:myUrl+"/runAllCase ",
		async:true,
		dataType:"json",
		data:{},
		success:function(res){
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("提交成功！");
			getAllData();
		}
	})
}
//编辑
function edit(){
	var current_id=$(event.target).closest("tr").attr("id");
	var currentTr=$("#msg-table tr[id="+current_id+"]");
	var _title=currentTr.find(".t-title").text();
	var _domain=currentTr.find(".t-domain").text();
	var _methods=currentTr.find(".t-methods").text();
	var _projectName=currentTr.find(".t-projectName").text();
	var _reqparams=currentTr.next().find(".dt-cont-s").text();
	var _resparams=currentTr.next().find(".dt-cont-y").text();
	var _des=currentTr.find(".describle").text();
	var _env=currentTr.find(".t-env").text();
	var _checkpoint=currentTr.find(".t-checkpoint").text();
	var _correlation=currentTr.find(".t-rel").text();

	// 增加了 环境 检查点和关联的条件
	
	$(".ctrl-pop").attr("current_id",current_id);
	$(".ctrl-pop .pop-tit").text("+ 编辑");
	$(".ctrl-pop .r-title").val(_title=="-"?"":_title);
	$(".ctrl-pop .r-domain").val(_domain=="-"?"":_domain);
	$(".ctrl-pop .source-object").val(_projectName=="-"?"":_projectName);
	$(".ctrl-pop .r-method .method-sed").prop("selected","selected").text(_methods=="-"?"":_methods);
	$(".ctrl-pop .r-reqparams").val(_reqparams=="-"?"":_reqparams);
	$(".ctrl-pop .r-resparams").val(_resparams=="-"?"":_resparams);
	$(".ctrl-pop .r-des").val(_des=="-"?"":_des);
	$(".ctrl-pop .r-env").val(_env=="-"?"":_env);
	$(".ctrl-pop .check-point").val(_checkpoint=="-"?"":_checkpoint);
	$(".ctrl-pop .r-rel").val(_correlation=="-"?"":_correlation);
}
//复制
function copyHandle(){
	var _id=$(event.target).closest("tr").attr("id");
	$.ajax({
		type:"post",
		url:myUrl+"/copyCase",
		async:true,
		dataType:"json",
		data:{id:_id},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("复制成功！");
			getAllData();
		}
	})
}





















