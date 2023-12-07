
function updateSelectOptions(numeroPnr) {
    const parent = document.getElementById("selectNumCommande");
                        
    const child = document.getElementById("child_commande");
        if (child) {
            parent.removeChild(child);
        }
                        
        if (numeroPnr.length === 0) {
            document.getElementById("selectNumCommande").innerHTML = "";
                return;
        } else {
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.onreadystatechange = function () {
                
                if (this.readyState == 4 && this.status == 200) {
                                            
                var response = JSON.parse(this.responseText);

                const invoices = Array.from(response.invoices)

                invoices.map((invoice) => {
                    const newOption = document.createElement("option");
                    newOption.id = "child_commande";
                    newOption.value = invoice;
                    newOption.textContent = invoice;
                    parent.append(newOption);
                })
            }
        };
        xmlhttp.open("GET", '/home/get-invoice-number-to-uncommand/' + numeroPnr, true);
        xmlhttp.send();

    }
}

    $('#modalUncommandApi').on('show.bs.modal', function(){
        const numeroPnr = document.getElementById('pnr_number').value;
        updateSelectOptions(numeroPnr);
    });

const sendRemovePassengerInvoice = document.getElementById("sendRemovePassengerInvoice")
if (sendRemovePassengerInvoice) {
    sendRemovePassengerInvoice.addEventListener("click", () => {

    try {
    const pnr_number = (document.getElementById('pnr_number')).value;
    const invoice_number = (document.getElementById('selectNumCommande')).value;
    console.log(pnr_number);
    console.log(invoice_number);

    $.ajax({
        type: 'GET',
        url: '/home/server',
        success: (response) => {
            console.log(response);

            // Utilisation de setTimeout pour ajouter un délai avant le deuxième appel AJAX
            setTimeout(() => {
                const hostname = "http://localhost:1000/api/pnr_unorder";
                $.ajax({
                    type: "POST",
                    url: hostname,
                    dataType: "json",
                    contentType: "application/json",
                    data: JSON.stringify({
                        pnrNumber: pnr_number,
                        invoiceNumber: invoice_number
                    }),
                    success: (response) => {
                        console.log(`response`, response);
                        $('#modalUncommandApi').modal('hide');
                        location.reload();
                        toastr.info(`PNR ${pnr_number} décommandé!`);

                    },
                    error: (error) => {
                        console.log(`error`, error);
                    }
                });
            }, 5000); // 5000 milliseconds équivalent à 5 secondes
        },
        error: (response) => {
            console.log(response);
        }
    });
} catch (error) {
    console.log(`error`, error);
}

    })
}

