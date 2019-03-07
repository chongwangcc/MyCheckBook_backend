layui.use('table', function(){
  var table = layui.table;

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
      ,{field:'my_role', width:150, title: '我的角色', sort: true,}
      ,{field:'my_permission', width:150, title: '我的权限', sort: true,}
      ,{field:'status', width:80, title: '状态', sort: true, }
      ,{field:'create_time', width:170, title: '创建日期', sort: true}
      ,{field:'last_update_time', width:170, title: '最后更新时间', sort: true}
      ,{fixed:'right', width:200, title: '操作',toolbar: '#OperaTools'}
    ]]
  });

  //头工具栏事件
  table.on('toolbar(test)', function(obj){
    var checkStatus = table.checkStatus(obj.config.id); //获取选中行状态
    switch(obj.event){
      case 'getCheckData':
        var data = checkStatus.data;  //获取选中行数据
        layer.alert(JSON.stringify(data));
      break;
    };
  });
});

				// <!--<colgroup>-->
				// 	<!--<col width="50">-->
				// <!--<thead>-->
				// 	<!--<tr>-->
				// 		<!--<th></th>-->
				// 		<!--<th >记账本名称</th>-->
				// 		<!--<th >创建日期</th>-->
				// 		<!--<th >最后更新时间</th>-->
				// 		<!--<th >描述</th>-->
				// 		<!--<th>参与人</th>-->
				// 		<!--<th>状态</th>-->
				// 		<!--<th>模板规则</th>-->
				// 		<!--<th>操作</th>-->
				// 	<!--</tr>-->
				// <!--</thead>-->
				// <!--<tbody>-->
				// 	<!--<tr>-->
				// 		<!--<td><input type="radio" name="" lay-skin="primary" data-id="1"></td>-->
				// 		<!--<td class="hidden-xs">CM家庭记账本</td>-->
				// 		<!--<td class="hidden-xs">2019.2.28</td>-->
				// 		<!--<td>1989-10-14</td>-->
				// 		<!--<td class="hidden-xs">家庭记账本</td>-->
				// 		<!--<td class="hidden-xs">CC,MM</td>-->
				// 		<!--<td><button class="layui-btn layui-btn-mini layui-btn-normal">正常</button></td>-->
				// 		<!--<td class="hidden-xs">收入分配 1:2:7</td>-->
				// 		<!--<td>-->
				// 			<!--<div class="layui-inline">-->
				// 				<!--<button class="layui-btn layui-btn-small layui-btn-normal go-btn" data-id="1" data-url="article-detail.html"><i class="layui-icon">&#xe642;</i></button>-->
				// 				<!--<button class="layui-btn layui-btn-small layui-btn-danger del-btn" data-id="1" data-url="article-detail.html"><i class="layui-icon">&#xe640;</i></button>-->
				// 			<!--</div>-->
				// 		<!--</td>-->
				// 	<!--</tr>-->
				// 						<!--<tr>-->
				// 		<!--<td><input type="radio" name="" lay-skin="primary" data-id="1"></td>-->
				// 		<!--<td class="hidden-xs">CM家庭记账本</td>-->
				// 		<!--<td class="hidden-xs">2019.2.28</td>-->
				// 		<!--<td>1989-10-14</td>-->
				// 		<!--<td class="hidden-xs">家庭记账本</td>-->
				// 		<!--<td class="hidden-xs">CC,MM</td>-->
				// 		<!--<td><button class="layui-btn layui-btn-mini layui-btn-normal">正常</button></td>-->
				// 		<!--<td class="hidden-xs">收入分配 1:2:7</td>-->
				// 		<!--<td>-->
				// 			<!--<div class="layui-inline">-->
				// 				<!--<button class="layui-btn layui-btn-small layui-btn-normal go-btn" data-id="1" data-url="article-detail.html"><i class="layui-icon">&#xe642;</i></button>-->
				// 				<!--<button class="layui-btn layui-btn-small layui-btn-danger del-btn" data-id="1" data-url="article-detail.html"><i class="layui-icon">&#xe640;</i></button>-->
				// 			<!--</div>-->
				// 		<!--</td>-->
				// 	<!--</tr>-->
				// <!--</tbody>-->