//------------------ anomalie : réponse automatique -----------------------------------

$('#comment-ticket-form').hide();
$('#other_info').hide();
$('#info').hide();
$('#taxSection').hide();
$('#Erreur').hide();
$('#fee').hide();
$('#comment-ticket-cancel-button').hide();

$('#comment-ticket').on('click', ()=> {
    // lister les billets non affichés dans la page pnr-detail
    var container = document.getElementById("list-ticket");
    var pnrIdDiv = document.getElementById("pnr_id");
    var pnr_id = pnrIdDiv.getAttribute("data-id");
    get_unshowed_ticket(pnr_id,container)
    $('#comment-ticket-next-button').hide();
    $('#comment-form').hide();
    $('#comment-ticket').hide();  
})

function createButton(container, ticketNumber, transportCost, taxe) {
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
        $('#taxSection').show();

        $('#ticket_number').val(ticketNumber);
        $('#ticket_number').prop('disabled', true);

        $('#montant_hors_taxe').val(transportCost);
        $('#taxe').val(taxe);


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
    $('#taxSection').hide();

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
                title.innerHTML = "Billet non remonté";
                title.style.margin = '10px 0 0 0';
                container.appendChild(title);

                // créer les boutons correspondants au billets
                data.tickets.forEach((ticket)=>{
                    createButton(container,ticket.number,ticket.transport_cost,ticket.taxe)
                })

                // Ajouter un bouton pour un nouveau billet
                var new_ticket_button = document.createElement("button");
                new_ticket_button.className = 'btn btn-success';
                new_ticket_button.innerHTML = 'Nouveau Billet';
                new_ticket_button.style.margin = '20px 10px 10px 0';
                new_ticket_button.value = "TKT";
                new_ticket_button.addEventListener("click", function(){
                    // Don't allow to modify ticket number
                    $('#ticket_number').removeAttr('disabled')
                    $('#ticket_number').attr('data-isticket', '0');
                    showTicketInput();
                    $('#ticket_number').val('');
                    $('#comment-ticket-next-button').show();
                });
                container.appendChild(new_ticket_button);

                // Ajouter un bouton pour les remboursements
                var new_rfnd_button = document.createElement("button");
                new_rfnd_button.className = 'btn btn-success';
                new_rfnd_button.innerHTML = 'Remboursement';
                new_rfnd_button.value = 'RFND';
                new_rfnd_button.style.margin = '20px 10px 10px 0';
                new_rfnd_button.addEventListener("click", function(){
                    // Don't allow to modify ticket number
                    $('#ticket_number').removeAttr('disabled')
                    $('#ticket_number').attr('data-isticket', '1');
                    showTicketInput();
                    $('#ticket_number').val('');
                    $('#comment-ticket-next-button').show();
                });
                container.appendChild(new_rfnd_button);
            }
        },
    });
}

