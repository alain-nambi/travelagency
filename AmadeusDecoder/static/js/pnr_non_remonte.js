const AddTicketButton = document.querySelector('#addTicketButton');
const AddTicketButtonSection = document.getElementById('AddTicketButtonSection');
const ticketData = document.querySelector('#collapseTicketData');
const ticketDataFooter = document.querySelector('#ticketDataFooter');
const cancelAddTicketButton = document.querySelector('#CancelAddTicketButton');
const ConfirmAddTicketButton = document.querySelector('#ConfirmAddTicketButton');
const ticketList  = document.querySelector('#ticketList');
const generalFooter = document.querySelector('#generalFooter');

const PassengerDataFooter = document.querySelector('#PassengerDataFooter');
const AddPassengerButton = document.querySelector('#AddPassengerButton');
const CancelAddPassengerButton = document.querySelector('#CancelAddPassengerButton');
const passengerData = document.querySelector('#collapsePassengerData');
const passengerSelect = document.querySelector('#passengerSelect');
const ConfirmAddPassengerButton = document.querySelector('#ConfirmAddPassengerButton');

const AddSegmentButton = document.querySelector('#addSegmentButton');
const ConfirmAddSegmentButton = document.querySelector('#ConfirmAddSegmentButton');
const AddSegmentButtonDiv = document.querySelector('#addSegmentButtonDiv');

const AddMoreSegmentButton = document.querySelector('#addMoreSegmentButton');

const SegmentDataFooter = document.querySelector('#SegmentDataFooter');
const CancelAddSegmentButton = document.querySelector('#CancelAddSegmentButton');
const SegmentData = document.querySelector('#collapseSegmentData');
const selectSegment = document.querySelector('#selectSegment');
const SelectSegmentDiv = document.querySelector('#SelectSegmentDiv');
var dropdownOptions = document.querySelectorAll('.dropdown-option');
var dropdownList = document.querySelector('.dropdown-list');


const confirmAddPnrButton = document.querySelector('#ConfirmAddPnrButton');

const AddOtherFeeButton = document.querySelector('#AddOtherFeeButton');
const AddTicketButton2 = document.querySelector('#AddTicketButton2');

const pnrNumber = document.querySelector('#pnrNumber');
const ticketNumber = document.querySelector('#ticketNumber');
const ticketCost = document.querySelector('#ticketCost');
const ticketTax = document.querySelector('#ticketTax');
const unremountedPnrFeeSection = document.querySelector('#unremountedPnrFeeSection');

const flightNumber = document.querySelector('#flightNumber');
const segmentOrder = document.querySelector('#segmentOrder');
const airline = document.querySelector('#airline');

const PassengerName = document.querySelector('#PassengerName');
const PassengerOrder = document.querySelector('#PassengerOrder');

var checked=[];
var label = document.querySelector('.dropdown-label');

