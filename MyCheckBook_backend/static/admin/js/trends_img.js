function init_bar(myChart, mdata){

     var options = {
            title: {
                        text: "净收入/现金净流入  走势图",
                        textStyle: {
                            color: "rgb(85, 85, 85)",
                            fontSize: 18,
                            fontStyle: "normal",
                            fontWeight: "normal"
                        }
                    },
            tooltip: {
                trigger: "axis"
            },
            legend: {
                data: ["利润", "现金净流入"],
                selectedMode: false,
            },
            xAxis: [
                {
                    type: "category",
                    data: mdata.xAxis
                }
            ],
            yAxis: [
                {
                    type: "value"
                }
            ],
            grid: {
                x2: 30,
                x: 50
            },
            series: [
                {
                    name: "利润",
                    type: "bar",
                    barMaxWidth: '50',
                    data: mdata.profit
                },
                {
                    name: "现金净流入",
                    type: "bar",
                    barMaxWidth: '50',
                    data: mdata.cashflow
                }
            ]
     }
     myChart.setOption(options)
}

function init_line_stack(myChart, mdata){

    var series = []
    for(j = 0; j < mdata.all_datas.length; j++) {
        var m_s = {
            name: mdata.all_datas[j].name,
            type: 'line',
            stack: '总量',
            areaStyle: {normal: {}},
            data: mdata.all_datas[j].data,
        }
        series.push(m_s)
    }

    var options = {
        title: {
            text: mdata.title
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:mdata.legend
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : mdata.xAxis
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : series
    };
    myChart.setOption(options)

}


layui.use(['layer','jquery'], function(){
    var layer 	= layui.layer;
    var $=layui.jquery;
    var myCharts = [] ;
    require.config({
        paths: {
            echarts: '../../static/admin/lib/echarts'
        }
    });
    require(
        [
            'echarts',
            'echarts/chart/bar',
            'echarts/chart/line',
            'echarts/chart/map'
        ],
        function (ec) {
            profile_sum_echart = ec.init(document.getElementById("profile_sum_echart"));
            income_category_echart = ec.init(document.getElementById("income_category_echart"));
            spent_category_echart = ec.init(document.getElementById("spent_category_echart"));
            inflow_category_echart = ec.init(document.getElementById("inflow_category_echart"));
            outflow_category_echart = ec.init(document.getElementById("outflow_category_echart"));
            assert_category_echart = ec.init(document.getElementById("assert_category_echart"));
            liability_category_echart = ec.init(document.getElementById("liability_category_echart"));
            myCharts.push(profile_sum_echart)
            myCharts.push(income_category_echart)
            myCharts.push(spent_category_echart)
            myCharts.push(inflow_category_echart)
            myCharts.push(outflow_category_echart)
            myCharts.push(assert_category_echart)
            myCharts.push(liability_category_echart)

            //TOOD 获得记账本id
            var checkbook_id="12dafds"
             $.get("/api/v1/trends/all/"+checkbook_id).done(function (data){
                 init_bar(profile_sum_echart, data.remain_income_trends)
                 init_line_stack(spent_category_echart,data.spent_category_trends )
                 init_line_stack(income_category_echart,data.income_category_trends )
                 init_line_stack(inflow_category_echart,data.inflow_category_trends )
                 init_line_stack(outflow_category_echart,data.outflow_category_trends )
                 init_line_stack(assert_category_echart,data.asset_category_trends )
                 init_line_stack(liability_category_echart,data.liability_category_trends )
             })
        }
    );
    $(window).resize(function(){
        for(j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }

    })
});