layui.use(['layer', 'jquery',"table", "laydate", "element", "form"], function (){
    var layer = layui.layer;
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = layui.jquery;
    var element = layui.element;
    var form = layui.form;

    // 月份选择器
    laydate.render({
        elem: document.getElementById('month_selector')
        ,type: 'month'
        ,value: getNowMonth()
    });

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
    init_checkbook(checkbook_list_json)

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
        var checkbook_id = $("#checkbook_selector option:selected").val();
        var month_str = $("#month_selector").val();
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
    init_tab()
    $("#save_assets").click(function () {
        var checkbook_id = $("#checkbook_selector option:selected").val();
        var month_str = $("#month_selector").val();
        layer.msg(checkbook_id)
        layer.msg(month_str)

        var data = {
            "checkbook_id":checkbook_id,
            "month_str":month_str,
            "action":"all",
            "data":[]
        }
        for(var i in appendix_names){
            var t_name = appendix_names[i]
            all_data = table.cache[t_name+"_appendix_table"];
            data.data.push({
                name:t_name,
                data:all_data
            })
        }
        data.data = JSON.stringify(data.data)
        $.ajax({
            url:"/api/v1/assets",
            type:'POST',
            dataType:'json',
            data:JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            async:false,
            success:function(json){ // http code 200
                 parent.layer.closeAll();
                 parent.layer.msg('添加资产负债附表成功');
            }
        })
    });
})