$(document).ready(function(){
    if(AddSegmentButton,SelectSegmentDiv, AddSegmentButtonDiv){
        //  check if there is segments data in the session storage
        // if there is, fill the segment select with it
        if('segments' in sessionStorage){
            AddSegmentButton.hidden = true;
            SelectSegmentDiv.hidden = false;

            var session_segments = JSON.parse(sessionStorage.getItem('segments'));
            session_segments.forEach(element => {
                var label = document.createElement('label');
                label.classList.add('dropdown-option'); // Ajouter la classe dropdown-option

                // Créer l'élément input
                var input = document.createElement('input');
                input.classList.add('dropdown-input');
                input.type = 'checkbox';
                input.name = 'dropdown-group';
                input.value = element['order']; // Définir la valeur

                input.addEventListener('click', ()=>{
                    console.log('input clicked ! : ',input);
                    
                    updateStatus(input.value);
                })

                // Ajouter l'élément input à l'élément label
                label.appendChild(input);

                // Créer un nœud texte pour le texte "Selection One"
                var textNode = document.createTextNode(element['order']);

                // Ajouter le nœud texte à l'élément label
                label.appendChild(textNode);
                dropdownList.appendChild(label);

            });
        }
        else{
            AddSegmentButtonDiv.hidden = false;
        }
    }


    // check if there is tickets data in the session storage
    // if there is, create the table to list the data
    if('tickets' in sessionStorage){
        let session_tickets = JSON.parse(sessionStorage.getItem('tickets'));
        
        // Create ticket table

        var html = `<table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Type</th>
                        <th>Numéro</th> 
                        <th>Montant</th> 
                        <th>Taxe</th> 
                        <th>Passager</th> 
                        <th>Segment</th> 
                      </tr>
                    </thead>
                    <tbody>`;
        session_tickets.forEach(ticket => {
            html += `<tr>
            <td>${ticket['ticketType']}</td>`;
            if (ticket['ticketNumber']) {s
                html += `<td>${ticket['ticketNumber']}</td>`;
            } else {
                html += `<td>${ticket['designation']}</td>`;
            }
            html += `<td>${ticket['ticketCost']}</td>
                        <td>${ticket['ticketTax']}</td>
                        <td class="ticket_passenger">${ticket['ticketPassenger']}</td>
                        <td class="ticket_segment">${ticket['ticketSegment']}</td>
                    </tr>`;
        
        });

        html += `</tbody>
        </table>`;

        $("#ticketTable").html(html);
        ticketList.hidden= false;
    }


    //  check if there is passengers data in the session storage
    // if there is, fill the passenger select with it
    if('passengers' in sessionStorage){
        let session_passengers = JSON.parse(sessionStorage.getItem('passengers'));
        // Ajouter les passagers contenu dans session storage en tant qu'option de selectSegment
        session_passengers.forEach(element => {
            var option = document.createElement('option');
            option.value = element['PassengerOrder']; // Définir la valeur de l'option
            option.text = element['PassengerName'] +" " +element['PassengerSurname'];
            passengerSelect.appendChild(option);
        });
    }

    $('#ticketType').on('change', ()=>{

        if($('#ticketType').val() == 'EMD'){
            unremountedPnrFeeSection.hidden = false;
        }
        else{
            unremountedPnrFeeSection.hidden = true;

        }
    })

})

