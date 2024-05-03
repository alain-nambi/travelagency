//------------------ anomalie : réponse automatique -----------------------------------

$('#comment-ticket-form').hide();
$('#other_info').hide();
$('#info').hide();
$('#Erreur').hide();
$('#fee').hide();
$('#comment-ticket-cancel-button').hide();

$('#comment-ticket').on('click', ()=> {
    // lister les billet non affichés dans la page pnr-detail
    var container = document.getElementById("list-ticket");
    var pnrIdDiv = document.getElementById("pnr_id");
    var pnr_id = pnrIdDiv.getAttribute("data-id");
    get_unshowed_ticket(pnr_id,container)
    $('#comment-ticket-next-button').hide();
    $('#comment-form').hide();
    $('#comment-ticket').hide();  
})

function createButton(container, ticketNumber) {
    // Créer un bouton correspondant à un billet
    var button = document.createElement("button");
    button.className = 'btn btn-info';
    button.innerHTML = ticketNumber;
    button.style.margin = '20px 10px 10px 0';
    

    button.addEventListener("click", function () {
        // Afficher les champs numero du billet, montant hors taxe et taxe

        showTicketInput();

        $('#info').show();
        $('#comment-ticket-next-button').show();

        $('#ticket_number').val(ticketNumber);
        // Afficher le bouton annuler
        $('#comment-ticket-cancel-button').show();
        
        var Boutton = $('#comment-ticket-next-button');
        Boutton.prop('disabled', false);
        
    });
    container.appendChild(button);
}

// Hide ticket input
function hideTicketInput(){
    var ticket_input = document.querySelector('#ticket_input');
    ticket_input.hidden = true;
}

// show ticket input
function showTicketInput(){
    var ticket_input = document.querySelector('#ticket_input');
    ticket_input.hidden = false;
}

// Hide InfoSection
function hideInfoSection() {
    $('#info').hide();
}

// Show Cancel Button
function showCancelButton(){
    $('#comment-ticket-cancel-button').show();
}

// Fonction pour montrer la section d'autres informations
function hideOtherInfoSection() {
    $('#other_info').hide();
}

function get_unshowed_ticket(pnr_id,container){
    $.ajax({
        type: "POST",
        url: "/comment/get-unshowed-tickets",
        dataType: 'json',
        data : {
            pnr_id : pnr_id,
            csrfmiddlewaretoken : csrftoken
        },
        success : function(data){
            if(data.status = 200){
                $('#comment-ticket-form').show();

                // Ajouter un titre au modal
                var title = document.createElement("h3");
                title.innerHTML = "Billets non remonté";
                title.style.margin = '10px 0 0 0';
                container.appendChild(title);

                // créer les boutons correspondants au billets
                data.tickets.forEach((ticket)=>{
                    createButton(container,ticket.number)
                })

                // Ajouter un bouton pour un nouveau billet
                var new_ticket_button = document.createElement("button");
                new_ticket_button.className = 'btn btn-success';
                new_ticket_button.innerHTML = 'Nouveau Billet';
                new_ticket_button.style.margin = '20px 10px 10px 0';
                new_ticket_button.addEventListener("click", function(){
                    // Don't allow to modify ticket number
                    $('#ticket_number').removeAttr('disabled')
                    showTicketInput();
                    $('#ticket_number').val('');
                    $('#comment-ticket-next-button').show();
                });
                container.appendChild(new_ticket_button);
            }
        },
    });
}

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
        var inputValue = $(this).val();

        // Seulement pour les remboursements à remonter
        var sanitizedValue = inputValue.replace(/[^0-9-]/g, '');
        $(this).val(sanitizedValue);

        $('#comment-ticket').attr("disabled", true);

        VerifTicketLength();
    });

    $('#modal-constat').on('shown.bs.modal', function () {
        // VerifTicketValue();
    });

    $('#comment-ticket-next-button').on('click', function () {
        VerifTicketValue();
    });
});

// ---------------------- verif ticket length

    function VerifTicketLength() {
        ticket = $('#ticket_number').val();
        var Boutton = $('#comment-ticket-next-button');
        
        if(ticket.length > 16){
            Boutton.prop('disabled', true);
        }
        if (ticket.length <= 16) {
            Boutton.prop('disabled', false);
        }
        if (ticket.length < 13) {
            Boutton.prop('disabled', true);
        }

        if(ticket.length == 14 && ticket.charAt(13) !== '-') {
            var modifiedValue = ticket.slice(0, 13) + '-' + ticket.slice(13);
            $('#ticket_number').val(modifiedValue);
        }
    }

// ------------------ verif ticket type
$(document).ready(function () {
    type = document.getElementById('selectType');
    if (type) {
        type.addEventListener("change", function (){
            if (type.value == 'TKT') {
                $('#fee').hide();
            } else {
                $('#fee').show();
            }
        });
    }
});



// --------------------- entrée détails anomalie
const parent = document.getElementById("selectPassenger");

