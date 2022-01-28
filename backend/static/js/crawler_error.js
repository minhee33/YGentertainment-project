$(document).ready(function(){
    $.ajax({
        url: '/dataprocess/api/crawler_error',
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
          console.log(res.data);
          var log_info = res.data
          var no_page = 0
          var no_login = 0
          var ect = 0

          for(var i = 0; i< log_info.length; i++){
              if(log_info[i]['error_code'] === '[400]'){
                  no_page  = no_page + 1;
              } else if(log_info[i]['error_code'] === '[401]'){
                  no_login = no_login + 1;
              } else{
                  ect = ect + 1;
              }
          }
          $('#no-page').text(no_page)
          $('#no-login').text(no_login)
          $('#ect').text(ect)
        },
        error: e => {
           console.log(e);
        },
    })
})

const creatRowForError = (data) => {
    const tableRow = $('<tr></tr>')

    for(key in data){
        let dataCol;
        if(key === 'error_code'){
            dataCol = $('<td></td>',{
                text: '페이지 없음'
            })
        } else if(key === 'id'){
            dataCol = $('<td></td>',{
                text: data[key],
                class: 'hidden'
            })
        }  else if(key === 'url'){
            dataCol = $('<td></td>',{
                text : data[key],
                class: 'error-url',
                title: '더블 클릭 하여 수정하세요.'
            })
        }  else{
            dataCol = $('<td></td>',{
                text: data[key],
            })
        }
        tableRow.append(dataCol)
    }
    dataCol = $('<td></td>')
    let dataLabel = $('<label></label>',{
        text:'저장',
        class: 'btn btn-primary btn-shadow border-0',
        id : 'save-error-url'
    })
    dataCol.append(dataLabel)
    tableRow.append(dataCol)
    return tableRow;
}

function action_add(text_add){
	var ul_list = $("ul.pagination"); //ul_list선언
	ul_list.append("<li class='page-item'>"+text_add+"</li>"); //ul_list안쪽에 li추가
}

function crawler_error_table(page){
    $.ajax({
        url: '/dataprocess/api/crawler_error_table/?'+ $.param({
            page:page
        }),
        type: 'GET',
        datatype: 'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
          var log_info = res.data.data
          var no_page_info = [];


          console.log(log_info)
          console.log(res.data.next_page);

          $('#error-report').html('')
          $("ul.pagination").html('')

          for(var i = 0; i<log_info.length; i++){
              if(log_info[i]['error_code'] === '[400]'){
                  no_page_info.push(log_info[i])
              } else{
                  continue
              }
          }

          no_page_info.forEach(data => {
            $('#error-report').append(creatRowForError(data))
          })

          $('.page-link').eq(page)
          action_add(`<span class="page-link">처음</span>`)
          for(var i = 0; i<res.data.total_page; i++){
              action_add(`<span class="page-link">${i+1}</span>`)
          }

          $('.page-link').eq(page).css("color","white")
          $('.page-link').eq(page).css("background-color","black")
          
        },
        error: e => {
           console.log(e);
        },
    })
}


$(document).on('click','.no-page',function(){
    crawler_error_table(1)
})

$(document).on('click','li.page-item',function(){
    page = $(this).children().text();
    if(page === '처음'){
        page = 1;
    } 
    crawler_error_table(page);
})


var url;
$(document).on('dblclick','td.error-url',function(){
    url = $(this).text(); 
    $(this).data('prev-url', $(this).text());
    $(this).text('') //텍스트 비우기
    console.log(url);
    let dataLabel = $('<input></input>',{
        value: url,
        class: 'error-url-input'
    })
    $(this).append(dataLabel)
    
})


$(document).on('click','#save-error-url',function(){
    var tr = $(this).closest('tr')
    datas = [];
    var cells = tr[0].getElementsByTagName("td");
    console.log(cells[1].innerHTML); //artist name
    console.log(cells[2].innerHTML); //platform
    console.log(cells[3].firstElementChild.value); //new url
    console.log(cells[4].innerHTML); //collect target id
    console.log(url); //orginal url


    datas.push({
        'type':'error-change',
        'id' : cells[4].innerHTML,
        'new_target_url':cells[3].firstElementChild.value,
        'old_target_url':url,
    })


    $.ajax({
        url: '/dataprocess/api/platform_of_artist/',
        type: 'PUT',
        datatype:'json',
        data: JSON.stringify(datas),
        success: res => {
            alert('저장되었습니다.');
            cells[3].innerHTML = ''
            cells[3].innerText = res.data

        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })


})


