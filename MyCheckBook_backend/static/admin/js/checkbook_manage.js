layui.use(['table', "jquery"], function(){
    var table = layui.table;
  	$ = layui.jquery;
  	table.render({
      elem: '#checkbook_table'
      ,url:'/api/v1/checkbooks'
      ,toolbar: '#toolbarDemo'
      ,page: true
      ,cols: [[
      {type:'radio',fixed: 'left'}
      ,{field:'checkbook_name', width:150, title: '记账本名称', sort: true, fixed: 'left'}
      ,{field:'description', title: '描述'}
      ,{field:'rules', width:150, title: '内置规则约束'}
      ,{field:'partner', width:150, title: '参与人'}
      ,{field:'my_permission', width:120, title: '我的权限', sort: true,}
      ,{field:'status', width:80, title: '状态', sort: true, }
      ,{field:'create_time', width:160, title: '创建日期', sort: true}
      ,{field:'last_update_time', width:160, title: '最后更新时间', sort: true}
      ,{fixed:'right', width:150, title: '操作',toolbar: '#OperaTools'}
    ]]
  });

  //监听行工具事件
  table.on('tool(checkbook_table)', function(obj){
    var data = obj.data;
    //console.log(obj)
    if(obj.event === 'del'){
        layer.confirm('真的删除记账本【'+obj.data.checkbook_name+'】么', function(index){
            // 同步服务器删除 记账本
            $.ajax({
                url:"/api/v1/checkbook?checkbook_id="+obj.data.checkbook_id,
                type:'DELETE',
                dataType:'json',
                success:function(){ // http code 200
                    obj.del();
                    layer.close(index);
                },
                error:function(XMLHttpRequest, textStatus, errorThrown){
                       layer.msg('删除失败，您无权删除此记账本，请联系本记账本 创建者');
                }
            })

        });
    }
    else if(obj.event === 'detail'){
        var data = obj.data;
        console.log(data)
        //TODO 打开记账本详情编辑页
        layer.prompt({
            formType: 2
            ,value: data.email
        }, function(value, index){
            obj.update({
                email: value
            });
            layer.close(index);
        });
    }
    else if(obj.event == "invitation"){
        // 调用服务器接口，生成邀请码
        var data = obj.data;
        console.log(data)
        var code=""
         $.ajax({
              url:"/api/v1/CheckbookInvitationCode?checkbook_id="+obj.data.checkbook_id,
                type:'GET',
                dataType:'json',
                async:false,
                success:function(json){ // http code 200
                    code=json["invationCode"]
                },
                error:function(XMLHttpRequest, textStatus, errorThrown){
                       layer.msg('生成邀请码失败，请稍后再试');
              }
         });
         //弹窗 展示邀请码
        layer.alert(code,{title:'邀请码'});
    }
  });

    //头工具栏事件
  table.on('toolbar(checkbook_table)', function(obj){
    var checkStatus = table.checkStatus(obj.config.id);
    switch(obj.event){
      case 'join_by_code':
          layer.prompt({
              formType: 2
              ,value: ""
              ,title:"输入邀请码"
                },
              function(value, index){
              // 调用接口 加入记账本
                  $.ajax({
                    url:"/api/v1/CheckbookInvitationCode?code="+value,
                    type:'POST',
                    data:{"code":value},
                    dataType:'json',
                    success:function(){ // http code 200
                        layer.msg('加入记账本成功');
                    },
                    error:function(XMLHttpRequest, textStatus, errorThrown){
                           layer.msg('加入记账本失败');
                    }
                    })
                layer.close(index);
            });
      break;
      case 'create_check_book':
          // var url="checkbook_add";
          // var title="创建记账本"
          // var iframeObj = $(window.frameElement).attr('name');
          // parent.page(title, url, iframeObj, w = "700", h = "620px");
          layer.open({
              type: 2,
              content: "checkbook_add",
              area: ['700px', '620px'],
              end:function () {
                  table.reload("checkbook_table",{
                  url: "/api/v1/checkbooks"
                  ,where: {
                }
            })

              }
          })
      break;

    };
  });
});