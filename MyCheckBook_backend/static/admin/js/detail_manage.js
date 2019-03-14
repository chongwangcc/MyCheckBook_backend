function init_pie1(mychart, mdata, callback) {
    var myoption = {
        color: ['#ff7f50','#87cefa','#da70d6','#32cd32','#6495ed',
            '#ff69b4','#ba55d3','#cd5c5c','#ffa500','#40e0d0',
            '#1e90ff','#ff6347','#7b68ee','#00fa9a','#ffd700',
            '#6699FF','#ff6666','#3cb371','#b8860b','#30e0e0'],
        title: {
            text:mdata.sumType+"\n"+mdata.sumValue,
            x:"center",
            y:"center"
        },
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b}: {c}元 ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x:"left",
            y:"top",
            data: mdata.legend
        },
        series: [
            {
                type: 'pie',
                radius: ['35%', '70%'],
                selectedMode: 'single',
                data: mdata.data
            }]
    };
    mychart.setOption(myoption)
    mychart.on('click',callback);
}

function init_pie2(mychart, mdata, callback){
    var myoption = {
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b}: {c}元 ({d}%)"
        },
        center: ['1%', '50%'],
        legend: {
            orient: 'vertical',
            x:"right",
            y:"top",
            data: mdata.legend
        },
        color: ['#ff7f50','#87cefa','#da70d6','#32cd32','#6495ed',
            '#ff69b4','#ba55d3','#cd5c5c','#ffa500','#40e0d0',
            '#1e90ff','#ff6347','#7b68ee','#00fa9a','#ffd700',
            '#6699FF','#ff6666','#3cb371','#b8860b','#30e0e0'],
        title: {
            text:mdata.sumType+"\n"+mdata.sumValue,
            x:"center",
            y:"center"
        },
        series: [
            {
                type: 'pie',
                radius: ['25%', '45%'],
                selectedMode: 'single',
                label: {
                    normal: {
                        position: 'inner'
                    },
                    formatter: '{d}%',

                    textStyle: {
                        color: '#fff',
                        fontWeight: 'bold',
                        fontSize: 14
                    }
                },
                labelLine: {
                    normal: {
                        show: true
                    }
                },
                data: mdata.data1
            },
            {
                type: 'pie',
                radius: ['50%', '70%'],
                selectedMode: 'single',

                data: mdata.data2
            }]
    };
    mychart.setOption(myoption)
    mychart.on('click',callback);
}

function init_echarts($){
    var myCharts = [];
    var mycharts_id = ["income_category_echart","income_account_echart",
        "spent_category_echart","spent_account_echart",
        "inflow_category_echart","inflow_account_echart",
        "outflow_category_echart","outflow_account_echart"
    ]
    var checkbook_id = "none"

    // echart 随窗口 自适应大小
    for(j=0; j<mycharts_id.length; j++){
        var t_echart = echarts.init(document.getElementById(mycharts_id[j]));
        myCharts.push(t_echart)
    }
    $(window).resize(function () {
        for (j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }
    })
    return myCharts;
}

