var newhtml = ""
var requesting = 0

$(function(){
    $('.getInfoBtn').click(function(){       
        if(requesting==1){
            return;
        } else{
            requesting=1;
        }
        var getUrl="getRadarInfo"
        newhtml = "";
        $('.getInfoBtn').html("等待响应")
        console.log("debug,click!")
        
        $.ajax({
            url: getUrl,
            type: 'get',
            dataType: "JSON",
            success: function (data) {
                console.log(data)
                $('.getInfoBtn').html("刷新信息")
                if(data.len>1){
                    newhtml = '<li class="list-group-item list-group-item-danger"><span class="badge">'
                    +data.list[0][1]+'</span>'+data.list[0][0]+'</li>'
                    for(var ri=1;ri<data.len;ri++){
                        newhtml += '<li class="list-group-item list-group-item-info"><span class="badge">'
                        +data.list[ri][1]+'</span>'+data.list[ri][0]+'</li>'
                    }
                }else{
                    newhtml = '<li class="list-group-item list-group-item-danger"><span class="badge">'
                    +data.list[0][1]+'</span>'+data.list[0][0]+'</li>'
                }
                $('.list-group').html(newhtml)
            },
            complete:function(){
                $('.getInfoBtn').prop("disable",false);
                requesting=0;
            }
        });
    })
})
