layui.use(['layer', 'jquery',"table", "laydate", "element", "form"], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    var form = layui.form;

    // 设置记账本下拉框
    function init_checkbook(result) {
     resultData = result;
         var parent_html = $("#checkbook_selector").html();
         var htmls =""
     for(var x=0; x<resultData.length; x++){
             var htmls = '<option value = "' + resultData[x].checkbook_id + '">' + resultData[x].checkbook_name + '</option>';
             if(x==0){
                 checkbook_id = resultData[x].checkbook_id
             };
     };
         parent_html = parent_html.replace("checkbook_selector_replace",htmls);
         $("#checkbook_selector")[0].innerHTML = parent_html;
         form.render();
   };
    init_checkbook(checkbook_list_json)

    // 出事table
    var checkbook_id = $("#checkbook_selector option:selected").val();
    function init_table(){
       detail_tableIns =  table.render({
           elem: '#report_table'
           ,id:"report_table-id"
           ,page: true
           ,url:"/api/v1/report?checkbook_id="+checkbook_id+"&action=list"
           ,cols: [[
              {field:'report_name', width:200, title: '财报名称', sort: true, fixed: 'left'}
              ,{field:'type',width:80, title: '类型', sort: true}
              ,{field:'period', width:200, title: '统计时段', sort: true}
              ,{field:'own_name', width:150, title: '个人名称'}
              ,{field:'career', width:150, title: '职业', sort: true,}
              ,{field:'auditor', width:80, title: '审计师', sort: true,}
              ,{field:'suggestion',  title: '审计师建议', sort: true, }
              ,{field:'checkbook_name', width:150, title: '所属记账本', sort: true}
              ,{field:'create_date', width:120, title: '创建日期', sort: true}
              ,{fixed:'right', width:250, title: '操作',toolbar: '#OperaTools'}
            ]]
            ,data:[]
        });
    }
    init_table()


    function edit_report(data,obj){
        layer.msg("edit_report")
    }

    function delete_report(data, obj){
        layer.msg("delete_report")
        confirm_text = '真的删除如下财报么？<br/>';
        confirm_text += '【'+data.report_name+"-"+data.type+ "-"+data.period+'】<br/>';
         layer.confirm(confirm_text, function(index){
             $.ajax({
                url:"/api/v1/report?report_id="+data.id,
                type:'DELETE',
                dataType:'json',
                success:function(){ // http code 200
                    obj.del();
                    layer.close(index);
                    parent.layer.msg('删除成功!!');
                },
                error:function(XMLHttpRequest, textStatus, errorThrown){
                   parent.layer.msg('删除失败!!');
                }
            })

         });
    }

    function  download_report(data, obj) {
        layer.msg("download_report")
    }

    //监听行工具事件
    table.on('tool(report_table)', function(obj){
        var data = obj.data;
        switch(obj.event){
             case 'delete':
                 delete_report(data,obj);
                 break;
             case "edit":
                 edit_report(data,obj);
                 break
             case "download":
                 download_report(data, obj);
                 break;
         }
    });


});