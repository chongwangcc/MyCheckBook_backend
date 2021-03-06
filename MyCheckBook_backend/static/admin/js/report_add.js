layui.config({
    debug: true
    ,base: '../../static/admin/layui/extend/'
}).extend({
    steps:"steps/steps"
});

function set_select_checked(selectId, checkValue){
    var select = document.getElementById(selectId);

    for (var i = 0; i < select.options.length; i++){
        if (select.options[i].value == checkValue){
            select.options[i].selected = true;
            break;
        }
    }
};

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
    ];

    // 初始化变量
    var base_info = {};
    var assets_appendix = []
    var report_content = {}
    var audit_info = {}

    // 上一步，下一步按钮点击
    var now_step = 0;
    var $step= $("#step_demo").step();
    $("#preBtn").click(function(event) {
        exit_card(now_step);
        now_step = now_step -1;
        if(now_step<0){
            now_step = 0;
        }
        enter_card(now_step);
        $step.preStep();//上一步
    });
    $("#nextBtn").click(function(event) {
        exit_card(now_step);
        now_step = now_step +1;
        if(now_step>title_list.length){
            now_step = title_list.length;
            //点击了完成按钮？
        };
        if(now_step == title_list.length){
            console.log("完成 click")
            // 把财报数据保存到后台
            mydata = {
                report_id:report_content["report_id"],
                "audit_info":audit_info
            }
            $.ajax({
                url:"/api/v1/report?"+"action=add_audit",
                type:'PUT',
                dataType:'json',
                data:{"data":JSON.stringify(mydata)},
                async:false,
                success:function(json){ // http code 200
                    result = json.data
                }
            });

            //关闭界面
             parent.layer.closeAll();
        }
        enter_card(now_step);
        $step.nextStep();//下一步
    });

    //初始化web界面, 保留之前的数据
    function enter_card(step_nums){
        $("#card_title").text(title_list[step_nums]);
        var card_id = "card" + step_nums;
        $("#card_content").html($("#"+card_id).html())
        $("#nextBtn").html("<i class=\"layui-icon\">&#xe602;</i>下一步");

        switch(step_nums){
            case 0:
                if(JSON.stringify(base_info) == '{}')
                {
                    init_checkbook(checkbook_list_json);
                    laydate.render({
                    elem: '#date_range'
                    ,range: true
                });
                    form.render();
                }
                else {
                    init_checkbook(checkbook_list_json);
                    laydate.render({
                        elem: '#date_range'
                        ,range: true
                        ,value: base_info["date_range"]
                    });
                    set_select_checked("checkbook_selector", base_info["checkbook_id"]);
                    set_select_checked("report_type_selector", base_info["report_type"]);
                    $("#person_name").val(base_info["person_name"]);
                    $("#career").val(base_info["career"]);
                    $("#report_name").val(base_info["report_name"]);
                    form.render();
                }
                break;
            case 1:
                break;
            case 2:
                if(JSON.stringify(assets_appendix) == '[]'){
                    init_tab();
                 }else{
                    init_tab_by_value(assets_appendix);
                }
                break;
            case 3:
                // 检查财报内容
                var mydata = {
                    base_info:base_info,
                    assets_appendix:assets_appendix,
                };
                report_content = (function () {
                    var result;
                    $.ajax({
                            url:"/api/v1/report?"+"action=gen_report",
                            type:'PUT',
                            dataType:'json',
                            data:{"data":JSON.stringify(mydata)},
                            async:false,
                            success:function(json){ // http code 200
                                result = json.data
                            }
                        });
                        return result;
                    })();
                $("#report_path").click(function(event) {
                    window.open(report_content["excel_path"]);
                });
                break;
            case 4:
                 if(JSON.stringify(audit_info) == '{}'){

                 }else{
                     $("#audit_name").val(audit_info["audio_name"]);
                     $("#suggestion").val(audit_info["audio_suggetions"]);
                 };
                 break;
            case 5:
            case 6:
            case 7:
                 $("#nextBtn").html("<i class=\"layui-icon\">&#xe605;</i>完成");
                 break;
        }
    };
    enter_card(now_step);

    //离开界面是触发，保存值
    function exit_card(step_nums){
         switch(step_nums) {
             case 0:
                base_info["checkbook_id"] = $("#checkbook_selector option:selected").val();
                base_info["report_type"] = $("#report_type_selector option:selected").val();
                base_info["date_range"] = $("#date_range").val();
                base_info["person_name"] = $("#person_name").val();
                base_info["career"] = $("#career").val();
                base_info["report_name"] = $("#report_name").val();
                break;
             case 1:
                break;
             case 2:
                 assets_appendix = []
                 for(var i in appendix_names){
                    var t_name = appendix_names[i]
                    var all_data = table.cache[t_name+"_appendix_table"];
                    assets_appendix.push({
                        "name":t_name,
                        "data":all_data
                    });
                }
                break;
             case 3:
                 // 检查财报内容


                break;
             case 4:
                 audit_info["audio_name"] = $("#audit_name").val();
                 audit_info["audio_suggetions"] = $("#suggestion").val();
                break;
             case 5:
                break;
         }
    };

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

    //添加 附表
    var myTables = [];
    var appendix_names = [];
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

            tableIns = table.render({
                    elem: '#'+account_name+'_appendix_table'
                    ,page: false
                    ,cols: old_cols
                    ,limit:100
                    ,data:oldData
            });
            myTables[account_name] = tableIns;
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
    };
    function init_tab(){
        var checkbook_id = base_info["checkbook_id"];
        var month_str=base_info["date_range"].substr(0,7);
        var assets_full_json = (function () {
                var result;
                $.ajax({
                    url:"/api/v1/assets?checkbook_id="+checkbook_id+"&month_str="+month_str+"&action=empty",
                    type:'GET',
                    dataType:'json',
                    async:false,
                    success:function(json){ // http code 200
                        console.log(json.data);
                        result = json.data
                    }
                });
                return result;
            })();

        $("#appendix_tab_title").empty()
        $("#appendix_tab_content").empty()
        for(var prop in assets_full_json["empty"]){
            appendix_names.push(prop)

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
        for(var prop in assets_full_json["empty"]){
            var account_name = prop;
            var account_sum = assets_full_json["empty"][account_name];
           init_appendix_tab(account_name,account_sum);
        }
    };
    function init_tab_by_value(table_values){
        $("#appendix_tab_title").empty()
        $("#appendix_tab_content").empty()
        for(var prop in table_values){
            prop = table_values[prop].name
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

        for(var prop in myTables){
            var account_name = prop;
            var table_temp = myTables[prop];
            var data = []
            for(var ii in table_values){
                if(table_values[ii].name==prop){
                    data = table_values[ii].data;
                    break;
                }
            }
            tableIns = table.render({
              elem: '#'+prop+'_appendix_table'
              ,page: false
              ,limit:100
              ,cols: table_temp.config.cols
              ,data:data
            });

        }
    };
})