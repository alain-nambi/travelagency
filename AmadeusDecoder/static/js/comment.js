const commentField = document.getElementById('comment');
const pnrId = window.location.pathname.split('/').reverse()[1];
const commentStateUpdateButton = document.getElementById('comment-state');

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };
  
const csrftoken = getCookie("csrftoken");

/*
    Ajax function to send data from 'comment' field to database
*/
$('#send-comment').on('click',function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/comment/',
        dataType: 'json',
        data: {
            comment: commentField.value.trim(),
            pnr_id: pnrId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            console.log(data.comment);
            toastr.success('Votre constat été envoyé avec succès');
        },
        error: function (data) {
            console.log(data)
        }
    });
    $("#comment-form").get(0).reset();
    $('.pnr-signal').removeClass("open");
})

const updateState = (event, commentId)=> {
    $.ajax({
        type: 'POST',
        url: 'update-comment-state/',
        dataType: 'json',
        data: {
            comment_id: commentId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (data) =>{
            console.log(data.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
        },
        error: (data) =>{
            console.log(data);
        }
    });
};

const updateStateDetail = (event, commentId)=> {
    $.ajax({
        type: 'POST',
        url: 'update-comment-state/',
        dataType: 'json',
        data: {
            comment_id: commentId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (data) =>{
            console.log(data.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
            location.reload();
        },
        error: (data) =>{
            console.log(data);
        }
    });
};

$(document).ready(function(){
    $('#commentButton').on('click',function(){
        $('#comment_id').val($(this).data('comment-id'));
        $("#modalResponseConfirmation").modal('show');
    });
})

function comment_reply(state){
    var comment_id = $('#comment_id').val();
    var commentButton = document.getElementById('commentButton');
    console.log(state);

    // without automatic response
    // Update the comment state
    if (state == 0) {
        $.ajax({
            type: 'POST',
            url: 'update-comment-state/',
            dataType : 'json',
            data: {
                comment_id : comment_id,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data){
                console.log(data);
                commentButton.classList.remove('btn-danger');
                commentButton.classList.add('btn-success');
                commentButton.textContent = 'Traitée';
            },
            error: function (data){
                console.log(data);
            }

        })
        
    }
    // with automatic response 
    if (state != 0) {
        $.ajax({
            type: 'POST',
            url: '/comment/reply-comment',
            dataType : 'json',
            data : {
                comment_id:comment_id,
                state:state,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data){
                console.log(data);
                commentButton.classList.remove('btn-danger');
                commentButton.classList.add('btn-success');
                commentButton.textContent = 'Traitée';
                location.reload();
            },
            error: function (data){
                console.log(data);
            }
        })
    }

}


// Reply comment not automatic
$(document).ready(function(){
    $('#comment-response-button').click(function(){
        
    })
});

