layui.config({
    debug: true
    ,base: '../../static/admin/layui/extend/'
}).extend({
    steps:"steps/steps"
});




layui.use(['jquery','steps'], function () {
    // var layer = layui.layer;
    // var table = layui.table;
    // var laydate = layui.laydate;
    // var $ = layui.jquery;
    // var element = layui.element;
    // var form = layui.form;
 var $ = layui.$;

    var $step= $("#step_demo").step();
    //
    $("#preBtn").click(function(event) {
        $step.preStep();//上一步
    });
    $("#nextBtn").click(function(event) {
        $step.nextStep();//下一步
    });
    $("#goBtn").click(function(event) {
        $step.goStep(3);//到指定步
    });

})