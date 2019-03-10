layui.use(['layer', 'jquery',"table", "laydate", "element"], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    element.init();
    var now = new Date();

    var checkbook_id = "12dafds"
    var month_str=now.getFullYear() + '-' + lay.digit(now.getMonth() + 1)
function init_pie1(mychart, mdata, type) {
    var myoption = {
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'horizontal',
            bottom: '0%',
            data: mdata.legend
        },
        series: [
            {
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '25%'],
            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: [
                {value: mdata.sumValue, name: mdata.sumType, selected: false},
            ]
            },
            {
                type: 'pie',
                radius: ['35%', '60%'],
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
                data: mdata.data
            }]
    };
    mychart.setOption(myoption)

    mychart.on('click', function (params) {
        if (params.componentType === 'series') {
            // 明细表重载
            var category = params.name
            table.reload("detail-table-id",{
                  url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
                  ,where: {
                      "type":type,
                       "category":category,
                }
            })
        }
    });
}

function init_pie2(mychart, mdata, type){
    var myoption = {
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'horizontal',
            bottom: '0%',
            data: mdata.legend
        },
        center: ["50%", "100%"],
        series: [
            {
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '20%'],
            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: [
                {value: mdata.sumValue, name: mdata.sumType, selected: false},
            ]
            },
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

    mychart.on('click', function (params) {
        if (params.componentType === 'series') {
            // 明细表重载
            var account_name = params.name
            table.reload("detail-table-id",{
                  url: "/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
                  ,where: {
                      "type":type,
                       "account_name":account_name,
                }
            })
        }
    });
}



    // 自定义变量
    var myCharts = [];
    income_category_echart = echarts.init(document.getElementById("income_category_echart"));
    income_account_echart = echarts.init(document.getElementById("income_account_echart"));
    spent_category_echart = echarts.init(document.getElementById("spent_category_echart"));
    spent_account_echart = echarts.init(document.getElementById("spent_account_echart"));
    inflow_category_echart = echarts.init(document.getElementById("inflow_category_echart"));
    inflow_account_echart = echarts.init(document.getElementById("inflow_account_echart"));
    outflow_category_echart = echarts.init(document.getElementById("outflow_category_echart"));
    outflow_account_echart = echarts.init(document.getElementById("outflow_account_echart"));
    myCharts.push(income_category_echart);
    myCharts.push(income_account_echart);
    myCharts.push(spent_category_echart);
    myCharts.push(spent_account_echart);
    myCharts.push(inflow_category_echart);
    myCharts.push(inflow_account_echart);
    myCharts.push(outflow_category_echart);
    myCharts.push(outflow_account_echart);

    //TODO 得记账本id


    // 初始化明细表
    table.render({
      elem: '#detail-table'
      ,toolbar: '#toolbarDemo'
      ,id:"detail-table-id"
      ,page: true
      ,url:"/api/v1/details?checkbook_id="+checkbook_id+"&month_str="+month_str
      ,cols: [[
          {type:'radio',fixed: 'left'}
          ,{field:'date', width:100, title: '日期', sort: true, fixed: 'left'}
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
    });

    // 月份选择器
    laydate.render({
        elem: document.getElementById('month_selector')
        ,type: 'month'
        ,value: month_str
    });

    // //填写pie图
    $.ajax({
        url:"/api/v1/detailsum?checkbook_id="+checkbook_id+"&month_str="+month_str,
        type:'GET',
        dataType:'json',
        async:false,
        success:function(json){ // http code 200
            init_pie1(income_category_echart, json["income_category"], type="收入")
            init_pie2(income_account_echart, json["income_account"], type="收入")
            init_pie1(spent_category_echart, json["spent_category"], type="支出")
            init_pie2(spent_account_echart, json["spent_account"], type="支出")
            init_pie1(inflow_category_echart, json["inflow_category"], type="流入")
            init_pie2(inflow_account_echart, json["inflow_account"], type="流入")
            init_pie1(outflow_category_echart, json["outflow_category"], type="流出")
            init_pie2(outflow_account_echart, json["outflow_account"], type="流出")


        }
    })

    //tab切换监听
    element.on('tab(test)',function (data) {
        switch(data.index){
            case 0 :
                income_category_echart.resize();
                income_account_echart.resize()
                break
            case 1 :
                spent_category_echart.resize();
                spent_account_echart.resize()
                break
            case 2 :
                inflow_category_echart.resize();
                inflow_account_echart.resize()
                break
            case 3 :
                outflow_category_echart.resize();
                outflow_account_echart.resize()
                break
        }
    });

    $(window).resize(function () {
        for (j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }

    })

});