function checknum(obj){
    if(/^\d+\.?\d{0,2}$/.test(obj.value)){
    obj.value = obj.value;
    }else{
    obj.value = obj.value.substring(0,obj.value.length-1);
    }
}

layui.use(['form', 'jquery',"laydate"], function() {
    var form = layui.form;
    var	layer = layui.layer;
    var	$ = layui.jquery;
    var laydate = layui.laydate;
    form.render();
    var form_method="post";
    if(JSON.stringify(detail_json).length>10){
        $("#detail_id").val(detail_json.detail_id)
        form_method="put";
    }

    // 日期选择器

    Date.prototype.Format = function (fmt) { //author: meizz
        var o = {
            "M+": this.getMonth() + 1, //月份
            "d+": this.getDate(), //日
            "h+": this.getHours(), //小时
            "m+": this.getMinutes(), //分
            "s+": this.getSeconds(), //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds() //毫秒
        };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }
    checkbook_full = null;
    laydate.render({
        elem: document.getElementById('day_selector')
        ,value: new Date().Format("yyyy-MM-dd")
    });

    //记账本 selector 填充
    for(var x=0; x<checkbooks_json.length; x++){
        var htmls = '<option value = "' + checkbooks_json[x].checkbook_id + '">' + checkbooks_json[x].checkbook_name + '</option>';
        $("#checkbook_selector").append(htmls);
        //TODO 设置选中的记账本
    };
    //所属账户填充
    function checkbookChange(default_checkbook_id=null, default_account=null){
        var checkbook_id =  $("#checkbook_selector option:selected").val();
        if(default_checkbook_id!=null){
            checkbook_id=default_checkbook_id;
            $("#checkbook_selector").val(checkbook_id);

        }
        checkbook_full = checkbook_fulls_json[checkbook_id+""];
        accounts_data = checkbook_fulls_json[checkbook_id].accounts;
        for(var prop  in accounts_data) {
            var htmls = '<option value = "' + prop + '">' + prop + '</option>';
            if(prop==default_account){
                var htmls = '<option selected="selected" value = "' + prop + '">' + prop + '</option>';
            }
            $("#detail_account_selector").append(htmls);
        }

        form.render('select');
        form.render('radio');
    };

    function ChangeSeletor(default_type=null,
                           default_category=null,
                           default_cash=null){
        // 明细类型
        var belong_account = $("#detail_account_selector option:selected").val();
        var type_tt = checkbook_full.accounts[belong_account];
        var old_selected_type = $("#detail_type_selector option:selected").val();
        $("#detail_type_selector").empty();
        for(var prop  in type_tt) {
             var htmls = '<option value = "' + prop + '">' + prop + '</option>';
             if(prop == old_selected_type || prop == default_type){
                 htmls = '<option selected="selected"  value = "' + prop + '">' + prop + '</option>';
             };
            $("#detail_type_selector").append(htmls);
        };

        //是否现金设置
        var detail_tapo = $("#detail_type_selector option:selected").val();
        var isCash_value = checkbook_full.accounts[belong_account][detail_tapo];
        var default_select = null

        var radios = document.getElementsByName("isCash");
        for (i=0; i<radios.length; i++) {
            if (radios[i].checked) {
                default_select = radios[i].value
            }
        }
        console.log(default_select)

        $("#detail_iscash").empty();
        for(var i=0; i<isCash_value.length;i++){
            var title = isCash_value[i];
            var htmls = '<input type="radio" name="isCash" value="'+title+'" title="'+title+'" id="isCash_'+title+'" checked="">';
            $("#detail_iscash").append(htmls)
        };
        if(default_select!=null){
            $("#isCash_"+default_select).prop("checked", true);
        }
        if(default_cash!=null){
            $("#isCash_"+default_cash).prop("checked", true);
        }

        //设置类别
         var selected_type = $("#detail_type_selector option:selected").val();
         var mmmCategory = checkbook_full.category[selected_type];
         var old_selected_detail = $("#detail_category_selector option:selected").val();
         $("#detail_category_selector").empty()
         for(var prop  in mmmCategory) {
             var htmls = '<option value = "' + mmmCategory[prop] + '">' + mmmCategory[prop] + '</option>';
             if(prop == default_category || prop==old_selected_detail){
                 htmls = '<option selected="selected"  value = "' + prop + '">' + prop + '</option>';
             };
            $("#detail_category_selector").append(htmls);
        };
        form.render('select');
        form.render('radio');
    };

    //设置初始值，然后触发一下就行了
    function init(m_detail_json){
        //设置选中
        if(JSON.stringify(m_detail_json).length>10){
            // 设置记账本选中              //设置所属账户
            checkbookChange(default_checkbook_id=m_detail_json.checkbook_id,
                            default_account=m_detail_json.account_name)
            //设置明细类型              //设置类别             //设置是否现金
            ChangeSeletor(default_type=m_detail_json.type,
                default_category=m_detail_json.category,
                default_cash=m_detail_json.isCash
                )
            //设置日期选中
            $("#day_selector").val(m_detail_json.date)

            //设置金额
            $("#detail_money").val(m_detail_json.money)

            //设置备注
             $("#detail_remark").val(m_detail_json.remark)
        }else{
            checkbookChange();
            ChangeSeletor()
        }
    };
    init(detail_json)
    //记录者
    $("#detail_updater").attr("value",current_user_json["user_name"])

    form.on("select(checkbook_selector)", checkbookChange)
    form.on("select(detail_account_selector)", ChangeSeletor)
    form.on("select(detail_type_selector)", ChangeSeletor)
    form.on("select(detail_category_selector)", ChangeSeletor)

    // 提交表单获得
    form.on("submit(detailform)", function(data){
        jsondata = $("#detail_json").val();
        url = "/api/v1/detail";
        if(form_method=="PUT"){
            url+="?detail_id="+detail_json.detail_id;
        }
        $.ajax({
            url:url,
            method:form_method,
            data:data.field,
            dataType:"JSON",
            async:"false",
            success:function(){ // http code 200
                 parent.layer.closeAll();
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
               parent.layer.msg('添加明细失败');
            }
        });

    });
});