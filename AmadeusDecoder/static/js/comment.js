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
        success: (response) => {
            console.log(response.comment);
            toastr.success('Votre constat été envoyé avec succès');
        },
        error: (response) => {
            console.log(response)
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
        success: (response) =>{
            console.log(response.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
        },
        error: (response) =>{
            console.log(response);
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
        success: (response) =>{
            console.log(response.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
            location.reload();
        },
        error: (response) =>{
            console.log(response);
        }
    });
};

