const AddTicketButton = document.querySelector('#addTicketButton');
const ticketData = document.querySelector('#ticket_data');

AddTicketButton.addEventListener('click', function(event){
    ticketData.hidden = false;
});