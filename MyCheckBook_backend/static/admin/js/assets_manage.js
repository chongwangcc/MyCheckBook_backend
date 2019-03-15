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
    function init_sum_tab(account_name, account_sum){
        return "<div class=\"layui-tab-item\"><label>"+account_name+"</label></div>";
    };

    function init_appendix_tab(account_name, account_sum){
        return "<div class=\"layui-tab-item\"><label>"+account_name+"</label></div>";
    };

    for(var prop in assets_full_json["sum"]){
        var account_name = prop
        var account_sum = assets_full_json["sum"][account_name]
        $("#sum_tab_title").append("<li>"+account_name+"</li>")
        $("#sum_tab_content").append(init_sum_tab(account_name, account_sum))
    }
    for(var prop in assets_full_json["appendix"]){
        var account_name = prop
        var account_sum = assets_full_json["appendix"][account_name]
        $("#appendix_tab_title").append("<li>"+account_name+"</li>")
        $("#appendix_tab_content").append(init_appendix_tab(account_name,account_sum))
    }










});