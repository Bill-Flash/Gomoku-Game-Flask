// rank list for jumping
$(document).ready(function () {

    // for toggle listener
    $('table').on('click', '.name', look_up_user);
    $('table').on('mouseover', '.name', out)
    $('table').on('mouseleave', '.name', dispear);
})

//check user information
function look_up_user() {
    let name = $(this).text()
    let field = $(this)
    console.log(field.find('.toggle').length===0)
    if (field.find('.toggle').length===0){
        $.post('/api/get_info',
        {name: name}).done(function (response) {
            let server_code = response['returnValue']
            if (server_code == 200){
                let info = response['info']
                field.append(createDiv(info))
            }else {
                console.log("No such a user!")
            }
        }).fail(function (response){
            console.log('server fail')
    })
    }

}

// ajax get user-info
function createDiv(info){
    let box = $('<div></div>').addClass('toggle')
    let img = $('<img>').prop('src',info['photo']).addClass('width-50')
    let intro = $('<p>Introduction:</p>')
    let content = $('<p></p>').text(info['intro'])
        .addClass('intro')
    let gender = $('<p></p>').text('Gender: '+info['gender'])

    box.append(img)
    box.append(intro)
    box.append(content)
    box.append(gender)
    return box
}

function out() {
    $(this).find('.toggle').show()
}
function dispear() {
    $(this).find('.toggle').toggle()
}

