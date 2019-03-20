function init_bar(assets_echarts, liability_echarts, account_name, account_sum){
    var max_nums = 0;
    var options1 =  {
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
        if(account_sum[type].sum>max_nums){
            max_nums = account_sum[type].sum;
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
                data: [account_sum[type].data[tt].sum]
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

layui.use(['layer', 'jquery',"table", "laydate", "element"], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    element.init();
    // init 变量初始化

    // 自定义变量
    var checkbook_id = 1;
    var month_str = "2019-03"

    //调用json
    var assets_full_json = (function () {
        var result;
        $.ajax({
            url:"/api/v1/assets?checkbook_id="+checkbook_id+"&month_str="+month_str+"&action=ALL",
            type:'GET',
            dataType:'json',
            async:false,
            success:function(json){ // http code 200
                result = json
            }
        })
        return result;
    })();
    console.log(assets_full_json);

    // 根据json串，初始化上下两个Tab
    var myCharts = []
    var myTables = {}
    function init_sum_tab(account_name, account_sum){
        var t_echart1 = echarts.init(document.getElementById(account_name+"_assets_total_echarts"));
        var t_echart2 = echarts.init(document.getElementById(account_name+"_liability_total_echarts"));
        myCharts.push(t_echart1);
        myCharts.push(t_echart2);
        init_bar(t_echart1,t_echart2,account_name,account_sum);
        console.log(account_name)
        console.log(account_sum)
        table.render({
              elem: '#'+account_name+'_assets-sum'
              ,page: false
              ,cols: [[
                  {field:'name',title: '总资产' }
                  ,{field:'org_price', title: '原价 '+account_sum["总资产"].org_sum+'元' }
                  ,{field:'now_price', title: '现价 '+account_sum["总资产"].now_sum+'元'}
                ]]
                ,data:gen_table_data(account_sum,"总资产")
            });
        table.render({
          elem: '#'+account_name+'_liability-sum'
          ,page: false
          ,cols: [[
              {field:'name',title: '总负债'}
              ,{field:'org_price', title: '原价 '+ account_sum["总资产"].org_sum + '元'}
              ,{field:'now_price', title: '现价 '+ account_sum["总负债"].now_sum + '元'}
            ]]
            ,data:gen_table_data(account_sum, "总负债")
        });
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
        $(document).on('click','#'+account_name+'_save',function(){});
    }

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
        // for(var prop in assets_full_json["sum"]){
        //     var account_name = prop
        //     var account_sum = assets_full_json["sum"][account_name]
        //     init_sum_tab(account_name,account_sum)
        // }
    });


     console.log()
});