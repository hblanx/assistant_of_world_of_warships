imageType = 1 //1、落弹时间，2、速度和距离，3、目标夹角

$().ready(function(){
    flushImg(1,0,0);
});
function flushImg(imageType,incr,toward){
        //和后台做交互              
        var postUrl="/radar/fitWindows/fit"
        var data = {
            "type":imageType,
            "incr":incr,
            "toward":toward
        }

        $.ajax({
            url: postUrl,
            type: 'get',
            data: data,
            //dataType: "JSON",
            success: function (data) {
                //$("#bigword").html(data.word[0]);
                $("#windowsImg").attr("src", "data:image/jpeg;base64,"+data);
            }
        });
}
$(function(){
    $('#btnUp').click(function(){
        flushImg(imageType,$("#speedRange").val(),1);
    })
    $('#btnLeft').click(function(){
        flushImg(imageType,$("#speedRange").val(),0);
    })
    $('#btnDown').click(function(){
        flushImg(imageType,$("#speedRange").val(),3);
    })
    $('#btnRight').click(function(){
        flushImg(imageType,$("#speedRange").val(),2);
    })
    $('#btnImgType1').click(function(){
        imageType = 1
        flushImg(imageType,0,0);
    })
    $('#btnImgType2').click(function(){
        imageType = 2
        flushImg(imageType,0,0);
    })
    $('#btnImgType3').click(function(){
        imageType = 3
        flushImg(imageType,0,0);
    })
})
function showNum() {
    $("#inputText").html("移动的像素大小:"+$("#speedRange").val())
}