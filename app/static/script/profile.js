// profile page for detailed competition records
$(document).ready(function () {

    // records
    stage_records()
})

//idea from lab&quiz
function stage_records() {
    name = $(".name").attr('id')
    // get the record list
    // add row for each record list with proper formatting
    $.post('/api/get_records',
        {name: name}).done(function (response) {
            let server_code = response[0]['returnValue']
            if (server_code == 200){
                for (record of response[1]) {
                    console.log(record)
                    let row = $('<tr></tr>').addClass('record_table_row');
                    let index = $('<td></td>').text(response[1].indexOf(record)+1);
                    index.prop('id',record.id)
                    let result = $('<td></td>').html(record.result);
                    let name = $('<td></td>').html(record.name);
                    let time = $('<td></td>').html(record.time.slice(0,record.time.length-3));

                    row.append(index);
                    row.append(result);
                    row.append(name);
                    row.append(time);
                    $("#tbody").append(row);
                }
            }else {
                console.log("No such a user!")
            }
        }).fail(function (response){
            console.log('server fail')
    })
}