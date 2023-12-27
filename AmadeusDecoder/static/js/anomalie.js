//------------------ anomalie : réponse automatique -----------------------------------

$('#comment-ticket-form').hide();
$('#other_info').hide();
$('#info').hide();
$('#Erreur').hide();
$('#fee').hide();

$('#comment-ticket').on('click', function (e) {
    $('#comment-form').hide();
    $('#comment-ticket-form').show();

})

// ---------------------- verif ticket Value
$(document).ready(function () {
    function VerifTicketValue() {
        var ticket_number = $('#ticket_number').val();
        var Boutton = $('#comment-ticket-next-button');
   
        if (ticket_number.trim() === '') {
            Boutton.prop('disabled', true);
        } else {
            Boutton.prop('disabled', false);
        }
    }


    $('#ticket_number').on('input', function () {
        ticket = $('#ticket_number').val();
        VerifTicketLength();
    });

    $('#modal-constat').on('shown.bs.modal', function () {
        VerifTicketValue();
    });

    $('#comment-ticket-next-button').on('click', function () {
        VerifTicketValue();
    });
});

// ---------------------- verif ticket length

    function VerifTicketLength() {
        ticket = $('#ticket_number').val();
        var regex = /^[0-9-]+$/;
        var Boutton = $('#comment-ticket-next-button');
        if (!regex.test(ticket)) {
            toastr.error("Veuillez saisir uniquement des chiffres");
            Boutton.prop('disabled', true);
        }
        if(ticket.length > 16){
            Boutton.prop('disabled', true);
        }
        if (ticket.length <= 16) {
            Boutton.prop('disabled', false);
        }
        if (ticket.length == 14) {
            var firstPart = ticket.substring(0, 13);
            var modifiedTicket = firstPart + '-' + ticket[13];
            $('#ticket_number').val(modifiedTicket);

            $('#ticket_number').attr('maxlength', 16);
        }
    }

// ------------------ verif ticket type
$(document).ready(function () {
    type = document.getElementById('selectType');
    type.addEventListener("change", function (){
        if (type.value == 'TKT') {
            $('#fee').hide();
        } else {
            $('#fee').show();
        }
    });
});



// --------------------- entrée détails anomalie
const parent = document.getElementById("selectPassenger");
const parent_segment = document.getElementById('selectSegment');

const child = document.getElementById("child_passeger");
const child_segment = document.getElementById('child_segment');

if (child) {
    parent.removeChild(child);
}

//---------------- Ticket verification and saving anomalie
$(document).ready(function () {
    $("#comment-ticket-next-button").on("click", function () {
        var pnr_id = $("#pnr-id").val();
        //Ticket verification
        if ($('#info').is(':hidden')) {
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

                    if (result === 'True') { // if ticket exists
                        showInfoSection();
                    } if (result === 'is_no_adc'){
                        toastr.error('Ticket Is no adc')
                    } 
                    if (result === 'False') { // if ticket does not exist
                        $.ajax({
                            type: "POST",
                            url: "/home/get-passengers-and-segments",
                            dataType: "json",
                            data: {
                                pnr_id: pnr_id,
                                csrfmiddlewaretoken: csrftoken,
                            },
                            success: function (data) {
                                console.log(data);
                                let passengers = data.context.passengers;
                                if (passengers.length > 0) {
                                    parent.innerHTML = ''

                                    passengers.map((passenger) => {
                                        const newOption = document.createElement("option");
                                        newOption.id = "child_passenger";
                                        newOption.value = passenger['passenger_id'];
                                        if (passenger['passenger_name'] !== null  && passenger['passenger_surname'] != null ){
                                            newOption.textContent = passenger['passenger_surname'] + ' ' + passenger['passenger_name'];
                                        }
                                        if (passenger['passenger_name'] !== null  && passenger['passenger_surname'] == null ) {
                                            newOption.textContent = passenger['passenger_name'] ;
                                        }
                                        if (passenger['passenger_name'] == null  && passenger['passenger_surname'] !== null ) {
                                            newOption.textContent = passenger['passenger_surname'];
                                        }
                                        parent.append(newOption);
                                    });
                                } else {
                                    console.log('Error......');
                                }
                                let segments = data.context.segments;
                                if (segments.length > 0) {

                                    segments.map((segment) => {
                                        const newOption = document.createElement("option");
                                        newOption.id = "child_segment";
                                        newOption.value = segment['segment_id'];
                                        newOption.textContent = segment['segment'] + ' ' + segment['vol'] + ' ' + segment['vol_number'];

                                        parent_segment.append(newOption);
                                    });
                                } else {
                                    console.log('Error......');
                                }
                                showInfoSection();
                                showOtherInfoSection();
                            }
                        });
                    }
                },
            });
        }
            //Saving Anomalie
        else {

            if ($("#other_info").is(':hidden')) { // if ticket exists
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
                        montant_hors_taxe: mnt_hors_taxe,
                        taxe: taxe,
                        user_id: user_id,
                        pnr_id: pnr_id,
                        csrfmiddlewaretoken: csrftoken,
                    },
                    success: function (data) {
                        if (data == 'ok') {
                            toastr.success('Demande envoyée');
                            $('#modal-constat').hide();
                            setTimeout(() => {
                                location.reload();
                            }, 1000)
                        }
                        if(data == 'error'){
                            toastr.error(data.error);
                        }
                    },
                });   
            } else { // if ticket does not exist
                var ticketNumber = $("#ticket_number").val();
                var mnt_hors_taxe = $('#montant_hors_taxe').val();
                var taxe = $('#taxe').val();
                var user_id = $('#user_id').val();
                var passenger_id = $('#selectPassenger').val();
                var segment = $('#selectSegment').val();
                var type = $('#selectType').val();
                var fee;

                feeCheckbox = document.getElementById('feecheckbox')
                if ($('#fee').is(':hidden')) {
                    fee = true;
                } else {
                    fee = feeCheckbox.checked;
                }

                $.ajax({
                    type: "POST",
                    url: "/home/save-ticket-anomalie",
                    dataType: "json",
                    data: {
                        ticket_number: ticketNumber,
                        montant_hors_taxe: mnt_hors_taxe,
                        taxe: taxe,
                        user_id: user_id,
                        pnr_id: pnr_id,
                        passenger_id: passenger_id,
                        segment: segment,
                        ticket_type: type,
                        fee: fee,
                        csrfmiddlewaretoken: csrftoken,
                    },
                    success: function (data) {
                        if (data == 'ok') {
                            toastr.success('Demande envoyée');
                            $('#modal-constat').hide();
                            setTimeout(() => {
                                location.reload();
                            }, 1000)
                        }
                    },
                });   
            }
            
        }

        // Fonction pour montrer la section d'info
        function showInfoSection() {
            $('#info').show();
        }

        // Fonction pour montrer la section d'autres informations
        function showOtherInfoSection() {
            $('#other_info').show();
        }
    });
});

// ---------------------- update or create ticket 

function accept_anomaly(anomalie_id){
    console.log('---coucou----');
    // var anomalie_id = $('#anomalie_id').val();
    console.log(anomalie_id);
        $.ajax({
            type: "POST",
            url: "/home/update-ticket",
            dataType: "json",
            data: {
                anomalie_id: anomalie_id,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data == 'ok') {
                    toastr.success('Ticket remonté');
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                }
                else {
                    toastr.error('Erreur. Veuillez recommencer');
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                }
            },
        });
    
}

