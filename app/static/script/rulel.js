//refers from flask_chess on github by Kechi Zhang
var color = "";
function get_color(){
    $.get("/getColorl",function(rtnFromSvr){
        color = rtnFromSvr;
    })
}
function try_play(e){
    var xy = $(e).attr("id");
    var try_rst = '';
    console.log("try_play xy: "+xy);
    $.get("/play_chessl",{xy:xy},function(rtnFromSvr){
        console.log("try_play rtnFromSvr: "+rtnFromSvr);
        try_rst = rtnFromSvr;
        console.log("try_play rst: "+try_rst);
        console.log((new Date()).getTime());

        if (try_rst == '1') {
                $("#messageContent").append("");
                $("#"+$(e).attr("id")).html("<div class=\"chessman "+color+"\"></div>");
                play_rst = Chess.isEnd($(e).attr("id"),color)
                console.log("play_rst: "+play_rst);
                if (play_rst != 0) {
                    console.log("play_rst: "+play_rst);

                    $.get("/end_chessl",function(rtnFromSvr){
                        setTimeout('window.location.replace("/index");', 2000);

                    })
                }
            }
            else if (try_rst == '0') {
                $("#messageContent").append("");
            }
            else {
                $("#messageContent").append("");
            }
    })

}

setInterval("get_color()",1000);