if(pnrNumber, ticketNumber,ticketCost, ticketTax, PassengerName, flightNumber, segmentOrder, PassengerOrder, PassengerName, AddTicketButton, cancelAddTicketButton, AddPassengerButton, CancelAddPassengerButton, AddSegmentButton, AddMoreSegmentButton
    ,CancelAddSegmentButton, ConfirmAddSegmentButton,ConfirmAddPassengerButton,ConfirmAddTicketButton, confirmAddPnrButton)
{
    // Check PNR Number
    if(pnrNumber.value.trim() === ""){
        confirmAddPnrButton.disabled = true;
    }

    pnrNumber.addEventListener('keyup', function(event){
        if(pnrNumber.value.length == 6){
            confirmAddPnrButton.disabled = false;
        }
        else{
            confirmAddPnrButton.disabled = true;
        }
    })

    // check Ticket number
    if(ticketNumber.value.trim() === ""){
        ConfirmAddTicketButton.disabled = true;
    }
    if(ticketCost.value.trim() === ""){
        ConfirmAddTicketButton.disabled = true;
    }
    if(ticketTax.value.trim() === ""){
        ConfirmAddTicketButton.disabled = true;
    }

    ticketNumber.addEventListener('keyup', function(event){
        if (ticketNumber.type == 'number') {
            if(ticketNumber.value.length == 16 || ticketNumber.value.length == 13){
                ConfirmAddTicketButton.disabled = false;
            }
            else{
                ConfirmAddTicketButton.disabled = true;
            }
        }
        else{
            ConfirmAddTicketButton.disabled = false;
        }
        
    })
    
    if(PassengerName.value.trim() === "" || PassengerOrder.value.trim() ===""){
        ConfirmAddPassengerButton.disabled = true;
    }
    
    if(flightNumber.value.trim() === "" || segmentOrder.value.trim() ===""){
        ConfirmAddSegmentButton.disabled = true;
    }

    flightNumber.addEventListener('keyup', function(event){
        if(flightNumber.value.length >= 3 && segmentOrder.value.trim() !=""){
            ConfirmAddSegmentButton.disabled = false;
        }
        else{
            ConfirmAddSegmentButton.disabled = true;
        }
    })
    
    segmentOrder.addEventListener('keyup', function(event){
        if(flightNumber.value.length >= 3 && segmentOrder.value.trim() !=""){
            ConfirmAddSegmentButton.disabled = false;
        }
        else{
            ConfirmAddSegmentButton.disabled = true;
        }
    })
    
    PassengerOrder.addEventListener('keyup', function(event){
        if(PassengerOrder.value.trim() === ""){
            ConfirmAddPassengerButton.disabled = true;
        }
        if(PassengerOrder.value.trim() != "" && PassengerName.value.trim() != ""){
            ConfirmAddPassengerButton.disabled = false;
        }
    })
    
    PassengerName.addEventListener('keyup', function(event){
        if(PassengerName.value.trim() === ""){
            ConfirmAddPassengerButton.disabled = true;
        }
        if(PassengerOrder.value.trim() != "" && PassengerName.value.trim() != ""){
            ConfirmAddPassengerButton.disabled = false;
        }
    })

    AddOtherFeeButton.addEventListener('click', function(event){
        ticketLabel = document.getElementById('ticketLabelSection');
        ticketLabel.innerText = "Désignation";
        ticketNumber.type = 'text';

        AddTicketButton2.hidden = false;

        addTicketLabel = document.getElementById('AddTicketLabelSection');
        addTicketLabel.hidden=true;
        
        AddTicketButtonSection.hidden = false;
    })

    AddTicketButton.addEventListener('click', function(event){
        $('#collapseTicketData').collapse("show");
        generalFooter.hidden= true;
        ticketDataFooter.hidden = false;
    });

    AddTicketButton2.addEventListener('click', function(event){
        addTicketLabel = document.getElementById('AddTicketLabelSection');
        addTicketLabel.hidden=false;
        AddTicketButtonSection.hidden = true;

        AddTicketButton2.hidden = true;

        ticketLabel = document.getElementById('ticketLabelSection');
        ticketLabel.innerText = "Numéro du Billet";
        ticketNumber.type = 'number';
    })

    cancelAddTicketButton.addEventListener('click', function(event){
        closeTicketSection();
    });

    AddPassengerButton.addEventListener('click', function(event){
        $('#collapsePassengerData').collapse("show");
        generalFooter.hidden= true;
        PassengerDataFooter.hidden = false;
        ticketDataFooter.hidden = true;
        $(ticketData).collapse('hide');
    });

    CancelAddPassengerButton.addEventListener('click', function(event){
        closePassengerSection();
    }); 

    AddSegmentButton.addEventListener('click', function(event){
        showSegmentSection();
    });
    
    AddMoreSegmentButton.addEventListener('click', function(event){
        showSegmentSection();
    });
    
    CancelAddSegmentButton.addEventListener('click', function(event){
        closeSegmentSection();
    });

    // Add a new Segment on the Segment select and sock it in the session storage
ConfirmAddSegmentButton.addEventListener('click', function(event){
    
    var departureDate = $('#departureDate').val();
    var departureTime = $('#departureTime').val();
    var arrivalDate = $('#arrivalDate').val();
    var arrivalTime = $('#arrivalTime').val();
    var origin = $('#origin').val();
    var destination = $('#destination').val();
    var airline = $('#airline').val();
    var order = $('#segmentOrder').val();


    var Segment = {"airline":airline,"flightNumber":flightNumber.value,"order":order,"departureDate":departureDate,"departureTime":departureTime,"arrivalDate":arrivalDate,"arrivalTime":arrivalTime,"origin":origin,"destination":destination}
    
    // Effacer tous les option de selectSegment s'il y en a
    if (!selectSegment.hidden) {
        var labelElements = selectSegment.querySelectorAll('.dropdown-list label.dropdown-option');
    
        // Parcourez les éléments et supprimez chacun d'eux
        labelElements.forEach(function(label) {
            label.remove();
        });
        
    }

    // verifier si une liste de segment se trouve dans session storage
    if('segments' in sessionStorage){
        console.log("it's in the session storage" );
        let session_segments = JSON.parse(sessionStorage.getItem('segments'));
        session_segments.push(Segment);
        sessionStorage.setItem('segments', JSON.stringify(session_segments));

        // Ajouter les segment contenu dans session storage en tant qu'option de selectSegment
        session_segments.forEach(element => {  

            var label = document.createElement('label');
            label.classList.add('dropdown-option'); // Ajouter la classe dropdown-option

            // Créer l'élément input
            var input = document.createElement('input');
            input.classList.add('dropdown-input');
            input.type = 'checkbox';
            input.name = 'dropdown-group';
            input.value = element['order']; // Définir la valeur

            input.addEventListener('click', ()=>{
                console.log('input clicked ! : ',input);
                
                updateStatus(input.value);
            })

            // Ajouter l'élément input à l'élément label
            label.appendChild(input);

            // Créer un nœud texte pour le texte "Selection One"
            var textNode = document.createTextNode(element['order']);

            // Ajouter le nœud texte à l'élément label
            label.appendChild(textNode);
            dropdownList.appendChild(label);
        });


    }
    else{
        var segments = [];
        segments.push(Segment);
        // Ajouter une entrée au sessionStorage
        sessionStorage.setItem('segments', JSON.stringify(segments));

        var label = document.createElement('label');
        label.classList.add('dropdown-option'); // Ajouter la classe dropdown-option

        // Créer l'élément input
        var input = document.createElement('input');
        input.classList.add('dropdown-input');
        input.type = 'checkbox';
        input.name = 'dropdown-group';
        input.value = Segment['order']; // Définir la valeur

        input.addEventListener('click', ()=>{
            console.log('input clicked ! : ',input);
            
            updateStatus(input.value);
        })

        // Ajouter l'élément input à l'élément label
        label.appendChild(input);

        // Créer un nœud texte pour le texte "Selection One"
        var textNode = document.createTextNode(Segment['order']);

        // Ajouter le nœud texte à l'élément label
        label.appendChild(textNode);
        dropdownList.appendChild(label);
    }
    
    closeSegmentSection();
    AddSegmentButton.hidden = true;
    SelectSegmentDiv.hidden = false;
});

// Add a new Passenger on the passenger select and stock it in the session storage
ConfirmAddPassengerButton.addEventListener('click', function(event){
    var PassengerName = $('#PassengerName').val();
    var PassengerSurname = $('#PassengerSurname').val();
    var PassengerDesignation = $('#PassengerDesignation').val();
    var PassengerOrder = $('#PassengerOrder').val();
    var PassengerType = $('#PassengerType').val();
    var Passeport = $('#Passeport').val();

    var Passenger = {"PassengerName":PassengerName,"PassengerSurname":PassengerSurname,"PassengerDesignation":PassengerDesignation,"PassengerOrder":PassengerOrder,"PassengerType":PassengerType,"Passeport":Passeport}
    
    // Effacer tous les option de Passenger select s'il y en a
    
    if(!passengerSelect.hidden){
        var options = passengerSelect.options;
        for (var i = options.length - 1; i >= 0; i--) {
            passengerSelect.remove(i);
        }
    }
    


    // verifier si une liste de passagers se trouve dans session storage
    if('passengers' in sessionStorage){
        let session_passengers = JSON.parse(sessionStorage.getItem('passengers'));
        session_passengers.push(Passenger);
        sessionStorage.setItem('passengers', JSON.stringify(session_passengers));

        // Ajouter les passagers contenu dans session storage en tant qu'option de selectSegment
        session_passengers.forEach(element => {
            var option = document.createElement('option');
            option.value = element['PassengerOrder']; // Définir la valeur de l'option
            option.text = element['PassengerName'] +" " +element['PassengerSurname'];
            passengerSelect.appendChild(option);
        });
    }
    else{
        var passengers = [];
        passengers.push(Passenger);
        // Ajouter un passager au sessionStorage
        sessionStorage.setItem('passengers', JSON.stringify(passengers));

        var option = document.createElement('option');
        option.value = Passenger['PassengerOrder'] ; // Définir la valeur de l'option
        option.text = Passenger['PassengerName'] +" " +Passenger['PassengerSurname'];
        passengerSelect.appendChild(option);
    }
    
    closePassengerSection();

});

//  Add a new ticket and stock it in the session storage
ConfirmAddTicketButton.addEventListener('click', function(event){

    var ticketPassenger = $('#passengerSelect').val();
    var ticketSegment = checked;
    var fee = document.getElementById('feeSection');
    ticketLabel = document.getElementById('ticketLabelSection');

    var Ticket = {"ticket_type":0,"ticketNumber":ticketNumber.value,"ticketType":ticketType.value,"ticketCost":ticketCost.value,"ticketTax":ticketTax.value,"ticketPassenger":ticketPassenger,"ticketSegment":ticketSegment,fee:'True'}

    if (ticketType.value == 'EMD') {
        Ticket = {"ticket_type":0,"ticketNumber":ticketNumber.value,"ticketType":ticketType.value,"ticketCost":ticketCost.value,"ticketTax":ticketTax.value,"ticketPassenger":ticketPassenger,"ticketSegment":ticketSegment,fee:fee.checked}
    }

    if (ticketLabel.innerText == 'Désignation') {
        if (ticketType.value == 'EMD') {
            Ticket = {"ticket_type":1,"designation":ticketNumber.value,"ticketType":ticketType.value,"ticketCost":ticketCost.value,"ticketTax":ticketTax.value,"ticketPassenger":ticketPassenger,"ticketSegment":ticketSegment,fee:fee.checked}
        }
        else{
            Ticket = {"ticket_type":1,"designation":ticketNumber.value,"ticketType":ticketType.value,"ticketCost":ticketCost.value,"ticketTax":ticketTax.value,"ticketPassenger":ticketPassenger,"ticketSegment":ticketSegment,fee:fee.checked}
        }
    }
    
     
    // verifier si une liste de passagers se trouve dans session storage
    if('tickets' in sessionStorage){
        let session_tickets = JSON.parse(sessionStorage.getItem('tickets'));
        session_tickets.push(Ticket);
        sessionStorage.setItem('tickets', JSON.stringify(session_tickets));

        // Create ticket table

        var html = `<table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Type</th>
                        <th>Numéro</th> 
                        <th>Montant</th> 
                        <th>Taxe</th> 
                        <th>Passager</th> 
                        <th>Segment</th> 
                      </tr>
                    </thead>
                    <tbody>`;
        session_tickets.forEach(ticket => {
            html += `<tr>
            <td>${ticket['ticketType']}</td>`;
            if (ticket['ticketNumber']) {
                html += `<td>${ticket['ticketNumber']}</td>`;
            } else {
                html += `<td>${ticket['designation']}</td>`;
            }
            html += `<td>${ticket['ticketCost']}</td>
                        <td>${ticket['ticketTax']}</td>
                        <td class="ticket_passenger">${ticket['ticketPassenger']}</td>
                        <td class="ticket_segment">${ticket['ticketSegment']}</td>
                    </tr>`;
        });

        html += `</tbody>
        </table>`;

        $("#ticketTable").html(html);
        ticketList.hidden= false;

    }
    else{
        var tickets = [];
        tickets.push(Ticket);
        // Ajouter un passager au sessionStorage
        sessionStorage.setItem('tickets', JSON.stringify(tickets));

        // Create ticket table

        var html = `<table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Type</th>
                        <th>Numéro</th> 
                        <th>Montant</th> 
                        <th>Taxe</th> 
                        <th>Passager</th> 
                        <th>Segment</th> 
                      </tr>
                    </thead>
                    <tbody>`;
                    tickets.forEach(ticket => {
                        html += `<tr>
                                <td>${ticket['ticketType']}</td>`;
                    if (ticket['ticketNumber']) {
                        console.log(ticket['ticketNumber']);

                        html += `<td>${ticket['ticketNumber']}</td>`;
                    } else {
                        console.log(ticket['desigantion']);

                        html += `<td>${ticket['designation']}</td>`;
                    }
                    html += `<td>${ticket['ticketCost']}</td>
                                <td>${ticket['ticketTax']}</td>
                                <td>${ticket['ticketPassenger']}</td>
                                <td>${ticket['ticketSegment']}</td>
                            </tr>`;
        });

        html += `</tbody>
        </table>`;

        $("#ticketTable").html(html);
        ticketList.hidden= false;
    }

    
    closeTicketSection();
});

// Save everything in the database
confirmAddPnrButton.addEventListener('click', function(event){
    
    var pnrType = $('#pnrType').val();

    var tickets = "";
    var passengers = "";
    var segments = "";
    var user_id = $('#user_id').val();

    if('tickets' in sessionStorage){
        tickets = JSON.parse(sessionStorage.getItem('tickets'));
    }

    if('passengers' in sessionStorage){
        passengers = JSON.parse(sessionStorage.getItem('passengers'));
    }

    if('segments' in sessionStorage){
        segments = JSON.parse(sessionStorage.getItem('segments'));
    }

    $.ajax({
        type: "POST",
        url : "/home/pnr-non-remonte",
        dataType : "json",
        data : {
            pnrNumber: pnrNumber.value,
            pnrType: pnrType,
            passengers: JSON.stringify(passengers),
            segments: JSON.stringify(segments),
            tickets: JSON.stringify(tickets),
            user_id: user_id,
            csrfmiddlewaretoken: csrftoken
        },
        success : (response) => {
            toastr.success(response.message);

            // Effacer le contenu du sessionStorage
            sessionStorage.clear();
            checked = [];
            location.reload();

        },
        error : (response) =>{
            toastr.error(response);
        }
    });

});
}