layui.use(['layer', 'jquery',"table", "laydate", "element"], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    element.init();

    // 自定义变量
    var myCharts = init_echarts($);

    // 设置记账本下拉框
     function init_checkbook(result) {
     resultData = result;
         var parent_html = $("#toolbarDemo").html();
         var htmls =""
     for(var x=0; x<resultData.length; x++){
             var htmls = '<option value = "' + resultData[x].checkbook_id + '">' + resultData[x].checkbook_name + '</option>';
             if(x==0){
                 checkbook_id = resultData[x].checkbook_id
             };
     };
         parent_html = parent_html.replace("checkbook_selector_replace",htmls);
         $("#toolbarDemo")[0].innerHTML = parent_html;
   };
    init_checkbook(checkbook_list_json)

    // 初始化明细表
   detail_tableIns =  table.render({
      elem: '#detail-table'
      ,toolbar: '#toolbarDemo'
      ,id:"detail-table-id"
      ,page: true
      ,cols: [[
          {type:'radio',fixed: 'left'}
          ,{field:'date', width:110, title: '日期', sort: true, fixed: 'left'}
          ,{field:'category',width:80, title: '类别', sort: true}
          ,{field:'money', width:80, title: '金额', sort: true}
          ,{field:'remark', title: '备注'}
          ,{field:'isCash', width:150, title: '现金/信用卡', sort: true,}
          ,{field:'type', width:150, title: '收入/支出/流入/流出', sort: true,}
          ,{field:'checkbook_name', width:150, title: '所属记账本', sort: true, }
          ,{field:'account_name', width:150, title: '所属账户', sort: true}
          ,{field:'seconds_account_name', width:150, title: '所属子账户', sort: true}
          ,{field:'updater', width:80, title: '记录着', sort: true, }
          ,{fixed:'right', width:200, title: '操作',toolbar: '#OperaTools'}
        ]]
        ,data:[]
    });

    // 月份选择器
    laydate.render({
        elem: document.getElementById('month_selector')
        ,type: 'month'
        ,value: getNowMonth()
    });

    // 默认记账本id
   checkbook_id;

    //[收入/支出/流入/流出] tab 切换监听
    element.on('tab(test)',function (data) {
        for (j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }
        var mtype=null
        var checkbook_id = $("#checkbook_selector option:selected").val();
        var month_str = $("#month_selector").val();
        switch(data.index){
            case 0 :
                mtype = "收入"
                break;
            case 1 :
                mtype = "支出"
                break;
            case 2 :
                mtype = "流入"
                break
            case 3 :
                mtype = "流出"
                break
        }
        table.reload("detail-table-id",{
              url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
              ,where: {
                  "type":mtype,
            }
            ,done:function (res, curr, count) {
                this.where={};
            }
        });

         $("#month_selector").val(month_str)

    });

    function look_details(){
        var checkbook_id = $("#checkbook_selector option:selected").val();
        var month_str = $("#month_selector").val();

        //填写pie图
        $.ajax({
        url:"/api/v1/detailsum?checkbook_id="+checkbook_id+"&month_str="+month_str,
        type:'GET',
        dataType:'json',
        async:false,
        success:function(json){ // http code 200
            function callback1_factory(mtype){
                return function call_back_1(params) {
                    if (params.componentType === 'series') {
                        // 明细表重载
                        var category = params.name;
                        table.reload("detail-table-id",{
                              url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
                              ,where: {
                                  "type":mtype,
                                "category":category,
                            }
                            ,done:function (res, curr, count) {
                                this.where={};
                            }
                        });
                        // 月份选择器
                        laydate.render({
                            elem: document.getElementById('month_selector')
                            ,type: 'month'
                            ,value: month_str
                        });
                    }
            }
            }

            function callback2_factory(mtype){
                return function call_back_2(params) {
                    if (params.componentType === 'series') {
                        // 明细表重载
                        var account_name = params.name;
                        table.reload("detail-table-id",{
                              url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
                              ,where: {
                                  "type":mtype,
                                   "account_name":account_name,
                            },done:function (res, curr, count) {
                                this.where={};
                            }
                        });
                        // 月份选择器
                        laydate.render({
                            elem: document.getElementById('month_selector')
                            ,type: 'month'
                            ,value: month_str
                        });
                    }
                }
            }

            json = json.data

            var mytype= ["收入","收入","支出","支出","流入","流入","流出","流出"]
            var json_names = ["income_category","income_account",
                "spent_category","spent_account",
                "inflow_category","inflow_account",
                "outflow_category","outflow_account"]
            for(j=0;j<myCharts.length;j+=2){
                init_pie1(myCharts[j], json[json_names[j]], callback=callback1_factory(mytype[j]))
                init_pie2(myCharts[j+1], json[json_names[j+1]], callback=callback2_factory(mytype[j+1]))
            };
        }
        })

        //更新表格
        table.reload("detail-table-id",{
              url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
              ,where: { }
        })

        // 月份选择器
        laydate.render({
        elem: document.getElementById('month_selector')
        ,type: 'month'
        ,value: month_str
        });
    }

    function add_details(){
        layer.open({
             type: 2,
             content: 'detail_add',
             area: ['500px', '700px'],
             end: function () {
                look_details();
             }
         });
    }

    function delete_detail(data,obj){
        confirm_text = '真的删除如下明细么？<br/>';
        confirm_text += '【'+data.type+ "-"+data.category+ "-"+data.remark+ "-"+data.money+'元】<br/>';
        try{
            var combine_list = eval('(' + data.combine_details + ')')
            for(var i=0;i< combine_list.length;i++){
             var detail_id = combine_list[i]
             $.ajax({
                url:"/api/v1/detail?detail_id="+detail_id,
                type:'GET',
                dataType:'json',
                 async:false,
                success:function(json){ // http code 200
                    json = json.data
                    confirm_text += '【'+json["type"]+ "-"+json["category"]+ "-"+json["money"]+'元】<br/>';
                },
            })
            }
        }catch(err){};
        layer.confirm(confirm_text, function(index){
            // 同步服务器删除 记账本
            $.ajax({
                url:"/api/v1/detail?detail_id="+data.detail_id,
                type:'DELETE',
                dataType:'json',
                success:function(){ // http code 200
                    obj.del();
                    layer.close(index);
                    look_details();
                    parent.layer.msg('删除成功!!');
                },
                error:function(XMLHttpRequest, textStatus, errorThrown){
                   parent.layer.msg('删除失败!!');
                }
            })

        });
    }

    function edit_detail(data){
        layer.open({
             type: 2,
             content: 'detail_add?detail_id='+data.detail_id,
             area: ['500px', '700px'],
             end: function () {
                 console.log("end_edit")
                look_details();
             }
         });
    }
    //头工具栏事件
    table.on('toolbar(detail-table)', function(obj){
        var checkStatus = table.checkStatus(obj.config.id);
        switch(obj.event){
          case 'look-details':
              look_details();
              break;
          case 'add-details':
              add_details();
          break;
        };
    });

    //监听行工具事件
    table.on('tool(detail-table)', function(obj){
        var data = obj.data;
        switch(obj.event){
             case 'delete':
                 delete_detail(data,obj);
                 break;
             case "edit":
                 edit_detail(data);
                 break
         }
    });

    // 点击“查看明细按钮”
    $("#look_details").trigger('click');
});