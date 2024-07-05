// Test Parssage ---------------------------------------
$(document).ready(function () {
    const fileTestButton = document.getElementById('fileTestButton');
    var newTestButton = document.getElementById('NewTest');
    // Verify if we should show the textarea or the input file
    $(document).on('change', '#SelectTypeParsing', function () {
        if ($(this).val() == 'rd' || $(this).val() == 'ewa' ) {
            document.getElementById('input_file').hidden = false;
            document.getElementById('textarea').hidden = true;

        }
        else{
            document.getElementById('input_file').hidden = true;
            document.getElementById('textarea').hidden = false;

        }
    });

    // Upload file
    $(document).on('click', '#fileUploadButton', function() {
        const fileInput = $('#fileInput')[0];  
        const file = fileInput.files[0];
        
        // Create a FormData object and append the file and CSRF token
        const formData = new FormData();
        formData.append('file', file);
        formData.append('csrfmiddlewaretoken', csrftoken);

        $.ajax({
            type: "POST",
            url: "/tools/test-parsing-upload-file",
            data: formData,
            contentType: false,  // Set content type to false for FormData
            processData: false,  // Prevent jQuery from processing the data
            success: function (data) {
                
                if (data.status == 200) {

                    toastr.success('Fichier chargé');
                    
                    fileTestButton.hidden = false;
                } else {
                    toastr.error('Fichier non chargé');
                }
            }
        });
    });

    // Test PNR, TKT, TST (ALTEA)
    $(document).on('click', '#TestTextButton', function() {
        const error_console = document.getElementById('console');

        var data = $('#data').val();
        
        $.ajax({
            type: "POST",
            url: "/tools/test-parsing-text",
            dataType: "json",
            data: {
                data: data,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data.status == 200) {
                    toastr.success('Test réussi');
                    var pnr = data.pnr
                    // Afficher détails PNR
                    if (pnr) {
                        
                        var pnr_html = `<h2>Détails du PNR <a href="/home/pnr/${ pnr.id}"><h2>${pnr.number}</h2></a></h2>`;
                        $("pnr-data").html(pnr_html); // Mise à jour du contenu de la table
                        $("#pnr-data").html(pnr_html).trigger("update");
                        $('#pnr-data').prop('hidden', false);
                    }
                    var segments = data.segments
                    var tickets = data.tickets
            
                   
                    $('#segment-data').prop('hidden', false);
                    $('#ticket-data').prop('hidden', false);

                    var html = `<thead class="bg-info" id="thead-all-segment">
                        <tr >
                        <th>Segment</th>
                        <th>Vols</th> 
  
                        <th>Classe</th>
                        <th>Départ</th>
                        <th>Arrivée</th>
                        <th>Date et heure de départ</th>
                        <th>Date et heure d'arrivée</th>
                        </tr>
                      </thead>
                      <tbody >`;

                    // afficher la table des segments
                    segments.forEach(element => {
                        html +=`<tr>
                            <td>${ element.segmentorder }</td>
                            <td>${ element.segment }</td>
                            <td>${ element.flightclass }</td>
                            <td>${ element.codeorg }</td>
                            <td>${ element.codedest }</td>
                            <td>`

                            if (element.segment_state == 0) {
                                html += `${ element.departuretime} </td><td>`;
                            }else{
                                html += `${ element.departuretime} </td><td>`;
                            }

                            if (element.segment_state == 0) {
                                html += `${ element.arrivaltime} </td><td>`;
                            }else{
                                html += `Flown </td><td>`;
                            }
                             
                            if (pnr.status != 'Emis') {
                                html += `${ element.arrivaltime} </td></tr></tbody>`;
                            }
                            
                    });
                    
                    $("all-segment").html(html); // Mise à jour du contenu de la table
                    $("#all-segment").html(html).trigger("update");

                    // Afficher table des billets pour les tickets
                    var ticket_html = ``;
                    if (tickets.length > 0) {
                        ticket_html += `<thead class="bg-info" >
                            <tr >
                            <th>Type</th>
                            <th>Article</th> 
                            <th>Passager(s)/Trajet</th>
                            <th>Transport</th> 
                            <th>Taxe</th>
                            <th>Total</th>
                            <th>Passager/Segment(s)</th>
                            <th>Date d'émission</th>
                            </thead>
                            <tbody>`;

                            tickets.forEach(element => {
                                ticket_html += `<tr>
                                <td>${ element.type }</td>
                                <td>${ element.billet }</td>
                                <td>${ element.passager }</td>
                                <td>${ element.montant }</td>
                                <td>${ element.taxe }</td>
                                <td>${ element.total }</td>
                                <td>${ element.passenger_order }</td>
                                <td>${ element.issuing_date }</td>
                                </tr>`;
                                ticket_html += `<tr>
                                <td>Fee</td>
                                <td>${ element.fee_type }</td>
                                <td></td>
                                <td>${ element.fee_cost }</td>
                                <td>${ element.fee_taxe }</td>
                                <td>${ element.fee_total }</td>
                                <td></td>
                                <td>${ element.fee_issuing_date }</td>
                                <td></td>
                                </tr></tbody>`
                            });
                            
                    }
                    console.log('other fee : ',data.other_fee);

                    // Afficher table des billets pour les other_fee
                    if(data.other_fee){
                        other_fees = data.other_fee
                        console.log('other fee : ',other_fees);

                        console.log('tickets.length : ',tickets.length);
                        if (tickets.length <= 0) {
                            console.log('other fee : ',other_fees);
                            ticket_html += `<thead class="bg-info" >
                                <tr >
                                <th>Type</th>
                                <th>Article</th> 
                                <th>Passager(s)/Trajet</th>
                                <th>Transport</th> 
                                <th>Taxe</th>
                                <th>Total</th>
                                <th>Passager/Segment(s)</th>
                                <th>Date d'émission</th>
                                </thead>
                                <tbody>`;
    
                            other_fees.forEach(element => {
                                ticket_html += `<tr>
                                <td>${ element.type }</td>
                                <td>${ element.billet }</td>
                                <td>${ element.passager }</td>
                                <td>${ element.montant }</td>
                                <td>${ element.taxe }</td>
                                <td>${ element.total }</td>
                                <td>${ element.passenger_segment }</td>
                                <td>${ element.issuing_date }</td>
                                </tr>`;

                                ticket_html += `<tr>
                                    <td>Fee</td>
                                    <td>${ element.fee_type }</td>
                                    <td></td>
                                    <td>${ element.fee_cost }</td>
                                    <td>${ element.fee_taxe }</td>
                                    <td>${ element.fee_total }</td>
                                    <td></td>
                                    <td>${ element.fee_issuing_date }</td>
                                    <td></td>
                                    </tr></tbody>`;
                            });
                                
                        }
                    }else{
                        if(tickets.length <0){
                            ticket_html += `<h5 class="text-danger">Pas de billet</h5>`
                        }
                    }

                    $("all-ticket-test").html(ticket_html); // Mise à jour du contenu de la table
                    $("#all-ticket-test").html(ticket_html).trigger("update");

                    
                    newTestButton.hidden = false;

                } else {
                    error_console.hidden = false;
                    
                    // Show error
                    var error_list = data.error.split(',');
                    error_list.forEach(error => {
                        var paragraphe = document.createElement('p');
                        paragraphe.textContent = error;
                        error_console.appendChild(paragraphe);
                    });

                    newTestButton.hidden = false;
                        
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });

    });

    // reload page 
    $(document).on('click','#NewTest', function() {
        location.reload();
    });

    $(document).on('click','#NewTestZenith', function() {
        location.reload();
    });

    
});

$(document).ready(function () {
    const error_console = document.getElementById('console');
    var newTestButton = document.getElementById('NewTestZenith');
    var uploadButton = document.getElementById('fileUploadButton');
    var testButton = document.getElementById('fileTestButton');
    // TEST ZENITH
    $(document).on('click', '#fileTestButton', function() {
        
        const fileInput = $('#fileInput')[0];  
        const file = fileInput.files[0];
        $.ajax({
            type: "POST",
            url: "/tools/test-parsing-zenith",
            dataType: "json",
            data: {
                uploaded_file_name: file.name,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {  

                if (data.status == 200 || data.status == 122 ) {
                    toastr.success('Test réussi');
                    var pnr = data.pnr
                    // Afficher détails PNR
                    if (pnr) {
                        
                        var pnr_html = `<h2>Détails du PNR <a href="/home/pnr/${ pnr.id}"><h2>${pnr.number}</h2></a></h2>`;
                        $("pnr-data").html(pnr_html); // Mise à jour du contenu de la table
                        $("#pnr-data").html(pnr_html).trigger("update");
                        $('#pnr-data').prop('hidden', false);
                    }
                    var segments = data.segments
                    var tickets = data.tickets
            
                   
                    $('#segment-data').prop('hidden', false);
                    $('#ticket-data').prop('hidden', false);

                    var html = `<thead class="bg-info" id="thead-all-segment">
                      <tr >
                        <th>Segment</th>
                        <th>Vols</th> 
  
                        <th>Classe</th>
                        <th>Départ</th>
                        <th>Arrivée</th>
                        <th>Date et heure de départ</th>
                        <th>Date et heure d'arrivée</th>
                        </tr>
                      </thead>
                      <tbody >`;

                    // afficher la table des segments
                    segments.forEach(element => {
                        html +=`<tr>
                            <td>${ element.segmentorder }</td>
                            <td>${ element.segment }</td>
                            <td>${ element.flightclass }</td>
                            <td>${ element.codeorg }</td>
                            <td>${ element.codedest }</td>
                            <td>`

                            if (element.segment_state == 0) {
                                html += `${ element.departuretime} </td><td>`;
                            }else{
                                html += `${ element.departuretime} </td><td>`;
                            }

                            if (element.segment_state == 0) {
                                html += `${ element.arrivaltime} </td><td>`;
                            }else{
                                html += `Flown </td><td>`;
                            }
                             
                            if (pnr.status != 'Emis') {
                                html += `${ element.arrivaltime} </td></tr></tbody>`;
                            }
                            
                    });
                    $("all-segment").html(html); // Mise à jour du contenu de la table
                    $("#all-segment").html(html).trigger("update");

                    // Afficher table des billets pour les tickets
                    var ticket_html = ``;
                    if (tickets.length > 0) {
                        ticket_html += `<thead class="bg-info" >
                            <tr >
                            <th>Type</th>
                            <th>Article</th> 
                            <th>Passager(s)/Trajet</th>
                            <th>Transport</th> 
                            <th>Taxe</th>
                            <th>Total</th>
                            <th>Passager/Segment(s)</th>
                            <th>Date d'émission</th>
                            </thead>
                            <tbody>`;

                            tickets.forEach(element => {
                                ticket_html += `<tr>
                                <td>${ element.type }</td>
                                <td>${ element.billet }</td>
                                <td>${ element.passager }</td>
                                <td>${ element.montant }</td>
                                <td>${ element.taxe }</td>
                                <td>${ element.total }</td>
                                <td>${ element.passenger_order }</td>
                                <td>${ element.issuing_date }</td>
                                </tr>`;
                                ticket_html += `<tr>
                                <td>Fee</td>
                                <td>${ element.fee_type }</td>
                                <td></td>
                                <td>${ element.fee_cost }</td>
                                <td>${ element.fee_taxe }</td>
                                <td>${ element.fee_total }</td>
                                <td></td>
                                <td>${ element.fee_issuing_date }</td>
                                <td></td>
                                </tr></tbody>`
                            });
                            
                    }
                    console.log('other fee : ',data.other_fee);

                    // Afficher table des billets pour les other_fee
                    if(data.other_fee){
                        other_fees = data.other_fee
                        console.log('other fee : ',other_fees);

                        console.log('tickets.length : ',tickets.length);
                        if (tickets.length <= 0) {
                            console.log('other fee : ',other_fees);
                            ticket_html += `<thead class="bg-info" >
                                <tr >
                                <th>Type</th>
                                <th>Article</th> 
                                <th>Passager(s)/Trajet</th>
                                <th>Transport</th> 
                                <th>Taxe</th>
                                <th>Total</th>
                                <th>Passager/Segment(s)</th>
                                <th>Date d'émission</th>
                                </thead>
                                <tbody>`;
    
                                other_fees.forEach(element => {
                                    ticket_html += `<tr>
                                    <td>${ element.type }</td>
                                    <td>${ element.billet }</td>
                                    <td>${ element.passager }</td>
                                    <td>${ element.montant }</td>
                                    <td>${ element.taxe }</td>
                                    <td>${ element.total }</td>
                                    <td>${ element.passenger_segment }</td>
                                    <td>${ element.issuing_date }</td>
                                    </tr>`;

                                    ticket_html += `<tr>
                                    <td>Fee</td>
                                    <td>${ element.fee_type }</td>
                                    <td></td>
                                    <td>${ element.fee_cost }</td>
                                    <td>${ element.fee_taxe }</td>
                                    <td>${ element.fee_total }</td>
                                    <td></td>
                                    <td>${ element.fee_issuing_date }</td>
                                    <td></td>
                                    </tr></tbody>`
                                    });
                                
                        }
                    }else{
                        if(tickets.length <0){
                            ticket_html += `<h5 class="text-danger">Pas de billet</h5>`
                        }
                    }

                    $("all-ticket-test").html(ticket_html); // Mise à jour du contenu de la table
                    $("#all-ticket-test").html(ticket_html).trigger("update");

                    newTestButton.hidden = false;
                    uploadButton.hidden = true;
                    testButton.hidden = true;
                } else {
                    
                        //Show the traceback error on the div console in the page
                        error_console.hidden = false;

                        var error_list = data.error.split(',');
                        error_list.forEach(error => {
                            var paragraphe = document.createElement('p');
                            paragraphe.textContent = error;
                            error_console.appendChild(paragraphe);

                        });
                    newTestButton.hidden = false;
                    uploadButton.hidden = true;
                    testButton.hidden = true;
  
                }
            }
        });
    });
});
