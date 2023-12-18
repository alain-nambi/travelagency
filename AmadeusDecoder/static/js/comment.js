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
        },
        error: (response) =>{
            console.log(response);
        }
    });
};

//------------------ anomalie : réponse automatique -----------------------------------

$('#comment-ticket-form').hide();
$('#other_info').hide();
$('#Erreur').hide();

$('#comment-ticket').on('click', function(e){
    $('#comment-form').hide();
    $('#comment-ticket-form').show();
    
})

// ---------------------- verif ticket
$(document).ready(function() {
    function VerifTicketValue() {
      var ticket_number = $('#ticket_number').val();
      var Boutton = $('#comment-ticket-next-button');

      if (ticket_number.trim() === '') {
        Boutton.prop('disabled', true);
      } else {
        Boutton.prop('disabled', false);
      }
    }

    $('#ticket_number').on('input', function() {
      VerifTicketValue();
    });

    $('#modal-constat').on('shown.bs.modal', function() {
      VerifTicketValue();
    });

    $('#comment-ticket-next-button').on('click', function() {
      VerifTicketValue();
    });
  });

// --------------------- entrée détails anomalie
$(document).ready(function () {
  $("#comment-ticket-next-button").on("click", function () {
    if ($('#other_info').is(':hidden')) {
      var ticketNumber = $("#ticket_number").val();

      $.ajax({
        type: "POST",
        url: "/home/verif/ticket",
        dataType: "json",
        data: {
          ticket_number: ticketNumber,
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          let result = data.verif;
          console.log(result);
          if (result === true) {
              $('#other_info').show();
          } else {
            toastr.error("Ce billet n'existe pas");
          }
        },
      });
    }
    else{
      console.log('------coucou-----------------');
      var ticketNumber = $("#ticket_number").val();
      var mnt_hors_taxe = $('#montant_hors_taxe').val();
      var taxe = $('#taxe').val();
      var user_id = $('#user_id').val();
      $.ajax({
        type: "POST",
        url: "/home/save-ticket-anomalie",
        dataType: "json",
        data: {
          ticket_number: ticketNumber,
          montant_hors_taxe : mnt_hors_taxe,
          taxe: taxe,
          user_id: user_id,
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          if(data == 'ok'){
            toastr.success('Demande envoyée');
            $('#modal-constat').hide();
            setTimeout(() => {
              location.reload();
            }, 1000)
          }
        },
      });
    }
  });
});

//-------------------- details anomalie (modal)
$(document).on('click', '#table-element', function () {

  var categorie = $(this).data('categorie');
  var anomalie_id = $(this).data('id');
  var pnr_number = $(this).data('pnr-number');
  var ticket_number = $(this).data('ticket-number');
  var montant = $(this).data('montant');
  var taxe = $(this).data('taxe');
  var status = $(this).data('status');

  $('#modal-categorie').text(categorie);
  $('#modal-anomalie_id').val(anomalie_id);
  $('#modal-pnr_number').text(pnr_number);
  $('#modal-ticket_number').text(ticket_number);
  $('#modal-montant').text(montant);
  $('#modal-taxe').text(taxe);


  $('#show-details').modal('show');
  var Boutton = $('#accept-anomaly');

  if (status == 1) {
    Boutton.prop('disabled', true);
  } else {
    Boutton.prop('disabled', false);
  }
})

// ---------------------- update t_ticket 
$(document).ready(function () {
  $('#accept-anomaly').on('click', function(e){
    console.log('---coucou----');
    var ticket_number = $('#modal-ticket_number').text();
    var anomalie_id = $('#modal-anomalie_id').val();
    var montant = $('#modal-montant').text();
    var taxe = $('#modal-taxe').text();

    $.ajax({
        type: "POST",
        url: "/home/update-ticket",
        dataType: "json",
        data: {
          ticket_number: ticket_number,
          anomalie_id: anomalie_id,
          montant: montant,
          taxe: taxe,
          csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
          console.log(data);
          if (data == 'ok') {
            toastr.success('Ticket ${ticket_number} remonté');
            $('#show-details').hide();
            setTimeout(() => {
                location.reload();
              }, 1000)
            }
          else{
            toastr.error('Erreur. Veuillez recommencer');
            $('#show-details').hide();
            setTimeout(() => {
                location.reload();
              }, 1000)
          }
        },
      });
  });
});
