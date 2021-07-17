var newhtml = ""
var requesting = 0

$(function(){
    $('.getInfoBtn').click(function(){       
        if(requesting==1){
            return;
        } else{
            requesting=1;
        }
        var getUrl="getMapInfo"
        newhtml = "";
        $('.getInfoBtn').html("等待响应")
        //console.log("debug,click!")
        
        $.ajax({
            url: getUrl,
            type: 'get',
            dataType: "JSON",
            success: function (data) {
                console.log(data)
                if(data.state == 1){
                    $("#mapImg").attr("src", data.path);
                    $('.getInfoBtn').html("刷新信息")
                }else{
                    $('.getInfoBtn').html("查询无结果")
                }
            },
            complete:function(){
                $('.getInfoBtn').prop("disable",false);
                requesting=0;
            }
        });
    })
})
