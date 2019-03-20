function init_bar(assets_echarts, liability_echarts, account_name, account_sum){
    var max_nums = 0;
    var options1 =  {
         color: ['#00FF7F','#3CB371','#7FFF00'],
        legend: {
            data: []
        },
        grid: {
            right: '45',
        },
        xAxis:  {
            inverse: true,
            type: 'value'
        },
        yAxis: {
            type: 'category',
            position: 'right',
            data: ['总资产']
        },
        series: [ ]
    };
    var options2 =  {
        color: ['#FF4500','#FA8072','#BC8F8F'],
        legend: {
            data: []
        },
        grid: {
            left: '45',
        },
        xAxis:  {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: ['总负债']
        },
        series: []
    };

    function gen_data(option, type){
        var legend = [];
        var series = [];
        if(account_sum[type].now_sum>max_nums){
            max_nums = account_sum[type].now_sum;
        }
        for(var tt in account_sum[type].data){
            option.legend.data.push(account_sum[type].data[tt].name);
            option.series.push({
                name: account_sum[type].data[tt].name,
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: [account_sum[type].data[tt].now_sum]
            });
        }
    }

    gen_data(options1, "总资产");
    gen_data(options2, "总负债");

    options1.xAxis.max = max_nums;
    options2.xAxis.max = max_nums;

    assets_echarts.setOption(options1);
    liability_echarts.setOption(options2);
}

function gen_table_data(account_sum, type){
    var data = []
    for(var i in account_sum[type].data){
        data_1 = account_sum[type].data[i]
       data.push({
           "name":data_1["name"],
           "org_price":data_1["org_sum"],
           "now_price":data_1["now_sum"]
        });
        for(var j in data_1["data"]){
          data.push({
           "name":"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+data_1["data"][j]["name"],
           "org_price":data_1["data"][j]["org_sum"],
           "now_price":data_1["data"][j]["now_sum"]
            });
        }
    }
    return data
}