const child = document.getElementById("child_passenger");

if (child) {
    parent.removeChild(child);
}

function accept_anomaly(anomalie_id){

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


//---------------- Ticket verification and saving anomalie
$(document).ready(function () {
    $("#comment-ticket-next-button").on("click", function () {
        var pnr_id = $("#pnr-id").val();

        $("#montant_hors_taxe, #taxe").on("input", function() {
            var inputValue = $(this).val();
            
            // Utiliser la regex pour valider le format
            if (/^\d+(\.\d+)?(,\d+)?$/.test(inputValue)) {
                // Le format est correct, ne rien faire
            } else {
                // Le format est incorrect, nettoyer la valeur
                // à décommenter lorsque les remboursements sont remontées
                var sanitizedValue = inputValue.replace(/[^0-9,.]/g, '');
                $(this).val(sanitizedValue);
            }
        });        
        

        $("#taxe").on("input", function() {
            var inputValue = $(this).val();
            
            // Utiliser la regex pour valider le format
            if (/^\d+(\.\d+)?(,\d+)?$/.test(inputValue)) {
                // Le format est correct, ne rien faire
            } else {
                // Le format est incorrect, nettoyer la valeur
                var sanitizedValue = inputValue.replace(/[^0-9,.]/g, '');
                $(this).val(sanitizedValue);
            }
        })


        //Ticket verification
        if ($('#info').is(':hidden')) {
            var ticketNumber = $("#ticket_number").val();

            let index = ticketNumber.indexOf('-');

            console.log(ticketNumber.length);

            if (index !== -1) {
                if (!/^\d+$/.test(ticketNumber[index + 1]) || ticketNumber.length < 16) {
                    ticketNumber = ticketNumber.slice(0, 13)
                    $("#ticket_number").val(ticketNumber)
                }
            }

            console.log("Modified Ticket Number");
            console.log(ticketNumber);

            $.ajax({
                type: "POST",
                url: "/home/verif/ticket",
                dataType: "json",
                data: {
                    ticket_number: ticketNumber,
                    pnr_id:pnr_id,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function (data) {
                    let result = data.verif;

                    if (result.exist === true) { // if ticket exists
                        // Don't allow to modify ticket number
                        $('#ticket_number').attr('disabled', true)
                        showInfoSection();
                        $('#montant_hors_taxe').val(result.ticket_cost);
                        $('#taxe').val(result.ticket_tax);

                    } if (result === 'is_no_adc'){
                        toastr.info('Ticket Is no adc')
                    } 
                    if(result === 'pnr'){
                        toastr.info("Billet d'un autre PNR")
                    }
                    
                    if (result.exist === false) {
                        toastr.info(`Ce billet est déja présent dans le PNR ${result.pnr}`)
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
                                if (segments.length ==0){
                                    $('#SegmentLabel').hide();
                                    $('#selectSegment').hide();
                                }
                                if (segments.length > 0) {
                                    const segment_options = segments.map((segment) => {
                                        return {
                                            label: segment['segment'],
                                            value: segment['segment_id'],
                                        };
                                    });

                                    // segment_options.push({ label: 'Pas de segment', value: ''});

                                    VirtualSelect.init({
                                        ele: '#selectSegment',
                                        multiple: true,
                                    });
                                    document.querySelector('#selectSegment').setOptions(segment_options);

                                    var disabledOptions = [];
                                    segment_options.forEach(option => {
                                        if (option.value != '') {
                                            disabledOptions.push(option.value);    
                                        }
                                    });

                                    $('#selectSegment').on('change', function () {
                                        selectedValues = document.querySelector('#selectSegment').getSelectedOptions();
                                        
                                    });
                                } else {
                                    console.log('Error......');
                                }
                                // Don't allow to modify ticket number
                                $('#ticket_number').attr('disabled', true)
                                showInfoSection();
                                showOtherInfoSection();
                                showCancelButton();
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
                        console.log(data);
                        if (data.status == 'ok') {
                            if(data.accept == true){
                                accept_anomaly(data.anomalie_id)
                            }
                            else{
                                toastr.success('Demande envoyée avec succes')
                            }
                            
                            $('#modal-constat').hide();
                            setTimeout(() => {
                                location.reload();
                            }, 1000)
                        } 
                        if (data.status == 'error') {
                            toastr.error(data.error)
                        }
                    },
                });   
            } else { // if ticket does not exist
                var ticketNumber = $("#ticket_number").val();
                var mnt_hors_taxe = $('#montant_hors_taxe').val();
                var taxe = $('#taxe').val();
                var user_id = $('#user_id').val();
                var passenger_id = $('#selectPassenger').val();
                var segment ;

                if($('#selectSegment').is(":hidden") ){
                    segment = [];
                }
                else{
                    segment = document.querySelector('#selectSegment').getSelectedOptions();
                }

                try {
                    if (document.querySelector('#selectSegment').getSelectedOptions()) {
                        segment = document.querySelector('#selectSegment').getSelectedOptions()
                    } else {
                        segment = []
                    }
                } catch (error) {
                    segment = []
                    console.log(error.message);
                }
                
                var type = $('#selectType').val();
                var fee;

                feeCheckbox = document.getElementById('feecheckbox')
                if ($('#fee').is(':hidden')) {
                    fee = true;
                } else {
                    fee = feeCheckbox.checked;
                }

                const listNewTicketAnomalyInfo = []
                listNewTicketAnomalyInfo.push({
                    segment: segment,
                    ticket_number: ticketNumber,
                    montant_hors_taxe: mnt_hors_taxe,
                    taxe: taxe,
                    user_id: user_id,
                    pnr_id: pnr_id,
                    passenger_id: passenger_id,
                    ticket_type: type,
                    fee: fee,
                })


                $.ajax({
                    type: "POST",
                    url: "/home/save-ticket-anomalie",
                    dataType: "json",
                    data: {
                        listNewTicketAnomalyInfo: JSON.stringify(listNewTicketAnomalyInfo),
                        csrfmiddlewaretoken: csrftoken,
                    },
                    success: function (data) {
                        console.log(data);
                        if (data.status == 'ok') {
                            if(data.accept == true){
                                accept_anomaly(data.anomalie_id)
                            }
                            else{
                                toastr.success('Demande envoyée avec succes')
                            }
                            $('#modal-constat').hide();
                            setTimeout(() => {
                                location.reload();
                            }, 1000)
                        } 
                        if (data.status == 'error') {
                            toastr.error(data.error)
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

    

    $('#comment-ticket-cancel-button').on('click', function (){
        hideTicketInput();
        hideInfoSection();
        hideOtherInfoSection();
        $('#comment-ticket-cancel-button').hide();
        $('#comment-ticket-next-button').hide();
        var Boutton = $('#comment-ticket-next-button');
        Boutton.prop('disabled', true);
    });
});

// ---------------------- update or create ticket 
// $('#card-update-anomaly').hide();



function refuse_anomaly(anomalie_id) {

    $.ajax({
        type: "POST",
        url: "/home/refuse-anomaly",
        dataType: "json",
        data: {
            anomalie_id: anomalie_id,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Anomalie refusée');
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

function drop_anomaly(anomalie_id) {
    $.ajax({
        type: "POST",
        url: "/home/drop-anomaly",
        dataType: "json",
        data: {
            anomalie_id: anomalie_id,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Anomalie supprimée');
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

function update_anomaly(anomalie_id){
    var name = 'card-anomaly-' + anomalie_id;
    var nameUpdate = 'card-update-anomaly-' + anomalie_id;
    // console.log(name);
    // console.log(nameUpdate);

    var cardAnomaly = document.getElementById(name);
    cardAnomaly.hidden = true;
    var cardUpdateAnomaly = document.getElementById(nameUpdate);
    if (cardUpdateAnomaly) {
        cardUpdateAnomaly.hidden = !cardUpdateAnomaly.hidden;
    }
}

function VerifTicketUpdatedLength(id) {
    var Boutton = $('#update-anomaly-button');
    element = document.getElementById(id);

    var sanitizedValue = element.value.replace(/[^0-9-]/g, '');
    element.value = sanitizedValue;

    if (element.value.length > 16) {
        Boutton.prop('disabled', true);
    }
    if (element.value.length <= 16) {
        Boutton.prop('disabled', false);
    }
    if (element.value.length < 13) {
        Boutton.prop('disabled', true);
    }
    element = document.getElementById(id);
    if (element.value.length === 14 && element.value.charAt(13) !== '-') {
        // console.log('COUCOU------');
        var modifiedValue = element.value.slice(0, 13) + '-' + element.value.slice(13);
        element.value = modifiedValue;
    }

}

function VerifNumberValue(id){
    // console.log('COUCOU--------------');
    var Boutton = $('#update-anomaly-button');
    element = document.getElementById(id);
    var regex = /^\d+(\.\d{1,2})?$/;

    if (!regex.test(element.value)) {
        element.style.borderColor = 'red';
        Boutton.prop('disabled', true);
        toastr.error(('Le montant doit être au format correct (par exemple, 100 ou 100.50 et non 100.)'));
    }
    else{
        element.style.borderColor = 'black';
        Boutton.prop('disabled', false);
    }

}

function updateAnomaly(anomalie_id){
    var ticket = $('#ticket_to_update-'+anomalie_id).val();
    var montant = $('#montant_to_update-' + anomalie_id).val();
    var taxe = $('#taxe_to_update-' + anomalie_id).val();

    $.ajax({
        type: "POST",
        url: "/home/update-anomaly",
        dataType: "json",
        data: {
            anomaly_id: anomalie_id,
            ticket: ticket,
            montant: montant,
            taxe: taxe,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            if (data == 'ok') {
                toastr.success('Anomalie modifiée');
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