// ---------------------- verif ticket Value
$(document).ready(function () {
    function VerifTicketValue() {
        var ticket_number = $('#ticket_number').val();
        var ticket_button= $('#new_ticket').val();
        var rfnd_button = $('#rfnd').val();

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
        var sanitizedValue =""
        let isticket = $('#ticket_number').attr('data-isticket');
        if(isticket == 0) {
            sanitizedValue = inputValue.replace(/[^0-9-]/g, '');
        }else{ // remboursement
            sanitizedValue = inputValue.replace(/[^0-9-Rr]/g, '').replace(/r/g, 'R');
        }

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
        let isticket = $('#ticket_number').attr('data-isticket');
        var Boutton = $('#comment-ticket-next-button');
        
        Boutton.prop('disabled', ticket.length > 16 || ticket.length < 13);

        if (ticket.length === 14 && ticket.charAt(13) !== '-') {
            $('#ticket_number').val(ticket.slice(0, 13) + '-' + ticket.slice(13));
        } else if (ticket.length === 13 && isticket == 1) {
            $('#ticket_number').val(ticket + '-R');
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
        var isticket = $('#ticket_number').attr('data-isticket');
        

        $("#montant_hors_taxe").on("input", function() {
            var inputValue = $(this).val();
            if(isticket == 0){ // si c'est un billet
                // Utiliser la regex pour valider le format
                var sanitizedValue = inputValue.replace(/[^0-9,.]/g, '');
                sanitizedValue = sanitizedValue.replace(',', '.');
                $(this).val(sanitizedValue);

            }
            else{ // si c'est un remboursement
                
                // Retirer tous les caractères non numériques, excepté les points et les virgules
                let value = inputValue.replace(/[^0-9,.]/g, ''); 
                var rfndValue = value.replace(',', '.');
                $(this).val('-' + rfndValue);
            }
            
        });        
        

        $("#taxe").on("input", function() {
            var inputValue = $(this).val();
            
           // Utiliser la regex pour valider le format
           var sanitizedValue = inputValue.replace(/[^0-9,.]/g, '');
           sanitizedValue = sanitizedValue.replace(',', '.');
           $(this).val(sanitizedValue);
        })


        //Ticket verification
        if ($('#info').is(':hidden')) {
            var ticketNumber = $("#ticket_number").val();

            let index = ticketNumber.indexOf('-');

            console.log(ticketNumber.length);
            
            if($("#ticket_number").attr('data-isticket') == 0){
                if (index !== -1) {
                    if (!/^\d+$/.test(ticketNumber[index + 1]) || ticketNumber.length < 16) {
                        ticketNumber = ticketNumber.slice(0, 13)
                        $("#ticket_number").val(ticketNumber)
                    }
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
                    console.log('RESULT : ', result);
                    
                    if (result.exist === 'Exist') { // if ticket exists
                        // Don't allow to modify ticket number
                        $('#ticket_number').attr('disabled', true)
                        showInfoSection();
                        showCancelButton();
                        $('#montant_hors_taxe').val(result.ticket_cost);
                        $('#taxe').val(result.ticket_tax);

                    } if (result === 'is_no_adc'){
                        toastr.info('Ticket Is no adc')
                    } 
                    if(result === 'pnr'){
                        toastr.info("Billet d'un autre PNR !")
                    }
                    if(result === 'True'){
                        toastr.info("Ce billet est déjà remonté !")
                    }

                    if(result === 'Tarification'){
                        toastr.info("Envoi de mail de tarification billet manquant !")
                    }
                    
                    if (result.exist === true) {
                        toastr.info(`Ce billet est déja présent dans le PNR ${result.pnr} !`);
                        $('#info').hide();
                        $('#taxSection').hide();
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
                var isTickets = $("#ticket_number").attr('data-isticket');
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
                    isticket: isTickets,

                })
                console.log(listNewTicketAnomalyInfo);


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
            let isticket = $('#ticket_number').attr('data-isticket');
            $('#info').show();
            $('#taxSection').val(0);
            isticket == 0 ? $('#taxSection').show() : $('#taxSection').hide();
        }

        // Fonction pour montrer la section d'autres informations
        function showOtherInfoSection() {
            $('#other_info').show();
            let isticket = $('#ticket_number').attr('data-isticket');
            if (isticket == 1){ // i c'est un remboursement
                $('#selectType').val('EMD');
                $('#selectType').prop('disabled',true);
                $('#fee').hide();
            }
        }

        
    });

    

    $('#comment-ticket-cancel-button').on('click', function (){
        hideTicketInput();
        hideInfoSection();
        hideOtherInfoSection();
        $('#comment-ticket-cancel-button').hide();
        $('#comment-ticket-next-button').hide();
        $('#ticket_number').val("");
        $('#montant_hors_taxe').val("");
        $('#taxe').val("");
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

    Boutton.prop('disabled', ticket.length > 16 || ticket.length < 13);

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