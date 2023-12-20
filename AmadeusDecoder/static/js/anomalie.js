//------------------ anomalie : réponse automatique -----------------------------------

$('#comment-ticket-form').hide();
$('#other_info').hide();
$('#info').hide();
$('#Erreur').hide();

$('#comment-ticket').on('click', function (e) {
    $('#comment-form').hide();
    $('#comment-ticket-form').show();

})

// ---------------------- verif ticket
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
        VerifTicketValue();
    });

    $('#modal-constat').on('shown.bs.modal', function () {
        VerifTicketValue();
    });

    $('#comment-ticket-next-button').on('click', function () {
        VerifTicketValue();
    });
});

// --------------------- entrée détails anomalie
const parent = document.getElementById("selectPassenger");

const child = document.getElementById("child_passeger");
if (child) {
    parent.removeChild(child);
}
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
                    console.log(result);

                    if (result === true) {
                        showInfoSection();
                    } else {
                        $.ajax({
                            type: "POST",
                            url: "/home/get-passengers-by-pnr",
                            dataType: "json",
                            data: {
                                pnr_id: pnr_id,
                                csrfmiddlewaretoken: csrftoken,
                            },
                            success: function (data) {
                                console.log(data);
                                let passengers = data.context.passengers;
                                console.log(passengers);
                                console.log(passengers.length);
                                if (passengers.length > 0) {
                                    parent.innerHTML = ''

                                    passengers.map((passenger) => {
                                        const newOption = document.createElement("option");
                                        newOption.id = "child_passenger";
                                        newOption.value = passenger['passenger_id'];
                                        newOption.textContent = passenger['passenger_surname'] + ' ' + passenger['passenger_name'];

                                        parent.append(newOption);
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
            if ($("#other_info").is(':hidden')) {
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
                    },
                });   
            } else {
                var ticketNumber = $("#ticket_number").val();
                var mnt_hors_taxe = $('#montant_hors_taxe').val();
                var taxe = $('#taxe').val();
                var user_id = $('#user_id').val();
                var passenger_id = $('#selectPassenger').val();
                var segment = $('#segment').val();

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


//-------------------- details anomalie (modal)
$(document).ready(function () {
    $(document).on("click", '#table-element', function (e) {
        try {
            var ticket_status = $(this).data('ticket-status');

            var categorie = $(this).data('categorie');
            var anomalie_id = $(this).data('id');
            var pnr_number = $(this).data('pnr-number');
            var ticket_number = $(this).data('ticket-number');
            var montant = $(this).data('montant');
            var taxe = $(this).data('taxe');
            var status = $(this).data('status');
            var user = $(this).data('issuing-user');
            var passenger_id = $(this).data('passenger-id');
            var segment = $(this).data('segment');

            // si ticket existe

            $('#modal-categorie').text(categorie);
            $('#modal-anomalie_id').val(anomalie_id);
            $('#modal-pnr_number').text(pnr_number);
            $('#modal-ticket_number').text(ticket_number);
            $('#modal-montant').text(montant);
            $('#modal-taxe').text(taxe);
            $('#modal-user').text(user);

            if (ticket_status ===1) { // si ticket n'existe pas
                
                $.ajax({
                    type: "POST",
                    url: "/home/getPassengerById",
                    dataType: "json",
                    data: {
                        passenger_id: passenger_id,
                        csrfmiddlewaretoken: csrftoken,
                    },
                    success: function (data) {
                        console.log(data);
                        let passenger = data.passenger;
                        console.log(passenger.name);
                        let passenger_name = passenger.name;
                        let passenger_surname = passenger.surname;
                        console.log(passenger_name);

                        $('#modal-passenger_id').val(passenger_id);
                        $('#modal-passenger-name').text(passenger_name);
                        $('#modal-passenger-surname').text(passenger_surname);
                        $('#modal-segment').text(segment);
                    }
                });

                
            }

            $('#show-details').modal('show');
            var Boutton = $('#accept-anomaly');

            if (status == 1) {
                Boutton.prop('disabled', true);
            } else {
                Boutton.prop('disabled', false);
            }

        } catch (error) {
            console.error("Une erreur s'est produite : ", error.message);
        }
    });
});

// ---------------------- update or create ticket 
$(document).ready(function () {
    $('#accept-anomaly').on('click', function (e) {
        console.log('---coucou----');
        var ticket_number = $('#modal-ticket_number').text();
        var anomalie_id = $('#modal-anomalie_id').val();
        var montant = $('#modal-montant').text();
        var taxe = $('#modal-taxe').text();
        var user = $('#modal-user').text();
        var passenger_id = $('#passenger_id').val();
        var segment = $('#segment').text();
        var pnr_id = $('#pnr_id').val();

        if ($("#other_info").is(':hidden')) {
            
            $.ajax({
                type: "POST",
                url: "/home/update-ticket",
                dataType: "json",
                data: {
                    ticket_number: ticket_number,
                    anomalie_id: anomalie_id,
                    montant: montant,
                    taxe: taxe,
                    issuing_user: user,
                    pnr_id: pnr_id,
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
                    else {
                        toastr.error('Erreur. Veuillez recommencer');
                        $('#show-details').hide();
                        setTimeout(() => {
                            location.reload();
                        }, 1000)
                    }
                },
            });
        } else {  
            $.ajax({
                type: "POST",
                url: "/home/update-ticket",
                dataType: "json",
                data: {
                    ticket_number: ticket_number,
                    anomalie_id: anomalie_id,
                    montant: montant,
                    taxe: taxe,
                    issuing_user: user,
                    passenger_id:passenger_id,
                    segment:segment,
                    pnr_id: pnr_id,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function (data) {
                    console.log(data);
                    if (data == 'ok') {
                        toastr.success(`Ticket ${ticket_number} remonté`);
                        $('#show-details').hide();
                        setTimeout(() => {
                            location.reload();
                        }, 1000)
                    }
                    else {
                        toastr.error('Erreur. Veuillez recommencer');
                        $('#show-details').hide();
                        setTimeout(() => {
                            location.reload();
                        }, 1000)
                    }
                },
            });
        }
        
    });
});