function closeTicketSection(){
    $(ticketData).collapse('hide');
    generalFooter.hidden= false;
    ticketDataFooter.hidden = true;
}


function closePassengerSection(){
    $(passengerData).collapse('hide');
    generalFooter.hidden= true;
    PassengerDataFooter.hidden = true;
    ticketDataFooter.hidden = false;
    $(ticketData).collapse('show');
}

function showSegmentSection(){
    $('#collapseSegmentData').collapse('show');
    SegmentDataFooter.hidden = false;
    generalFooter.hidden= true;
    ticketDataFooter.hidden = true;
    $(ticketData).collapse('hide');
}

function closeSegmentSection(){
    $(SegmentData).collapse('hide');
    $(ticketData).collapse('show');
    SegmentDataFooter.hidden = true;
    ticketDataFooter.hidden = false;
}

function acceptToRemountPnr(unremountedPnrId){

    var ticketIds = []
    // obtenir les tickets cochés
    $('.ticketCheck').each(function() {
        // Vérifiez si la case à cocher est cochée ou non
        if ($(this).prop('checked')) {
            // Si la case est cochée, faites quelque chose avec la ligne associée
            var ligne = $(this).closest('tr');
            ticketIds.push(ligne.attr('data-ticket-id'))
        } 
    });

    console.log('ticket ids',ticketIds);

    $.ajax({
        type: 'POST',
        url : '/anomaly/accept/unremounted-pnr',
        dataType : 'json',
        data : {
            ticketIds : JSON.stringify(ticketIds),
            unremountedPnrId : unremountedPnrId,
            csrfmiddlewaretoken : csrftoken
        },
        success : (response) => {
            toastr.success(response.message);
            location.reload();
        },
        error : (response) => {
            toastr.error(response.message);
        }
    })
}