layui.use(['layer', 'jquery',"table", "laydate", "element", "form"], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    var form = layui.form;


    // 月份选择器
    laydate.render({
        elem: document.getElementById('month_selector')
        ,type: 'month'
        ,value: getNowMonth()
    });

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

    // 根据json串，初始化上下两个Tab
    var myCharts = []
    var myTables = []
    function init_sum_tab(account_name, account_sum){
        //1. 更新html

        // 2. 更新数据
        // var t_echart1 = echarts.init(document.getElementById(account_name+"_assets_total_echarts"));
        // var t_echart2 = echarts.init(document.getElementById(account_name+"_liability_total_echarts"));
        var t_echart1 =  echarts.init($("#"+account_name+"_assets_total_echarts")[0])
        var t_echart2 =  echarts.init($("#"+account_name+"_liability_total_echarts")[0])

        myCharts.push(t_echart1);
        myCharts.push(t_echart2);
        init_bar(t_echart1,t_echart2,account_name,account_sum);
        tableins = table.render({
              elem: '#'+account_name+'_assets-sum'
              ,page: false
              ,cols: [[
                  {field:'name',title: '总资产' }
                  ,{field:'org_price', title: '原价 '+account_sum["总资产"].org_sum+'元' }
                  ,{field:'now_price', title: '现价 '+account_sum["总资产"].now_sum+'元'}
                ]]
                ,data:gen_table_data(account_sum,"总资产")
            });
        myTables.push(tableins);
        tableins = table.render({
          elem: '#'+account_name+'_liability-sum'
          ,page: false
          ,cols: [[
              {field:'name',title: '总负债'}
              ,{field:'org_price', title: '原价 '+ account_sum["总负债"].org_sum + '元'}
              ,{field:'now_price', title: '现价 '+ account_sum["总负债"].now_sum + '元'}
            ]]
            ,data:gen_table_data(account_sum, "总负债")
        });
        myTables.push(tableins)
    };

    function init_appendix_tab(account_name, account_sum){

        var cols = [];
        var data = [];
        for(var col in account_sum.columns){
            col = account_sum.columns[col]
            cols.push({field:col,title: col, edit: 'text' })
        };
        for(var i=0; i< account_sum.rows.length; i++){
            var t_data = {}
            for(var col in account_sum.columns){
                col = account_sum.columns[col]
                t_data[col] = account_sum.content[col][i]
            }
            data.push(t_data)
        }
        tableIns = table.render({
              elem: '#'+account_name+'_appendix_table'
              ,page: false
              ,limit:100
              ,cols: [cols]
              ,data:data
            });
        myTables[account_name] = tableIns;

        $(document).on('click','#'+account_name+'_add_row',function(){
            var oldData = table.cache[account_name+"_appendix_table"];
            old_cols =  myTables[account_name].config.cols
            var newRow = {};
            for(var c in old_cols){
                newRow[c] = ""
            };
            oldData.push(newRow);
            myTables[account_name].reload({
                data : oldData
            });
         });
        $(document).on('click','#'+account_name+'_add_col',function(){
             // 弹出对话框设置列名
            layer.prompt({
                formType:0,
                title:"请输入列名",
            }, function(value, index, elem){
                // 重新渲染表格
                var oldData = table.cache[account_name+"_appendix_table"];
                old_cols =  myTables[account_name].config.cols;
                var new_cols = {field:value, title:value, edit: 'text' };
                old_cols[0].push(new_cols);
                tableIns = table.render({
                    elem: '#'+account_name+'_appendix_table'
                    ,page: false
                    ,cols: old_cols
                    ,limit:100
                    ,data:oldData
                });
                myTables[account_name] = tableIns;

                //关闭窗口
                layer.close(index);
            });
         });

        //TODO 保存表格数据到后台
        $(document).on('click','#'+account_name+'_save',function(){
             var month_str = $("#month_selector").val();
            layer.msg(account_name);
            all_data = table.cache[account_name+"_appendix_table"]
            console.log(all_data)
            $.ajax({
                url:"/api/v1/assets",
                type:'POST',
                dataType:'json',
                data: JSON.stringify({
                    "checkbook_id":checkbook_id,
                    "month_str":month_str,
                    "appendix":account_name,
                    "data":JSON.stringify(all_data)
                    }),
                contentType: "application/json; charset=utf-8",
                async:false,
                success:function(json){ // http code 200

                }
            })
        });
    }

    // JS 填充相关表格
    $(window).resize(function () {
        for (j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }
    });

    element.on('tab(test)',function (data) {
        for (j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        };
        for (j = 0; j < myTables.length; j++) {
            myTables[j].resize();
        };
    });

    $("#look-assets").click(function () {
        // 获得参数
        var checkbook_id = $("#checkbook_selector option:selected").val();
        var month_str = $("#month_selector").val();

        //调用json
        var assets_full_json = (function () {
            var result;
            $.ajax({
                url:"/api/v1/assets?checkbook_id="+checkbook_id+"&month_str="+month_str+"&action=ALL",
                type:'GET',
                dataType:'json',
                async:false,
                success:function(json){ // http code 200
                    result = json.data
                }
            })
            return result;
        })();
        console.log(assets_full_json)

        // 更新html
        $("#sum_tab_title").empty()
        $("#sum_tab_content").empty()
        $("#appendix_tab_title").empty()
        $("#appendix_tab_content").empty()

        for(var prop in assets_full_json["sum"]){
            if(prop === "合并账户"){
                $("#sum_tab_title").append("<li  class=\"layui-this\"> "+prop+"</li>");
            }else{
                $("#sum_tab_title").append("<li>"+prop+"</li>");
            }

           var parent_html = $("#sum_tab_content_script").html();
           parent_html = parent_html.replace(/account_name/g,prop);
           if(prop === "合并账户"){

           }else{
              parent_html = parent_html.replace("layui-show","");
           }
           $("#sum_tab_content").append(parent_html);
        }
        for(var prop in assets_full_json["appendix"]){
            var parent_html = $("#appendix_tab_content_script").html();
           parent_html = parent_html.replace(/account_name/g,prop);
            if(prop === "银行卡"){
                $("#appendix_tab_title").append("<li class=\"layui-this\">"+prop+"</li>");

           }else{
                $("#appendix_tab_title").append("<li>"+prop+"</li>");
               parent_html = parent_html.replace("layui-show","");
           }
           $("#appendix_tab_content").append(parent_html);
        }

        myCharts = []
        myTables = []
        for(var prop in assets_full_json["sum"]){
            var account_name = prop
            var account_sum = assets_full_json["sum"][account_name]
            init_sum_tab(account_name,account_sum)
        }
        for(var prop in assets_full_json["appendix"]){
            var account_name = prop;
            var account_sum = assets_full_json["appendix"][account_name];
           init_appendix_tab(account_name,account_sum);
        }
        element.render();

        console.log(document.body)
    });

    $("#look-assets").trigger('click');

    $("#add-assets").click(function () {
        layer.msg("hello")
    });



});