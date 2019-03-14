function checknum(obj)
{
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
    var isCash="现金";

    // 日期选择器
    var now = new Date();
    laydate.render({
        elem: document.getElementById('day_selector')
        ,value: now.getFullYear() + '-' + lay.digit(now.getMonth() + 1)+ '-'+ lay.digit(now.getDay() + 1)
    });

    //记账本 selector 填充
    $.ajax({
     url: "/api/v1/checkbooks",
     type: "get",
     dataType : "json",
     contentType : "application/json",
     async: false,//这得注意是同步
     success: function (result) {
         resultData = result.data;
             $("#checkbook_selector").append(htmls);
         for(var x=0; x<resultData.length; x++){
                 var htmls = '<option value = "' + resultData[x].checkbook_id + '">' + resultData[x].checkbook_name + '</option>';
                 $("#checkbook_selector").append(htmls)
         };
        }
   });

    //所属账户填充
    var checkbook_id =  $("#checkbook_selector option:selected").val();
    var checkbook_full = null;

    function checkbookChange(){
        $.ajax({
         url: "/api/v1/checkbook?checkbook_id="+checkbook_id,
         type: "get",
         dataType : "json",
         contentType : "application/json",
         async: false,//这得注意是同步
         success: function (result) {
                    checkbook_full = result;
                    accounts_data = result.accounts;
                    for(var prop  in accounts_data) {
                        var htmls = '<option value = "' + prop + '">' + prop + '</option>';
                        $("#detail_account_selector").append(htmls);
                    }
            }
       });
    };

    function ChangeSeletor(){
        // 明细类型
        var belong_account = $("#detail_account_selector option:selected").val();
        var type_tt = checkbook_full.accounts[belong_account];
        var old = $("#detail_type_selector option:selected").val();
        $("#detail_type_selector").empty();
        for(var prop  in type_tt) {
             var htmls = '<option value = "' + prop + '">' + prop + '</option>';
             if(prop == old){
                 htmls = '<option selected="selected"  value = "' + prop + '">' + prop + '</option>';
             };
            $("#detail_type_selector").append(htmls)
        };

        //是否现金设置
        var detail_tapo = $("#detail_type_selector option:selected").val();
        var isCash_value = checkbook_full.accounts[belong_account][detail_tapo];
        $("#detail_iscash").empty()
        for(var i=0; i<isCash_value.length;i++){
            var title = isCash_value[i];
            var htmls = '<input type="radio" name="isCash" value="'+title+'" title="'+title+'" checked="">';
            $("#detail_iscash").append(htmls);
        };

        //设置类别
         var selected_type = $("#detail_type_selector option:selected").val();
         var mmmCategory = checkbook_full.category[selected_type];
         $("#detail_category_selector").empty()
         for(var prop  in mmmCategory) {
             var htmls = '<option value = "' + mmmCategory[prop] + '">' + mmmCategory[prop] + '</option>';
            $("#detail_category_selector").append(htmls)
        };
        form.render('select');
        form.render('radio');
    };

    checkbookChange();
    ChangeSeletor()

    //记录者
    $.ajax({
     url: "/api/v1/user",
     type: "get",
     dataType : "json",
     contentType : "application/json",
     async: false,//这得注意是同步
     success: function (result) {
             $("#detail_updater").attr("value",result["user_name"])
        }
   });


    form.on("select(checkbook_selector)", checkbookChange)
    form.on("select(detail_account_selector)", ChangeSeletor)
    form.on("select(detail_type_selector)", ChangeSeletor)
    form.on("select(detail_category_selector)", ChangeSeletor)

    // 提交表单获得
    form.on("submit(detailform)", function(data){
        jsondata = $("#detail_json").val();
        console.log(jsondata);
        $.ajax({
            url:"/api/v1/detail",
            method:"post",
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