function refuseToRemountPnr(unremountedPnrId) {
    $.ajax({
        type: 'POST',
        url : '/anomaly/refuse/unremounted-pnr',
        dataType : 'json',
        data : {
            unremountedPnrId : unremountedPnrId,
            csrfmiddlewaretoken : csrftoken
        },
        success : (response) => {
            toastr.success(response.message);
            location.reload();
        },
        error : (response) => {
            toastr.error(response.message);
        }
    })
}

// ------------------------- MULTI SELECT ------------------------------------------------

// create a select dropdown
class CheckboxDropdown {
    constructor(el) {
        var _this = this;
        this.isOpen = false;
        this.areAllChecked = false;
        this.$el = $(el);
        this.$label = this.$el.find('.dropdown-label');
        this.$checkAll = this.$el.find('[data-toggle="check-all"]').first();
        this.$inputs = this.$el.find('.dropdown-input');
        this.$inputs.each(function() {
            console.log('inputs:', $(this).val()); // Afficher la valeur de chaque élément
        });

        this.onCheckBox();

        this.$label.on('click', function (e) {
            console.log('coucou1');
            e.preventDefault();
            _this.toggleOpen();
        });

        this.$checkAll.on('click', function (e) {
            console.log('coucou2');
            e.preventDefault();
            _this.onCheckAll();
        });

        this.$inputs.on('change', function (e) {
            console.log('coucou3');
            _this.onCheckBox();
        });
    }
    onCheckBox() {
        console.log('box checked');
        this.updateStatus();
    }
    updateStatus() {
        var checked = this.$el.find(':checked');
        var selectedValues = [];

        this.areAllChecked = false;
        this.$checkAll.html('Check All');

        if (checked.length <= 0) {
            this.$label.html('Select Options');
        }
        else if (checked.length === 1) {
            console.log('One option checked');
            console.log('checked : ', checked.parent('label').text());
            this.$label.html(checked.parent('label').text());
        }
        else if (checked.length === this.$inputs.length) {
            this.$label.html('All Selected');
            this.areAllChecked = true;
            this.$checkAll.html('Uncheck All');
        }
        else {
            console.log('--ELSE--');
            console.log('chedcked : ', $(this).parent('label').text().trim());
            checked.each(function () {
                selectedValues.push($(this).parent('label').text().trim());
            });
            this.$label.html(selectedValues.join(', '));
        }
    }


