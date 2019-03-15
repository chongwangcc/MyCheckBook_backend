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
    console.log(assets_full_json)

    // 根据json串，初始化上下两个Tab




});