var row = 15;
var col = 15;
var widthAndHeight = 30;//grid
var Chess = {
    isEnd:function(xy,chessmanColor){//end
        var end = 0;
        var id = parseInt(xy);
        // calculation of rows
        var num = 1;
        num = Chess.shujia(num,id,chessmanColor);
        num = Chess.shujian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("Game Over!");
                end = 1;
                console.log("end: "+end);
                return end;
            }else{
                confirm("Game Over!");
                end = 2;
                console.log("end: "+end);
                return end;
            }
        }
        num = 1;
        num = Chess.hengjia(num,id,chessmanColor);
        num = Chess.hengjian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("Game Over!");
                end = 1;
                console.log("end: "+end);
                return end;
            }else{
                confirm("Game Over!");
                end = 2;
                console.log("end: "+end);
                return end;
            }
        }
        num = 1;
        num = Chess.zuoxiejia(num,id,chessmanColor);
        num = Chess.zuoxiejian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("Game Over!");
                end = 1;
                console.log("end: "+end);
                return end;
            }else{
                confirm("Game Over!");
                end = 2;
                console.log("end: "+end);
                return end;
            }
        }
        num = 1;
        num = Chess.youxiejia(num,id,chessmanColor);
        num = Chess.youxiejian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("Game Over!");
                end = 1;
                console.log("end: "+end);
                return end;
            }else{
                confirm("Game Over!");
                end = 2;
                console.log("end: "+end);
                return end;
            }
        }
        return end;
    },youxiejia:function(num,id,color){
        var yu = id%row;
        id = id+(row-1);
        if(id<(row*col)&&(id%row)<yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.youxiejia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },youxiejian:function(num,id,color){
        var yu = id%row;
        id = id-(row-1);
        if(id>=0&&(id%row)>yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.youxiejian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },zuoxiejia:function(num,id,color){
        var yu = id%row;
        id = id+(row+1);
        if(id<(row*col)&&(id%row)>yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.zuoxiejia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },zuoxiejian:function(num,id,color){
        var yu = id%row;
        id = id-(row+1);
        if(id>=0&&(id%row)<yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.zuoxiejian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    hengjia:function(num,id,color){
        var yu = id%row;
        id = id+1;
        if(id<(row*col)&&(id%row)>yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.hengjia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }

    },
    hengjian:function(num,id,color){
        var yu = id%row;
        id = id-1;
        if(id>=0&(id%row)<yu){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.hengjian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    shujia:function(num,id,color){
        id = id+row;
        if(id<(row*col)){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.shujia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    shujian:function(num,id,color){
        id = id-row;
        if(id>=0){
            var flag = Chess.checkColor(id,color);
            if(flag){
                num++;
                return Chess.shujian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    checkColor:function(xy,color){
        if($("#"+xy).children("div").hasClass(color)){
            return true;
        }else {
            return false;
        }
    },
    playchess:function(e){
         console.log(e);
        if(color!=""){
            if($(e).children("div").length>0){
                alert("It is occupied! Please choose other places!");
                return;
            }
            console.log($(e).attr("id"));

            try_play(e);
            console.log((new Date()).getTime());


        }else{
            $("#messageContent").append("");
            $("#messageContent").append("\n");
            $("#messageContent").scrollTop($("#messageContent")[0].scrollHeight - $("#messageContent").height());
        }

    },

};
$(function(){

    $("#background").css({width:(row*widthAndHeight)+"px",height:(col*widthAndHeight)+"px"});
    //canvas draw
    var canvas = document.createElement("canvas");

$(canvas).attr({width:(row*widthAndHeight)+"px",height:col*widthAndHeight+"px"});
$(canvas).css({position:"relative","z-index":9999});
var cot = canvas.getContext("2d");
cot.fillStyle = "#EAC000";
cot.fillRect(0,0,row*widthAndHeight,col*widthAndHeight);
cot.lineWidth = 1;
var offset = widthAndHeight/2;
    for(var i=0;i<row;i++){
        cot.moveTo((widthAndHeight*i)+offset,0+offset);
        cot.lineTo((widthAndHeight*i)+offset,(col*widthAndHeight)-offset);
    }
    for(var j=0;j<col;j++){
        cot.moveTo(0+offset,(widthAndHeight*j)+offset);
        cot.lineTo((widthAndHeight*row)-offset,(j*widthAndHeight)+offset);
    }
    cot.stroke();
    $("#background").prepend(canvas);

    var str="";
    var index = 0;
    for(var i=0;i<row;i++){
        for(var j=0;j<col;j++){
            str+="<div class='grid' id=\""+index+"\"></div>";
            index++;
        }
    }
    $("#chess").empty();
    $("#chess").append(str);
    $("#chess").css({width:(row*widthAndHeight)+"px",height:(col*widthAndHeight)+"px",position: "absolute",top:"0px",left:"0px","z-index":99999});
    $(".grid").on("click",function(){
        Chess.playchess(this);
    });
    $(".grid").css({width:widthAndHeight+"px",height:widthAndHeight+"px"});

});

function get_new(){
    var rst = '';
    $.get("/get_chessl",function(rtnFromSvr){
        rst = rtnFromSvr;
        var anti_color = 'black';
        if (color == 'black') {
            anti_color = 'white';
        }
        if (rst != '-1' && rst != '') {
            $("#"+rst).html("<div class=\"chessman "+anti_color+"\"></div>");
            play_rst = Chess.isEnd(rst,anti_color)
            if (play_rst) {
                $.get("/end_chessl",function(rtnFromSvr){
                    setTimeout('window.location.replace("/play");', 2000);
                })
            }
        }
        return rst;
    })

}
setInterval("get_new()",1000);

function get_all(){
    var rst = '';
    $.get("/get_all_black_chessl",function(rtnFromSvr){
        rst = rtnFromSvr;
        if (rst == '-2') {
            $("#messageContent").append("");
            alert("Lose Connection!");
        }
        if (rst != '') {
            rst = rst.split(',')
            for (var i = 0; i < rst.length; i++) {
                $("#"+rst[i]).html("<div class=\"chessman "+"black"+"\"></div>");
            }
        }
    })

    rst = '';
    $.get("/get_all_white_chessl",function(rtnFromSvr){
        rst = rtnFromSvr;
        if (rst == '-2') {
            $("#messageContent").append("");
            alert("Lose Connection!");
        }
        if (rst != '') {
            rst = rst.split(',')
            for (var i = 0; i < rst.length; i++) {
                $("#"+rst[i]).html("<div class=\"chessman "+"white"+"\"></div>");
            }
        }
    })
}

get_all();

function checkturn(){
    $.get("/CheckTurnl",function(rtnSvr){
        $("#turn").html(rtnSvr["msg"]);
        // console.log(rtnSvr["msg"]);

    })
}
setInterval("checkturn()",500);

$(window).bind('beforeunload',function(){
    $.get("/leave",function(rtnFromSvr){
        setTimeout('window.location.replace("/index");', 2000);
    })
});