    onCheckAll(checkAll) {
        if (!this.areAllChecked || checkAll) {
            this.areAllChecked = true;
            this.$checkAll.html('Uncheck All');
            this.$inputs.prop('checked', true);
        }
        else {
            this.areAllChecked = false;
            this.$checkAll.html('Check All');
            this.$inputs.prop('checked', false);
        }

        this.updateStatus();
    }
    toggleOpen(forceOpen) {
        var _this = this;

        if (!this.isOpen || forceOpen) {
            this.isOpen = true;
            this.$el.addClass('on');
            $(document).on('click', function (e) {
                if (!$(e.target).closest('[data-control]').length) {
                    _this.toggleOpen();
                }
            });
        }
        else {
            this.isOpen = false;
            this.$el.removeClass('on');
            $(document).off('click');
        }
    }
}
    var is_open = false;
    var areAllChecked = false;

    
    console.log('labelsss : ', label);
    var checkAll = document.querySelector('[data-toggle="check-all"]');

var checkboxesDropdowns = document.querySelectorAll('[data-control="checkbox-dropdown"]');
for(var i = 0, length = checkboxesDropdowns.length; i < length; i++) {
    new CheckboxDropdown(checkboxesDropdowns[i]);

}

// Update the lobel of the select dropdown S1,S2 / S1,S3,S2
function updateStatus(input_value){
    var selectedValues = []
    var new_checked_value = []

    if (!checked.includes(input_value.toString().trim())) {
        checked.push(input_value.toString().trim());
    }
    else{
        checked.forEach(element => {
            if (element != input_value.toString().trim()) {
                new_checked_value.push(element)
            }
        });
        checked = new_checked_value;
    }
    
    if (checked.length <=0) {
        label.innerHTML = "Selectionner un Segment";
    }
    else if (checked.length === 1) {
        label.innerHTML = checked[0];
    }
    else{
        checked.forEach(element => {
            selectedValues.push(element);
        });

        label.innerHTML = selectedValues;
    }
}

