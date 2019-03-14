function checknum(obj){
    if(/^\d+\.?\d{0,2}$/.test(obj.value)){
    obj.value = obj.value;
    }else{
    obj.value = obj.value.substring(0,obj.value.length-1);
    }
}

layui.use(['form', 'jquery',"laydate"], function() {
    // 0. 初始化 layui 的一些模块
    var form = layui.form;
    var	layer = layui.layer;
    var	$ = layui.jquery;
    var laydate = layui.laydate;

    // 1. 自己使用的一些参数
    var form_method=JSON.stringify(detail_json).length>10 ?  "put":  "post"; ; // 判断事put操作还是post参数
    var selected_checkbook_full = null;

    checkbook_full = null;


    //记账本 selector 填充
    for (var prop in checkbook_fulls_json) {
        t_id=checkbook_fulls_json[prop].checkbook_id;
        t_name=checkbook_fulls_json[prop].checkbook_name;
        var htmls = '<option value = "' + t_id + '">' +t_name + '</option>';
        $("#checkbook_selector").append(htmls);
    };
    //所属账户填充
    function checkbookChange(){
        var default_checkbook_id = arguments[0] ? arguments[0] : null;
        var default_account = arguments[0] ? arguments[0] : null;

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

    function ChangeSeletor(){
        var default_type = arguments[0] ? arguments[0] : null;
        var default_category = arguments[0] ? arguments[0] : null;
        var default_cash = arguments[0] ? arguments[0] : null;
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
            aydate.render({
                elem: document.getElementById('day_selector')
                ,value: $("#day_selector").val(m_detail_json.date)
            });

            //设置金额
            $("#detail_money").val(m_detail_json.money)

            //设置备注
             $("#detail_remark").val(m_detail_json.remark)
        }else{
            checkbookChange();
            ChangeSeletor();
            laydate.render({
                elem: document.getElementById('day_selector')
                ,value: getNowDate()
            });

        }
    };
    init(detail_json)
     $("#detail_id").val(detail_json.detail_id)
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