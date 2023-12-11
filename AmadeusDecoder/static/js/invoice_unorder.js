
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

                parent.innerHTML = ''
                
                invoices.map((invoice) => {
                    const newOption = document.createElement("option");
                    newOption.id = "child_commande";
                    newOption.value = invoice;
                    newOption.textContent = invoice;

                    // init parent HTML 
                    parent.append(newOption);
                })
            }
        };
        xmlhttp.open("GET", '/home/get-invoice-number-to-uncommand/' + numeroPnr, true);
        xmlhttp.send();

    }
}

    $('#modalUncommandApi').on('show.bs.modal', function(){
        const numeroPnr = document.getElementById('pnr_number');
        if (numeroPnr) {
            updateSelectOptions(numeroPnr.value);
        }
    });

const sendRemovePassengerInvoice = document.getElementById("sendRemovePassengerInvoice")
if (sendRemovePassengerInvoice) {
    sendRemovePassengerInvoice.addEventListener("click", () => {
        try {
            const pnr_number = (document.getElementById('pnr_number')).value;
            const invoice_number = (document.getElementById('selectNumCommande')).value;
            const motif = (document.getElementById('motif')).value;
            const user_id = (document.getElementById('user_id')).value;
            // console.log(pnr_number);
            // console.log(invoice_number);

            const hostname = "http://localhost:1000/api/pnr_unorder";
            $.ajax({
                type: "POST",
                url: hostname,
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify({
                    pnrNumber: pnr_number,
                    invoiceNumber: invoice_number,
                    motif: motif,
                    user_id: user_id,
                }),
                success: (response) => {
                    console.log(`response`, response);
                    $('#modalUncommandApi').modal('hide');
                    toastr.info(`PNR ${pnr_number} décommandé avec ${motif}comme motif`);
                    
                    setTimeout(() => {
                        location.reload();
                    }, 1000)
                },
                error: (error) => {
                    console.log(`error`, error);
                }
            });
        } catch (error) {
            console.log(`error`, error);
        }
    })
}

