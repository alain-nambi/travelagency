
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
            

            $.ajax({
                type: "POST",
                url: "/home/unorder-pnr",
                dataType: "json",
                data:{
                    pnr_number: pnr_number,
                    invoice_number: invoice_number,
                    motif: motif,
                    user_id: user_id,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: (response) => {
                    console.log(`response`, response);
                    $('#modalUncommandApi').modal('hide');
                    toastr.info(`PNR ${pnr_number} décommandé avec ${motif} comme motif`);
                    
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

$(document).ready(function() {
    function VerifMotifValue() {
      var motif = $('#motif').val();
      var Boutton = $('#sendRemovePassengerInvoice');

      if (motif.trim() === '') {
        Boutton.prop('disabled', true);
      } else {
        Boutton.prop('disabled', false);
      }
    }

    $('#motif').on('input', function() {
      VerifMotifValue();
    });

    $('#modalUncommandApi').on('shown.bs.modal', function() {
      VerifMotifValue();
    });

    $('#sendRemovePassengerInvoice').on('click', function() {
      toggleEnvoyerButton();
    });
  });
