function init_pie(mychart, mdata){
    var myoption = {
        title: {
            text: '总支出',
            subtext: '20000',
            x: 'center',
            y: 'center',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 16
            }
        },
        tooltip: {
            show: true,
            trigger: 'item',
            formatter: "{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'horizontal',
            bottom: '0%',
            data: ['生活费', '零食', '购物', '运动', '娱乐']
        },
        series: [{
            type: 'pie',
            selectedMode: 'single',
            radius: ['25%', '58%'],
            color: ['#86D560', '#AF89D6', '#59ADF3', '#FF999A', '#FFCC67'],

            label: {
                normal: {
                    position: 'inner',
                    formatter: '{d}%',

                    textStyle: {
                        color: '#fff',
                        fontWeight: 'bold',
                        fontSize: 14
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: mdata
        }]
    };
    mychart.setOption(myoption)
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
            'echarts/chart/pie',
            'echarts/chart/line',
            'echarts/chart/map'
        ],
        function (ec) {
            income_echart = ec.init(document.getElementById("income_echart"));
            spend_echart = ec.init(document.getElementById("spend_echart"));
            myCharts.push(income_echart);
            myCharts.push(spend_echart);

            //TOOD 获得记账本id
            var checkbook_id="12dafds"

            // 填写明细表单

            //填写pie图
            var data = [
            {
                value: 3661,
                name: '生活费'
            }, {
                value: 5713,
                name: '零食'
            }, {
                value: 9938,
                name: '购物'
            }, {
                value: 17623,
                name: '运动'
            }, {
                value: 3299,
                name: '娱乐'
            }
            ];
            init_pie(income_echart, data)
            init_pie(spend_echart, data)

        });
    $(window).resize(function(){
        for(j = 0; j < myCharts.length; j++) {
            myCharts[j].resize();
        }

    })
});