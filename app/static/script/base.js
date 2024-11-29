$(document).ready(function () {
    // get the night/light
    get_mode()

    //toggle
    $('.btn').mouseover(function(){
        $(this).find('li').show();
    })
    $('.btn').mouseout(function(){
        $(this).find('li').hide();
    })

    //switch mode
    $('#mode').on("click", function(){
        $('body').toggleClass('body body_dark');
        $('#itp').toggleClass('title titled');

        mo = $('body').attr('class');
        $.get('/remember_mode', {mo:mo}, function (response) {
            m = response;
        })
    })
})


function get_mode(){
    m = ""
    $.get('/get_mode', function (response) {
        m = response;
        if(m == "dark"){
            $('body').removeClass('body');
            $('body').addClass('body_dark');
            $('#itp').removeClass('title');
            $('#itp').addClass('titled');
        } else if(m == "light"){
            $('body').removeClass('body_dark');
            $('body').addClass('body');
            $('#itp').removeClass('titled');
            $('#itp').addClass('title');
        }
    })
}
