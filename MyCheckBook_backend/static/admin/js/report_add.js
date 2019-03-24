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
        // end_card(now_step);
        now_step = now_step -1;
        if(now_step<0){
            now_step = 0;
        }
        init_card(now_step);
        $step.preStep();//上一步
    });
    $("#nextBtn").click(function(event) {
        console.log("click next "+now_step)
        // end_card(now_step);
        now_step = now_step +1;
        if(now_step>=title_list.length){
            now_step = title_list.length-1;
        };
        init_card(now_step);
        $step.nextStep();//下一步
    });

    //初始化web界面
    function init_card(step_nums){
        $("#card_title").text(title_list[step_nums]);
        var card_id = "card" + step_nums;
        $("#card_content").html($("#"+card_id).html())

        switch(step_nums){
            case 0:
                init_checkbook(checkbook_list_json);
                laydate.render({
                    elem: '#date_range'
                    ,range: true
                });
                form.render();
                break;


            case 2:

                init_tab();
                break;
        }
    }
    init_card(now_step);

    //离开界面是触发，保存值
    function end_card(step_nums){
        console.log(step_nums)
         switch(step_nums) {
             case 0:
                 base_info["checkbook_id"] = $("#checkbook_selector option:selected").val();
                base_info["report_type"] = $("#report_type_selector option:selected").val();
                base_info["date_range"] = $("#date_range").text();
                base_info["name"] = $("#name").text();
                base_info["career"] = $("#career").text();
                console.log(base_info)
                 break;
             case 1:
                break;
             case 2:
                break;
             case 3:
                break;
             case 4:
                break;
             case 5:
                break;
         }
    }


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
            console.log(account_name)
            var oldData = table.cache[account_name+"_appendix_table"];
            console.log(oldData)
            old_cols =  myTables[account_name].config.cols
            var newRow = {};
            for(var c in old_cols){
                newRow[c] = ""
            };
            oldData.push(newRow);
            console.log(oldData)
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
    }
    function init_tab(){
        checkbook_id=1
        month_str = "2019-03"
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
                })
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
    }

})