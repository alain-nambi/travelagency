const AddTicketButton = document.querySelector('#addTicketButton');
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

const confirmAddPnrButton = document.querySelector('#ConfirmAddPnrButton');


const pnrNumber = document.querySelector('#pnrNumber');
const ticketNumber = document.querySelector('#ticketNumber');
const ticketCost = document.querySelector('#ticketCost');
const ticketTax = document.querySelector('#ticketTax');

const flightNumber = document.querySelector('#flightNumber');
const segmentOrder = document.querySelector('#segmentOrder');

$(document).ready(function(){
    //  check if there is segments data in the session storage
    // if there is, fill the segment select with it
    if('segments' in sessionStorage){
        AddSegmentButton.hidden = true;
        SelectSegmentDiv.hidden = false;

        var session_segments = JSON.parse(sessionStorage.getItem('segments'));
        session_segments.forEach(element => {
            var option = document.createElement('option');
            option.value = element['order']; // Définir la valeur de l'option
            option.text = element['order'];
            selectSegment.appendChild(option);

        });
    }
    else{
        AddSegmentButtonDiv.hidden = false;
    }

    // check if there is tickets data in the session storage
    // if there is, create the table to list the data
    if('tickets' in sessionStorage){
        let session_tickets = JSON.parse(sessionStorage.getItem('tickets'));
        CreateTicketTable(session_tickets);
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

    


})

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
    if(ticketNumber.value.length == 16 || ticketNumber.value.length == 13){
        ConfirmAddTicketButton.disabled = false;
    }
    else{
        ConfirmAddTicketButton.disabled = true;
    }
})

if(flightNumber.value.trim() === "" || segmentOrder.value.trim() ===""){
    ConfirmAddSegmentButton.disabled = true;
}
else{
    ConfirmAddSegmentButton.disabled = false;
}

flightNumber.addEventListener('keyup', function(event){
    if(flightNumber.value.length >= 3 && segmentOrder.value.trim() !=""){
        ConfirmAddSegmentButton.disabled = false;
    }
    else{
        ConfirmAddSegmentButton.disabled = true;
    }
})


AddTicketButton.addEventListener('click', function(event){
    generalFooter.hidden= true;
    ticketDataFooter.hidden = false;
});

function closeTicketSection(){
    $(ticketData).collapse('hide');
    generalFooter.hidden= false;
    ticketDataFooter.hidden = true;
}

cancelAddTicketButton.addEventListener('click', function(event){
    closeTicketSection();
});

AddPassengerButton.addEventListener('click', function(event){
    generalFooter.hidden= true;
    PassengerDataFooter.hidden = false;
    ticketDataFooter.hidden = true;
    $(ticketData).collapse('hide');
});

function closePassengerSection(){
    $(passengerData).collapse('hide');
    generalFooter.hidden= true;
    PassengerDataFooter.hidden = true;
    ticketDataFooter.hidden = false;
    $(ticketData).collapse('show');
}

CancelAddPassengerButton.addEventListener('click', function(event){
    closePassengerSection();
}); 

function showSegmentSection(){
    SegmentDataFooter.hidden = false;
    generalFooter.hidden= true;
    ticketDataFooter.hidden = true;
    $(ticketData).collapse('hide');
}

AddSegmentButton.addEventListener('click', function(event){
    showSegmentSection();
});

AddMoreSegmentButton.addEventListener('click', function(event){
    showSegmentSection();
});

CancelAddSegmentButton.addEventListener('click', function(event){
    closeSegmentSection();
});

function closeSegmentSection(){
    $(SegmentData).collapse('hide');
    $(ticketData).collapse('show');
    SegmentDataFooter.hidden = true;
    ticketDataFooter.hidden = false;
}

// Add a new Segment on the Segment select and sock it in the session storage
ConfirmAddSegmentButton.addEventListener('click', function(event){
    
    var departureDate = $('#departureDate').val();
    var departureTime = $('#departureTime').val();
    var arrivalDate = $('#arrivalDate').val();
    var arrivalTime = $('#arrivalTime').val();
    var origin = $('#origin').val();
    var destination = $('#destination').val();

    var Segment = {"flightNumber":flightNumber,"order":order,"departureDate":departureDate,"departureTime":departureTime,"arrivalDate":arrivalDate,"arrivalTime":arrivalTime,"origin":origin,"destination":destination}
    
    // Effacer tous les option de selectSegment s'il y en a
    if (!selectSegment.hidden) {
        var options = selectSegment.options;
        for (var i = options.length - 1; i >= 0; i--) {
            selectSegment.remove(i);
        }
        
    }

    // verifier si une liste de segment se trouve dans session storage
    if('passengers' in sessionStorage){
        console.log("it's in the session storage" );
        let session_segments = JSON.parse(sessionStorage.getItem('segments'));
        session_segments.push(Segment);
        sessionStorage.setItem('segments', JSON.stringify(session_segments));

        // Ajouter les segment contenu dans session storage en tant qu'option de selectSegment
        session_segments.forEach(element => {
            var option = document.createElement('option');
            option.value = element['order']; // Définir la valeur de l'option
            option.text = element['order'];
            selectSegment.appendChild(option);
        });
    }
    else{
        var segments = [];
        segments.push(Segment);
        // Ajouter une entrée au sessionStorage
        sessionStorage.setItem('segments', JSON.stringify(segments));

        var option = document.createElement('option');
        option.value = Segment['order']; // Définir la valeur de l'option
        option.text = Segment['order'];
        selectSegment.appendChild(option);
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
    var ticketSegment = $('#selectSegment').val();
    

    var Ticket = {"ticketNumber":ticketNumber,"ticketType":ticketType,"ticketCost":ticketCost,"ticketTax":ticketTax,"ticketPassenger":ticketPassenger,"ticketSegment":ticketSegment}
    
    // verifier si une liste de passagers se trouve dans session storage
    if('tickets' in sessionStorage){
        let session_tickets = JSON.parse(sessionStorage.getItem('tickets'));
        session_tickets.push(Ticket);
        sessionStorage.setItem('tickets', JSON.stringify(session_tickets));

        CreateTicketTable(session_tickets);

    }
    else{
        var tickets = [];
        tickets.push(Ticket);
        // Ajouter un passager au sessionStorage
        sessionStorage.setItem('tickets', JSON.stringify(tickets));

        CreateTicketTable(tickets);

    }

    
    closeTicketSection();
});

// Create the table who contains the list of all the added ticket
function CreateTicketTable(session_tickets){
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
        session_tickets.forEach(tickets => {
            html += `<tr>
                    <td>${tickets['ticketType']}</td>
                    <td>${tickets['ticketNumber']}</td>
                    <td>${tickets['ticketCost']}</td>
                    <td>${tickets['ticketTax']}</td>
                    <td>${tickets['ticketPassenger']}</td>
                    <td>${tickets['ticketSegment']}</td>
            </tr>`;
        });

        html += `</tbody>
        </table>`;

        $("#ticketTable").html(html);
        ticketList.hidden= false;
}

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
            pnrNumber: pnrNumber,
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
            location.reload();

        },
        error : (response) =>{
            toastr.error(response);
        }
    });

});
