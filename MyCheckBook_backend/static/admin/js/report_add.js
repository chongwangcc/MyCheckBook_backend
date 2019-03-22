layui.config({
    debug: true
    ,base: '../../static/admin/layui/extend/'
}).extend({
    steps:"steps/steps"
});




layui.use(['layer', 'jquery',"table", "laydate", "element", "form",'steps'], function () {
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    var form = layui.form;
    var $ = layui.$;
    var title_list = ["填写基本信息",
        "同步明细数据",
        "资产负债清查",
        "检查财报内容",
         "审计师总结",
         "完成",
    ]

    // 初始化变量

    var base_info = {};
    var assets_appendix = {}
    var report_content = {}
    var audit_info = {}

    // 上一步，下一步按钮点击
    var now_step = 0;
    var $step= $("#step_demo").step();
    $("#preBtn").click(function(event) {
        $step.preStep();//上一步
        now_step = now_step -1;
        if(now_step<0){
            now_step = 0;
        }
        init_card(now_step);
    });
    $("#nextBtn").click(function(event) {
        $step.nextStep();//下一步
        now_step = now_step +1;
        if(now_step>=title_list.length){
            now_step = title_list.length-1;
        };
        init_card(now_step);
    });

    //初始化web界面
    function init_card(step_nums){
        $("#card_title").text(title_list[step_nums]);
        var card_id = "card" + step_nums;
        $("#card_content").html($("#"+card_id).html())
    }
    init_card(now_step);

})