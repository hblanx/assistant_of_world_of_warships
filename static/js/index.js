var newhtml = ""
var requesting = 0

$(function(){
    $('.computeBtn').click(function(){       
        if(requesting==1){
            return;
        } else{
            requesting=1;
        }
        var getUrl="compute"
        newhtml = "";
        $('.computeBtn').html("等待计算")
        console.log("debug,click!")
        
        $.ajax({
            url: getUrl,
            type: 'get',
            dataType: "JSON",
            success: function (data) {
                console.log(data)
                $('.computeBtn').html(data.num)
            },
            complete:function(){
                $('.computeBtn').prop("disable",false);
                requesting=0;
            }
        });
    })
})
