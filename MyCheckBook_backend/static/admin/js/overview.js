var layer 	= layui.layer;
var $=layui.jquery;
//图表
var myChart;
var myoption;
//--- 折柱 ---
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
    }];

myoption = {
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
            data: data
        }]
    };
myChart = echarts.init(document.getElementById('chart'));
myChart.setOption(myoption);

window.onresize = function(){
    myChart.resize();
}