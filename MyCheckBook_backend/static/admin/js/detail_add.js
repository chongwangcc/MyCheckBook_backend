function checknum(obj){
    if(/^\d+\.?\d{0,2}$/.test(obj.value)){
    obj.value = obj.value;
    }else{
    obj.value = obj.value.substring(0,obj.value.length-1);
    }
}

function isArray(o){
    return Object.prototype.toString.call(o)=='[object Array]';
}

function initSelector($,s_id, default_value, all_values){
    var old_selected_type = $("#"+s_id).val();
    $("#"+s_id).empty();
    for(var v  in all_values) {
        if(isArray(all_values)){
            v = all_values[v];
        }else{}
        var htmls = '<option value = "' + v + '">' + v + '</option>';
        if(v==default_value || v==old_selected_type){
            var htmls = '<option selected="selected" value = "' + v + '">' + v + '</option>';
        };
        $("#"+s_id).append(htmls);
    }
}

function initRadio($, name, default_cash, all_values){
    var default_select = null;
    var radios = document.getElementsByName("isCash");
    for (i=0; i<radios.length; i++) {
        if (radios[i].checked) {
            default_select = radios[i].value
        }
    }
    $("#detail_iscash").empty();
    for(var i=0; i<all_values.length;i++){
        var title = all_values[i];
        var htmls = '<input type="radio" name="isCash" value="'+title+'" title="'+title+'" id="isCash_'+title+'" checked="">';
        $("#detail_iscash").append(htmls)
    };
    if(default_select!=null){
        $("#isCash_"+default_select).prop("checked", true);
    }
    if(default_cash!=null){
        $("#isCash_"+default_cash).prop("checked", true);
    }
}

//记账本 selector 填充
function initCheckbookSelector($, checkbook_fulls_json){
    for (var prop in checkbook_fulls_json) {
        t_id=checkbook_fulls_json[prop].checkbook_id;
        t_name=checkbook_fulls_json[prop].checkbook_name;
        var htmls = '<option value = "' + t_id + '">' +t_name + '</option>';
        $("#checkbook_selector").append(htmls);
    };
}



layui.use(['form', 'jquery',"laydate"], function() {
    // 0. 初始化 layui 的一些模块
    var form = layui.form;
    var	layer = layui.layer;
    var	$ = layui.jquery;
    var laydate = layui.laydate;

    // 1. 自己使用的一些参数
    var form_method=JSON.stringify(detail_json).length>10 ?  "put":  "post"; ; // 判断事put操作还是post参数
    var selected_checkbook = null;

    function onChangeCheckbook(){

       var checkbook_id =  $("#checkbook_selector option:selected").val();
        var default_account = null;
        if(arguments.length==2){
            checkbook_id=default_checkbook_id;
            var default_account = arguments[1];
        }

        $("#checkbook_selector").val(checkbook_id);
        selected_checkbook = checkbook_fulls_json[checkbook_id];
        accounts_data = checkbook_fulls_json[checkbook_id].accounts;
        initSelector($,"detail_account_selector",default_account, accounts_data);

        form.render('select');
        form.render('radio');
    };

    function onChangeSelector(){
        var default_type =null;
        var default_category =null;
        var default_cash =null;
        if(arguments.length==3){
            var default_type = arguments[0] ? arguments[0] : null;
            var default_category = arguments[1] ? arguments[1] : null;
            var default_cash = arguments[2] ? arguments[2] : null;
        }

        // 明细类型
        var belong_account = $("#detail_account_selector option:selected").val();
        var type_tt = selected_checkbook.accounts[belong_account];
        initSelector($,"detail_type_selector",default_type, type_tt);

        //设置类别
         var selected_type = $("#detail_type_selector option:selected").val();
         var mmmCategory = selected_checkbook.category[selected_type];
         initSelector($,"detail_category_selector",default_category, mmmCategory);

        //是否现金设置
        var detail_tapo = $("#detail_type_selector option:selected").val();
        var isCash_value = selected_checkbook.accounts[belong_account][detail_tapo];
        initRadio($, "isCash",default_cash, isCash_value)

        //重新渲染表格
        form.render('select');
        form.render('radio');
    };

    //设置初始值，然后触发一下就行了
    function init(m_detail_json){
        initCheckbookSelector($,checkbook_fulls_json)
        //设置选中
        if(form_method=="put"){
            // 设置记账本选中
            // 设置所属账户
            onChangeCheckbook(default_checkbook_id=m_detail_json.checkbook_id,
                            default_account=m_detail_json.account_name);
            //设置明细类型
            // 设置类别
            // 设置是否现金
            onChangeSelector(default_type=m_detail_json.type,
                default_category=m_detail_json.category,
                default_cash=m_detail_json.isCash
                );
            //设置日期选中
            laydate.render({
                elem: document.getElementById('day_selector')
                ,value: m_detail_json.date
            });
            //设置金额
            $("#detail_money").val(m_detail_json.money);
            //设置备注
             $("#detail_remark").val(m_detail_json.remark);
             //设置id
            $("#detail_id").val(m_detail_json.detail_id)
        }else{
            onChangeCheckbook();
            onChangeSelector();
            laydate.render({
                elem: document.getElementById('day_selector')
                ,value: getNowDate()
            });
        }
        //记录者
        $("#detail_updater").attr("value",current_user_json["user_name"])

        //渲染
        form.on("select(checkbook_selector)", onChangeCheckbook)
        form.on("select(detail_account_selector)", onChangeSelector)
        form.on("select(detail_type_selector)", onChangeSelector)
        form.on("select(detail_category_selector)", onChangeSelector)
    };
    init(detail_json)

    // 提交表单获得
    form.on("submit(detailform)", function(data){

        function success(){
             parent.layer.closeAll();
             parent.layer.msg('添加明细成功');
        };
        function failed(){
            parent.layer.msg('添加明细失败');
        };

        // 修改一条明细
        if(form_method=="put"){
            $.ajax({
                url:"/api/v1/detail",
                method:"put",
                data:data.field,
                dataType:"JSON",
                async:"false",
                success:success,
                error:failed
            });
        }else if(form_method=="post"){
            // 新增一条明细
            $.ajax({
                url:"/api/v1/detail",
                method:"post",
                data:data.field,
                dataType:"JSON",
                async:"false",
                success:success,
                error:failed
            });
        }

    });
});