$('.ticket_segment').addEventListener('click', function(event){

    if('segments' in sessionStorage){
        let session_segments = JSON.parse(sessionStorage.getItem('segments'));
        
        // Create ticket table
    
        var html = `<table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Ordre</th>
                        <th>Vol</th> 
                        <th>date Départ</th> 
                        <th>date d'Arriée</th> 
                        <th>Origine</th> 
                        <th>Destination</th> 
                      </tr>
                    </thead>
                    <tbody>`;
        session_segments.forEach(segment => {
            html += `<tr>
            <td>${segment['order']}</td>
            <td>${segment['airline']} ${segment['flightNumber']}</td>
            <td>${segment['departureDate']} ${segment['departureTime']}</td>
            <td>${segment['arrivalDate']} ${segment['arrivalTime']}</td>
            <td>${segment['origin']}</td>
            <td>${segment['destination']}</td>
            </tr>`;
    
        });
    
        html += `</tbody>
        </table>`;
    
        $("#segmentTable").html(html);
        segmentList.hidden= false;
    }

});

$('.ticket_passenger').addEventListener('click', function(event){

    if('passengers' in sessionStorage){
        let session_passengers = JSON.parse(sessionStorage.getItem('passengers'));
        
        // Create ticket table
    
        var html = `<table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Ordre</th>
                        <th>Désignation</th> 
                        <th>Nom</th>
                        <th>Type</th> 
                      </tr>
                    </thead>
                    <tbody>`;
        session_passengers.forEach(passenger => {
            html += `<tr>
            <td>${passenger['order']}</td>
            <td>${passenger['PassengerDesignation']}</td>
            <td>${passenger['PassengerName']} ${passenger['PassengerSurname']}</td>
            <td>${passenger['PassengerOrder']}</td>
            <td>${passenger['PassengerType']}</td>
            </tr>`;
    
        });
    
        html += `</tbody>
        </table>`;
    
        $("#passengerTable").html(html);
        passengerList.hidden= false;
    }

});

