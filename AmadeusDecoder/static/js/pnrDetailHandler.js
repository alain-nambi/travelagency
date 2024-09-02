
const ServiceFeesInput = document.querySelectorAll(
  ".inputeditable.montant.fee-cost"
);
const MontantTotal = document.getElementById("pnr-amount-total");
const AmoutTicket = document.querySelectorAll(".montant.ticket");
const CreateOrder = document.getElementById("create-final-command");
const pnrIdNew = window.location.pathname.split("/").reverse()[1];
const passengerCheckbox = document.getElementsByName("passagers-checkbox");
const RfeCde = document.getElementById("ref_cde");
const spanCustomerDefaultData = document.querySelectorAll(".customer-default");
const customerDefault = document.getElementById("customerDefault");
const customerListSelection = document.getElementById("customer-list");
const passengers = document.getElementsByName("passengers-ids");
const TotalServicesFees = document.getElementById("total-services-fees");
const reduceFeeRequest = document.getElementById("submitFeeRequest");

const feeReduceMotif = document.getElementById("feeReduceMotif");
const submitFeeRequest = document.getElementById("submitFeeRequest");

// We block submitFeeRequest button first
submitFeeRequest.setAttribute("disabled", true);

// If feeReduceMotif is not empty, we allow click on submitFeeRequest button
if (feeReduceMotif != null) {
  feeReduceMotif.addEventListener("input", (e) => {
    if (e.target.value.trim() == "") {
      submitFeeRequest.setAttribute("disabled", true);
    } else {
      submitFeeRequest.removeAttribute("disabled");
    }
  });
}

let passenger = [];

passengers.forEach((item) => {
  passenger.push(item.value);
});

//Handling amout total calculation
////////
ServiceFeesInput.forEach((inputFees, index) => {
    inputFees.addEventListener('change', (e) => {
        // console.log(inputFees.parentElement.parentElement.parentElement.children[5].children[0]);
        // const InputTicketTotal = inputFees.parentElement.parentElement.parentElement.children[5].children[0];
        let role_id = e.target.getAttribute('data-role-id');
        let user_id = e.target.getAttribute('data-user-id');
        let cost = parseFloat(e.target.value) || 0;
        let fee_id = e.target.getAttribute('data-fee-id');
        // InputTicketTotal.textContent = cost.toFixed(2);
        // console.log($(".montant.fee-total")[index]);
        allAmountTicket[index].textContent = cost.toFixed(2);
        let currentCost = e.target.getAttribute('old-data-cost');
        let inputCurrentCost = e.target.getAttribute('data-cost');
        let is_at_airport = e.target.getAttribute('is-at-airport');

        // console.log(role_id, currentCost, cost);

        if (currentCost <= cost || is_at_airport == 'True') {
            let TicketAmoutTotal = 0;
            AmoutTicket.forEach((ticket) => {
                const TicketTotal = parseFloat(ticket.textContent);
                TicketAmoutTotal += TicketTotal;
            });
            document.querySelectorAll('.tr-fee').forEach((td) => {
                TicketAmoutTotal += parseFloat(td.children[5].children[0].textContent);
            })
            MontantTotal.textContent = TicketAmoutTotal.toFixed(2);
        }
        if ((currentCost >= cost && user_id == 13) || (currentCost >= cost && user_id == 22) || (currentCost >= cost && user_id == 15) || (currentCost >= cost && role_id == 1)) {
            let TicketAmoutTotal = 0;
            AmoutTicket.forEach((ticket) => {
                const TicketTotal = parseFloat(ticket.textContent);
                TicketAmoutTotal += TicketTotal;
            });
            document.querySelectorAll('.tr-fee').forEach((td) => {
                TicketAmoutTotal += parseFloat(td.children[5].children[0].textContent);
            })
            MontantTotal.textContent = TicketAmoutTotal.toFixed(2);
        }
        if (currentCost >= cost && user_id != 13 && user_id != 22 && user_id != 15 && role_id != 1) {
                inputFees.value = inputCurrentCost;
                $('#modal-dmdfrs').modal();
                $('#user_id').val(user_id);
                $('.fee-request').val(cost.toFixed(2));
                $('.fee-total').text(inputCurrentCost);
                $('#fee-id-request').val(fee_id);
                $('#fee-origin-cost').val(inputCurrentCost);
                $("#feeRequestAlert").attr("style", "display: none !important")
            
            
        }
    })
});
//////////

//=====================  CREATE ORDER PROCESSING ========================>
// Block Create Order Button if there is no check checkbox
const confirmationCustomerCheckbox = document.querySelectorAll(
  ".confirmation-customer-checkbox"
);
const totalAmountPerCheckboxChecked = document.getElementById(
  "totalAmountPerCheckboxChecked"
);
const spanTotalAmountPerCheckboxChecked = document.getElementById(
  "spanTotalAmountPerCheckboxChecked"
);
const totalAmountOrder = totalAmountPerCheckboxChecked.getAttribute(
  "data-total-amount-order"
);
const EachAmount =
  JSON.parse(
    totalAmountPerCheckboxChecked.getAttribute("data-each-amount-order")
  ) || [];

let totalAmount = EachAmount.reduce((sum, item) => sum + item.total, 0);

// We init checkbox checked to 0
let confirmationCustomerCheckboxChecked = 0;

// We add countDeDuplicateCustomer to remove all duplicated customer ID
let countDeDuplicatedCustomer = [];

let listCustomerIds = [];

const checkPassengerMissing = document.querySelector("#checkPassengerMissing")
const confirmationClientOrderCheckBox = document.querySelectorAll("#ConfirmationCustomerOrderCheckbox")
// We reset all values
const resetAmountValues = () => {
  let countPassengerMissing = 0
  confirmationClientOrderCheckBox.forEach((checkBox) => {
    if (parseInt(checkBox.getAttribute("data-count-passenger-missing")) > 0 && !checkBox.disabled) {
      countPassengerMissing += 1
    } 
  })

  // console.log(countPassengerMissing);
  
  // We block CreateOrder button if confirmationCustomerCheckboxChecked equals to 0
  // And remove totalAmountPerCheckboxChecked
  if (confirmationCustomerCheckboxChecked == 0 || countPassengerMissing > 0) {
    CreateOrder.setAttribute("disabled", true);
    totalAmountPerCheckboxChecked.setAttribute("hidden", true);
  } else {
    CreateOrder.removeAttribute("disabled");
    totalAmountPerCheckboxChecked.removeAttribute("hidden");
  }
};

// We set confirmationCustomerCheckboxChecked equals length of countDeDuplicatedCustomer
const resetAmountTotalValue = () => {
  confirmationCustomerCheckbox.forEach((checkBox) => {
    // We don't count the disabled checkbox
    if (!checkBox.disabled) {
      if (
        !countDeDuplicatedCustomer.includes(
          checkBox.getAttribute("data-customer-id")
        )
      ) {
        countDeDuplicatedCustomer.push(
          checkBox.getAttribute("data-customer-id")
        );
      }

      if (checkBox.checked && !checkBox.disabled) {
        confirmationCustomerCheckboxChecked = countDeDuplicatedCustomer.length;

        spanTotalAmountPerCheckboxChecked.textContent = totalAmount.toFixed(2);

        let customerId = checkBox.getAttribute("data-customer-id");
        if (!listCustomerIds.includes(customerId)) {
          listCustomerIds.push(customerId);
        }
        localStorage.setItem(
          "listCustomerIdsAfterChecked",
          JSON.stringify(listCustomerIds)
        );
      } else if (!checkBox.checked && !checkBox.disabled) {
        localStorage.setItem("listCustomerIdsAfterChecked", JSON.stringify([]));
      }

      checkBox.checked = true;

      // If there is any disabled checkbox then we decrement confirmationCustomerCheckboxChecked value
      checkBox.disabled
        ? confirmationCustomerCheckboxChecked--
        : confirmationCustomerCheckboxChecked + 0;
    }
  });
};

resetAmountTotalValue();

confirmationCustomerCheckbox.forEach((checkBox) => {
  checkBox.addEventListener("change", (e) => {
    if (checkBox.checked && !checkBox.disabled) {
      confirmationCustomerCheckboxChecked++;
      checkBox.setAttribute("checked", true);

      let customerId = checkBox.getAttribute("data-customer-id");

      if (!listCustomerIds.includes(customerId)) {
        listCustomerIds.push(customerId);
      }

      localStorage.setItem(
        "listCustomerIdsAfterChecked",
        JSON.stringify(listCustomerIds)
      );

      totalAmountFromLocalStorage();
    } else {
      confirmationCustomerCheckboxChecked--;

      let listCustomerIdsAfterChecked = [];
      let valueToRemove = checkBox.getAttribute("data-customer-id");

      listCustomerIdsAfterChecked = listCustomerIds.reduce((acc, item) => {
        if (item !== valueToRemove) {
          acc.push(item);
        }
        return acc;
      }, []);

      let customerId = checkBox.getAttribute("data-customer-id");

      let index = listCustomerIds.findIndex((item) => item == customerId);

      let NumberOfElementToRemove =
        countDeDuplicatedCustomer.length - confirmationCustomerCheckboxChecked;

      listCustomerIds.splice(index, NumberOfElementToRemove);

      localStorage.setItem(
        "listCustomerIdsAfterChecked",
        JSON.stringify(listCustomerIdsAfterChecked)
      );

      totalAmountFromLocalStorage();
    }

    if (confirmationCustomerCheckboxChecked == 0) {
      localStorage.setItem("listCustomerIdsAfterChecked", JSON.stringify([]));
    }
    resetAmountValues();

    function totalAmountFromLocalStorage() {
      let listCustomerIdsAfterCheckedLocalStorage = JSON.parse(
        localStorage.getItem("listCustomerIdsAfterChecked")
      );

      let amountTotalAfterChecked = [];

      listCustomerIdsAfterCheckedLocalStorage.forEach((customerId) => {
        const customerData = EachAmount.filter(
          (item) => item.customer_id == customerId
        );

        if (!amountTotalAfterChecked.includes(customerData)) {
          amountTotalAfterChecked.push(customerData);
        }
      });

      amountTotalAfterChecked = amountTotalAfterChecked.flat();

      const totalAmountAfterReload = amountTotalAfterChecked.reduce(
        (sum, item) => sum + item.total,
        0
      );

      spanTotalAmountPerCheckboxChecked.textContent =
        totalAmountAfterReload.toFixed(2);
    }
  });
});

resetAmountValues();

CreateOrder.addEventListener("click", (e) => {
  e.preventDefault();
  let customerSelectedValue = [];
  let listCustomerChecked = [];
  spanCustomerDefaultData.forEach((span) => {
    customerSelectedValue.push(span.getAttribute("data-customer-id"));
  });
  document
    .querySelectorAll(".confirmation-customer-checkbox")
    .forEach((checkbox) => {
      if (checkbox.checked && !checkbox.disabled) {
        listCustomerChecked.push(checkbox.getAttribute("data-customer-id"));
      }
    });
  console.log(document.querySelectorAll(".confirmation-customer-checkbox"));
  if (customerDefault == null || customerDefault.textContent == "") {
    toastr.error("Veuillez selectionner un client.");
  } else {
    // show loader
    $(".loadings").show("fade");
    $(".spinner-wrappers").show();
    $(".spinner-wrappers").css("position", "fixed");

    $.ajax({
      type: "POST",
      dataType: "json",
      url: `/home/pnr/${pnrIdNew}/get-order/`,
      data: {
        csrfmiddlewaretoken: csrftoken,
        pnrId: pnrIdNew,
        refCde: RfeCde.value,
        customerIdsChecked: JSON.stringify(listCustomerChecked),
        customerId: JSON.stringify(customerSelectedValue),
      },
      success: (response) => {
        console.log(response);
        // hide loader
        $(".spinner-wrappers").hide();
        $(".spinner-wrappers").css("position", "relative");
        if (response.pnr_status == "Non émis") {
          toastr.warning("Commande impossible avec pnr non émis");
        }
        location.reload();

        resetAmountTotalValue();

        toastr.info("Commande créée avec succès");
      },
      error: (response) => {
        console.log(response);
      },
    });
  }
});
//=====================  END OF CREATING ORDER PROCESSING ========================>

// ===> Don't allow user to create an order if the customer field is not filled
$(document).ready(function () {
  removeModalOrderConfirmAttribute();
  $("#create-command").click(function () {
    if (customerDefault == null || customerDefault.textContent == "") {
      $("#createOrderForCustomer").hide();
      $("#create-command").removeAttr("data-target");
      toastr.error("Veuillez selectionner un client.");
    } else if (
      (count__ticketCheckBoxPassenger > 0 && totalAmount == 0) ||
      (count__otherFeeCheckBox > 0 && totalAmount == 0) ||
      (count__feeCheckBox > 0 && totalAmount == 0)
    ) {
      toastr.info(
        "Veuillez devez sélectionner un nouveau client pour les nouveaux billets."
      );
      setTimeout(() => {
        removeModalOrderConfirmAttribute();
        $("#modal-confirm-cmd").modal("hide");
      }, 0);
    } else {
      setTimeout(() => {
        setModalOrderConfirmAttribute();
        $("#modal-confirm-cmd").modal("show");
      }, 0);
    }
  });
  function removeModalOrderConfirmAttribute() {
    $("#create-command").removeAttr("data-target");
    $("#create-command").removeAttr("data-toggle");
  }
  function setModalOrderConfirmAttribute() {
    $("#create-command").attr("data-target", "#modal-confirm-cmd");
    $("#create-command").attr("data-toggle", "modal");
  }
});

function parseDateTimeToFrenchType(datetime) {
  let dateToday = new Date(datetime);
  let dateOptions = { month: "long", day: "numeric", year: "numeric" };
  let hours =
    dateToday.getHours() < 10 ? `0${dateToday.getHours()}` : dateToday.getHours();
  let minutes =
    dateToday.getMinutes() < 10
      ? `0${dateToday.getMinutes()}`
      : dateToday.getMinutes();
  let seconds = 
    dateToday.getSeconds() < 10
      ? `0${dateToday.getSeconds()}`
      : dateToday.getSeconds();
  let dateHoursForToday = `${dateToday.toLocaleString(
    "fr-FR",
    dateOptions
  )}, à ${hours}:${minutes}:${seconds}`;
  return dateHoursForToday;
}

$("#fee-amount-request").attr("disabled", "true");
$("#feeRequestAlert").attr("style", "display: none !important")
reduceFeeRequest.addEventListener("click", (e) => {
  fee_id = $("#fee-id-request").val();
  fee_amount = $("#fee-amount-request").val();
  fee_origin_amount = $("#fee-origin-cost").val();
  choice_type = $("input[name=fee-decrease-application]:checked").val();
  motif = $("#feeReduceMotif").val();
  user_id = $('#user_id').val();
  // $("#modal-dmdfrs").modal("hide");
  $(".loadings").show("fade");
  $(".spinner-wrappers").show();
  $(".spinner-wrappers").css("position", "fixed");

  $.ajax({
    type: "POST",
    dataType: "json",
    url: `/home/reduce-fee-request`,
    data: {
      csrfmiddlewaretoken: csrftoken,
      pnrId: pnrIdNew,
      userId:user_id,
      feeId: fee_id,
      feeAmount: fee_amount,
      feeOriginAmount: fee_origin_amount,
      choiceType: choice_type,
      motif: motif,
    },
    success: (response) => {
      console.log(response);

      if (response.status == 1) {
        // toastr.info(response.message);
        $("#feeRequestAlert").attr("style", "display: flex !important; gap: 1rem;")
        $("#feeRequestAlert").removeClass("alert-info")
        $("#feeRequestAlert").addClass("alert-success")
        $("#feeRequestAlert").html(`
          <i class="fa fa-check" style="font-size: 2rem !important"></i>
          <span>${response.message}</span>
        `)

        // hide loader
        $(".spinner-wrappers").hide();
        $(".spinner-wrappers").css("position", "relative");
        // setInterval(() => {
          window.location.reload();
        // }, 1000)
      } else if (response.status == 3) {
        // toastr.info(response.message);
        submitFeeRequest.setAttribute("disabled", true)
        const datetimeFeeReduceRequest = parseDateTimeToFrenchType(response.date_creation)
        $("#feeRequestAlert").attr("style", "display: flex !important; gap: 1rem;")
        $("#feeRequestAlert").removeClass("alert-success")
        $("#feeRequestAlert").addClass("alert-info")
        $("#feeRequestAlert").html(`
          <i class="fa fa-exclamation-triangle" style="font-size: 2.5rem !important"></i>
          <div class="d-flex" style="flex-direction: column">
            <span class="text-center">Une demande de diminution est déja en cours. Veuillez attendre la validation s'il vous plaît...</span>
            <span style="width: 100%; height: 1px; background: white; margin: 6px 0 6px 0;"></span>
            <span>
              <strong class="text-white">
                Montant demandée: ${response.fee_origin} 
                <i class="fa-solid fa-euro-sign"></i>
                <i class="fa-solid fa-arrow-right"></i>
              </strong>
              
              <strong class="text-warning"> ${response.fee_amount}
                <i class="fa-solid fa-euro-sign"></i>
              </strong>
            </span>
            <span><strong class="text-white">Date du demande: </strong>${datetimeFeeReduceRequest}</span>
            <span><strong class="text-white">Demandé(e) par: </strong>${response.user}</span>
          </div>
        `)

        // hide loader
        $(".spinner-wrappers").hide();
        $(".spinner-wrappers").css("position", "relative");
      } else {
        toastr.error(response.message);
        $("#modal-dmdfrs").modal("hide");

        // hide loader
        $(".spinner-wrappers").hide();
        $(".spinner-wrappers").css("position", "relative");
        window.location.reload();
      }
      // window.location.reload();
      // toastr.info('');
    },
    error: (response) => {
      console.log(response.message);
      toastr.error(response.message);
      // hide loader
      $(".spinner-wrappers").hide();
      $(".spinner-wrappers").css("position", "relative");
    },
  });
});

document.getElementById("create-devis").addEventListener("click", (e) => {
  if (customerDefault == null || customerDefault.textContent == "") {
    toastr.error("Veuillez selectionner un client.");
  } else {
    // show loader
    $(".loadings").show("fade");
    $(".spinner-wrappers").show();
    $(".spinner-wrappers").css("position", "fixed");
    let customerSelectedValue = [];
    spanCustomerDefaultData.forEach((span) => {
      customerSelectedValue.push(span.getAttribute("data-customer-id"));
    });

    $.ajax({
      type: "POST",
      dataType: "json",
      url: `/home/pnr/${pnrIdNew}/get-quotation/`,
      data: {
        csrfmiddlewaretoken: csrftoken,
        pnrId: pnrIdNew,
        refCde: RfeCde.value,
        passengerIds: JSON.stringify(passenger),
        customerId: customerSelectedValue[0],
      },
      success: (response) => {
        // hide loader
        $(".spinner-wrappers").hide();
        $(".spinner-wrappers").css("position", "relative");

        // console.log(response);
        location.reload();
        toastr.info("Devis créée avec succès");
      },
      error: (response) => {
        console.log(response);
      },
    });
  }
});

//==> Handling Passengers CheckBox
const button__createCustomer = document.getElementById("buttonAddCustomer");
const pnrDetailSave = document.querySelector('#save[name="save-pnr-detail"]');
const allCheckBox = document.querySelectorAll(
  "#passagers-check.passengers-align-checkboxes"
);
let allCheckBoxLength = document.querySelectorAll(
  "#passagers-check.passengers-align-checkboxes"
).length;
let checkBoxChecked = allCheckBoxLength || 0;
let CheckboxHiddenCount = allCheckBoxLength;
allCheckBox.forEach((checkBox) => {
  checkBox.hidden ? checkBoxChecked-- : checkBoxChecked + 0;
  checkBox.hidden ? CheckboxHiddenCount-- : checkBoxChecked;
});

// console.log(CheckboxHiddenCount);

//count the checkbox of ticket that aren't checked yet
let count = 0;
document.querySelectorAll(".ticket-checkbox-passenger").forEach((input) => {
  if (!input.hidden) {
    count++;
  }
});

let ticketCheckBoxPassenger = document.querySelectorAll(
  ".ticket-checkbox-passenger"
);
let otherFeeCheckBox = document.querySelectorAll(".other-fees-check");
let feeCheckBox = document.querySelectorAll(".ticket-fee-checkbox");
let count__ticketCheckBoxPassenger = ticketCheckBoxPassenger.length;
let count__otherFeeCheckBox = otherFeeCheckBox.length;
let count__feeCheckBox = feeCheckBox.length;

ticketCheckBoxPassenger.forEach((checkBox) => {
  checkBox.hidden
    ? count__ticketCheckBoxPassenger--
    : count__ticketCheckBoxPassenger + 0;
});

feeCheckBox.forEach((checkBox) => {
  checkBox.hidden ? count__feeCheckBox-- : count__feeCheckBox + 0;
});

otherFeeCheckBox.forEach((checkBox) => {
  checkBox.hidden ? count__otherFeeCheckBox-- : count__otherFeeCheckBox + 0;
});

document.querySelectorAll(".other-fees-check").forEach((input) => {
  if (!input.hidden) {
    count++;
  }
});


const TableTicketFeesBody = document.getElementById("table-ticket-fees-body");
const ProductDropdown = document.querySelector(
  '[name="service-type-dropdown"]'
);
const ProductDesignaInput = document.querySelector(
  '[name="design-input-line"]'
);
const ProductTranspInput = document.querySelector(
  '[name="transport-input-line"]'
);
const ProductTaxInput = document.querySelector('[name="taxe-input-line"]');
const ProductpassInput = document.querySelector(
  '[name="passenger-input-line"]'
);
const ProductRefInput = document.querySelector('[name="reference-input-line"]');
const ProductTotalInput = document.querySelector('[name="total-input-line"]');
const NewLine = document.querySelector(".new-line");
const tableTicketFee = document.getElementById("table-ticket-fees");
const ProductTypeInitiale = document.getElementById("product-type-initial");

ProductDropdown.addEventListener("change", (e) => {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: `/home/pnr/${pnrIdNew}/get-product/`,
    data: {
      csrfmiddlewaretoken: csrftoken,
      productId: e.target.value,
    },
    success: (response) => {
      const product = response.products;
      ProductTranspInput.value = parseFloat(product[0].cost).toFixed(2);
      ProductTaxInput.value = parseFloat(product[0].tax).toFixed(2);
      ProductTotalInput.textContent = parseFloat(product[0].total).toFixed(2);
      ProductTypeInitiale.textContent = product[0].type;
    },
    error: (response) => {
      console.log(response);
    },
  });
});

/*
 * =======================  SET A COUNT IF SAVE ON ADD LINE IS CLICKED ===========================*
 *  SaveProductCounting: Compter les enregistrements de nouveaux produits                           *
 *  save-product-select: Les inputs de frais de service.                                         *
 *                                                                                             *
 *  S'il y a un enregistrement de nouvelle ligne (onclick event)                              *
 *=============================================================================================*
 */

let SaveProductCounting = 0;

document
  .getElementById("save-product-select")
  .addEventListener("click", (e) => {
    ticket = document.getElementById('ticket-avoir').value;
    console.log('------TICKET ----------------');
    console.log(ticket);
    
      SaveProductCounting++;
      let listNewProduct = [];
      const designation =
        ProductDropdown.children[ProductDropdown.selectedIndex].getAttribute(
          "data-designation"
        );
      document.querySelector(".tr-add-line").hidden = false;
      document.getElementById("add-product-service-line").hidden = false;

      passenger = (document.getElementById('select_Passenger')).value;
      console.log(ProductDropdown.value);

      if (ProductDropdown.value == 19) {
        if (ticket.trim() !== "") {
          selectedSegment = document.querySelector('#multipleSelect').getSelectedOptions();
          company_id = (document.getElementById('avoir-company-id')).value;
          console.log(selectedSegment);
          listNewProduct.push(
            ProductDropdown.value,
            ProductTypeInitiale.textContent,
            designation,
            parseFloat(ProductTranspInput.value).toFixed(2),
            (
              parseFloat(ProductTranspInput.value) + parseFloat(ProductTaxInput.value)
            ).toFixed(2),
            ProductpassInput.value,
            "",
            ticket,
            passenger,
            selectedSegment,
            company_id
          );
        }
        else {
          toastr.error('Veuillez entrer un Numéro de billet')
          document.getElementById('ticket-avoir').style.borderColor = 'red';
        }
      }
      else {
        listNewProduct.push(
          ProductDropdown.value,
          ProductTypeInitiale.textContent,
          designation,
          parseFloat(ProductTranspInput.value).toFixed(2),
          parseFloat(ProductTaxInput.value).toFixed(2),
          (
            parseFloat(ProductTranspInput.value) + parseFloat(ProductTaxInput.value)
          ).toFixed(2),
          ProductpassInput.value,
          ""
        );
      }

      $.ajax({
        type: "POST",
        dataType: "json",
        url: `/home/pnr/${pnrIdNew}/import_product/`,
        data: {
          csrfmiddlewaretoken: csrftoken,
          pnrId: pnrIdNew,
          listNewProduct: JSON.stringify(listNewProduct),
        },
        success: (response) => {
          console.log(response);
          location.reload();
        },
        error: (response) => {
          console.log(response);
        },
      });
    
      });

/*
 * =======================  SET A COUNT IF INPUT OF FEES IS CHANGED ===========================*
 *  feeCountChecking: Compter les frais de service séléctionnées                           *
 *  inputFeesCost: Les inputs de frais de service.                                         *
 *                                                                                             *
 *  S'il y a un changement de frais de service (onchange event)                            *
 *      1. Vérifier si le montant est le même, ne fait rien                                *
 *      2. Vérifier si le montant est différent, alors on incremente le feeCountChecking   *
 *=============================================================================================*
 */

let feeCountChecking = 0;
let inputFeesCost = document.querySelectorAll(".fee-cost");
if (inputFeesCost != null) {
  inputFeesCost.forEach((input) => {
    input.addEventListener("input", (e) => {
      let inputFeeCost = e.target.value;
      let currentFeeCost = e.target.getAttribute("data-cost");

      if (inputFeeCost != currentFeeCost) {
        feeCountChecking++;
      } else {
        feeCountChecking--;
      }
    });
  });
}

pnrDetailSave.removeAttribute("data-target");

allCheckBox.forEach((checkBox) => {
  checkBox.addEventListener("change", () => {
    if (checkBox.checked && !checkBox.hidden) {
      checkBoxChecked++;
    } else {
      checkBoxChecked--;
    }
    // checkBox.checked && !checkBox.hidden ? checkBoxChecked++ : checkBoxChecked--

    pnrDetailSave.addEventListener("click", (e) => {
      if (
        customerListSelection.value == null ||
        (customerListSelection.value == "" && feeCountChecking < 1)
      ) {
        e.preventDefault();
        pnrDetailSave.setAttribute("data-target", "#alertModalEmptyCustomer");
      } else if (checkBoxChecked == 0 && feeCountChecking < 1) {
        e.preventDefault();
        pnrDetailSave.setAttribute(
          "data-target",
          "#alertModalNoPassengerSelected"
        );
      } else {
        pnrDetailSave.removeAttribute("data-target");
      }
    });
  });
});

/*
 * ====== CLICK ON SAVE BUTTON AND HANDLE PAGE'S RELOADING ============*
 *  1. feeCountChecking: Compter les frais de service séléctionnées    *
 *  Si feeCountChecking > 0,                                           *
 *      c-à-d qu'il y a un changement au niveau des frais de services  *
 *      Alors, on recharge la page                                     *
 *  2. CheckboxHiddenCount == checkBoxChecked || checkBoxChecked > 0,  *
 *      Alors on recharge la page                                      *
 *=====================================================================*
 */

document.getElementById("save").addEventListener("click", (e) => {
  e.preventDefault();
  console.log("clicked");
  let listpassengersChecked = [];
  let listpassengersUnchecked = [];
  let listFeeCost = [];
  let listotherFeesChecked = [];
  let listTicketCheckboxesAddAfterOrderAlreadyCreated = [];

  document.querySelectorAll(".ticket-checkbox-passenger").forEach((input) => {
    if (
      input.getAttribute("data-ticket-status") == 0 &&
      input.checked &&
      !input.disabled &&
      !input.hidden
    ) {
      listTicketCheckboxesAddAfterOrderAlreadyCreated.push(
        input.getAttribute("data-ticket-id")
      );
    }
  });

  const InputFeeCost = document.querySelectorAll(".fee-cost");
  InputFeeCost.forEach((input) => {
    const Id = input.getAttribute("data-fee-id");
    const Value = input.value;
    listFeeCost.push([Id, Value]);
  });

  const listPassengersCheckboxes = document.querySelectorAll(
    ".passengers-align-checkboxes-first"
  );
  listPassengersCheckboxes.forEach((passengersCheckbox) => {
    if (
      passengersCheckbox.checked &&
      !passengersCheckbox.disabled &&
      !passengersCheckbox.hidden
    ) {
      listpassengersChecked.push(passengersCheckbox.getAttribute("data-id"));
    } else {
      listpassengersUnchecked.push(passengersCheckbox.getAttribute("data-id"));
    }
  });

  const listOtherFeesCheckboxes = document.querySelectorAll(
    ".other-fees-checkboxes"
  );
  listOtherFeesCheckboxes.forEach((otherFeesChecked) => {
    if (
      otherFeesChecked.checked &&
      !otherFeesChecked.disabled &&
      !otherFeesChecked.hidden
    ) {
      listotherFeesChecked.push(
        otherFeesChecked.getAttribute("data-other-fees-id")
      );
    }
  });

  if (
    checkBoxChecked < 1 &&
    CheckboxHiddenCount == checkBoxChecked &&
    feeCountChecking < 1
  ) {
    if (customerListSelection.value.trim().length == 0) {
      window.location.reload();
    }
  }
  if (
    checkBoxChecked > 0 ||
    feeCountChecking > 0 ||
    count > 0 ||
    customerListSelection.value.trim().length > 0
  ) {
    console.log("AJAX Launched");
    console.log(customerListSelection.value);
    $.ajax({
      type: "POST",
      dataType: "json",
      url: `/home/pnr/${pnrIdNew}/save_pnr_detail_modification/`,
      data: {
        csrfmiddlewaretoken: csrftoken,
        pnrId: pnrIdNew,
        refCde: RfeCde.value,
        ticketIdsChecked: JSON.stringify(
          listTicketCheckboxesAddAfterOrderAlreadyCreated
        ),
        customerId: customerListSelection.value,
        feeCost: JSON.stringify(listFeeCost),
        otherfeesIdsChecked: JSON.stringify(listotherFeesChecked),
      },
      success: (response) => {
        console.log("Status   : " , response);
        if (((response.ticket_status == 'success') && (response.other_fee_status == '')) || ((response.ticket_status == '') && (response.other_fee_status == '')) || ((response.ticket_status == '') && (response.other_fee_status == 'success')) || ((response.ticket_status == 'success') && (response.other_fee_status == 'success'))) {
          window.location.reload();
        }
        else if ((response.ticket_status == 'failed') || (response.other_fee_status == 'failed')) {
          $("#ErrorSavingModal").modal('show');
        }
      },
      error: (response) => {
        console.log(response);
      },
    });
  }
});

document.getElementById('RefreshErrorSaving').addEventListener('click', ()=> {
  $("#ErrorSavingModal").hide();
  window.location.reload();
})

document.querySelectorAll(".delete-other-fee-row").forEach((button) => {
  button.addEventListener("click", (e) => {
    $("#confirmDeleteOtherFee").modal('show');
    console.log(
      button.parentElement.parentElement.getAttribute("data-other-fee-id")
    );
  });
});

/*
 * ====== CLICK ON CONFIRMATION BUTTON AND DELETE THE CUSTOMER'S ORDER ======*
 *  1. Supprimer les commandes de ce PNR sur dans passengerInvoice           *
 *      Remettre les ticket et frais de service de ce client cochâble        *
 *===========================================================================*
 */

const ConfirmRemoveCustomer = document.getElementById("exitRemoveCustomer");
const removeCustomerButton = document.querySelectorAll(
  ".remove-customer-button"
);
const ModalRemoveCustomer = document.getElementById("ModalRemoveCustomer");
const ModalRemoveCustomerBody = document.getElementById(
  "ModalRemoveCustomerBody"
);

removeCustomerButton.forEach((button) => {
  button.addEventListener("click", () => {
    const customerIdOnRemoveModal =
      ModalRemoveCustomer.getAttribute("data-customer-id");
    if (customerIdOnRemoveModal == null || customerIdOnRemoveModal == "") {
      ModalRemoveCustomerBody.setAttribute(
        "data-customer-id",
        button.getAttribute("data-customer-id")
      );
    }
    ModalRemoveCustomerBody.textContent = `Les commandes pour le client "${button.getAttribute(
      "data-customer-intitule"
    )}" seront  supprimées.`;
  });
});

ConfirmRemoveCustomer.addEventListener("click", (e) => {
  e.preventDefault();
  const customerId = ModalRemoveCustomerBody.getAttribute("data-customer-id");
  console.log("AJAX Launched");
  $.ajax({
    type: "POST",
    dataType: "json",
    url: `/home/pnr/${pnrIdNew}/delete-customer/`,
    data: {
      csrfmiddlewaretoken: csrftoken,
      pnrId: pnrIdNew,
      customerId: customerId,
    },
    success: (response) => {
      console.log(response);
      window.location.reload();
    },
    error: (response) => {
      console.log(response);
    },
  });
});

/***
 * Recalculer le montant total et le montal total des frais de services selon les lignes cochées
 *
 */

const CheckboxForTotalRecalculation = document.querySelectorAll(
  ".checkbox-line-below"
);
const CheckboxOfPassenger = document.querySelectorAll(
  ".passengers-align-checkboxes"
);
const SpanAmoutTotal = document.getElementById("pnr-amount-total");
const SpanFeesTotal = document.getElementById("total-services-fees");
let amountFeeLineSelected = 0;
let AmountTotal = parseFloat(SpanAmoutTotal.getAttribute("data-amount-total"));
let FeeAmountTotal = parseFloat(SpanFeesTotal.getAttribute("data-amount-fees"));
CheckboxForTotalRecalculation.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const communeId = checkbox.getAttribute("data-commune-id");
    if (!checkbox.hidden && checkbox.checked) {
      const otherCheckbox = document.querySelectorAll(
        `input[data-commune-id="${communeId}"]`
      );
      otherCheckbox.forEach((item) => {
        AmountTotal += parseFloat(item.getAttribute("data-amount-total"));
        if (item.getAttribute("data-type") == "fee") {
          FeeAmountTotal += parseFloat(item.getAttribute("data-amount-total"));
        }
      });
      SpanAmoutTotal.textContent = AmountTotal.toFixed(2);
      SpanFeesTotal.textContent = FeeAmountTotal.toFixed(2);
    } else if (!checkbox.hidden && !checkbox.checked) {
      const otherCheckbox = document.querySelectorAll(
        `input[data-commune-id="${communeId}"]`
      );
      otherCheckbox.forEach((item) => {
        AmountTotal -= parseFloat(item.getAttribute("data-amount-total"));
        if (item.getAttribute("data-type") == "fee") {
          FeeAmountTotal -= parseFloat(item.getAttribute("data-amount-total"));
        }
      });
      SpanAmoutTotal.textContent = AmountTotal.toFixed(2);
      SpanFeesTotal.textContent = FeeAmountTotal.toFixed(2);
    }
  });
});

CheckboxOfPassenger.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const passengerId = checkbox.getAttribute("data-id");
    if (!checkbox.hidden && checkbox.checked) {
      const otherCheckbox = document.querySelectorAll(`.checkto${passengerId}`);
      otherCheckbox.forEach((item) => {
        AmountTotal += parseFloat(item.getAttribute("data-amount-total"));
        if (item.getAttribute("data-type") == "fee") {
          FeeAmountTotal += parseFloat(item.getAttribute("data-amount-total"));
        }
      });
      SpanAmoutTotal.textContent = AmountTotal.toFixed(2);
      SpanFeesTotal.textContent = FeeAmountTotal.toFixed(2);
    } else if (!checkbox.hidden && !checkbox.checked) {
      const otherCheckbox = document.querySelectorAll(`.checkto${passengerId}`);
      otherCheckbox.forEach((item) => {
        AmountTotal -= parseFloat(item.getAttribute("data-amount-total"));
        if (item.getAttribute("data-type") == "fee") {
          FeeAmountTotal -= parseFloat(item.getAttribute("data-amount-total"));
        }
      });
      SpanAmoutTotal.textContent = AmountTotal.toFixed(2);
      SpanFeesTotal.textContent = FeeAmountTotal.toFixed(2);
    }
  });
});

/***
 * Fin du code pour recalculer le montant total et le montal total des frais de services selon les lignes cochées
 *
 */

/**
 * Quand on clique sur créér un client, on affiche un pop up si le client est déja présent dans la table t_client,
 * Si non, on affiche le modal de création de client
 */
const modal__addNewClientForOtherPassenger = document.getElementById(
  "addNewClientForOtherPassenger"
);
const button__createNewClientForOtherPassenger = document.getElementById(
  "createNewClientForOtherPassenger"
);
const button__confirmSelectionCustomer = document.getElementById(
  "confirmSelectionCustomer"
);
let select__customersList = document.getElementById("customer-list");
if (button__createCustomer != null) {
  if (
    button__createCustomer.getAttribute("data-passenger-informations") != "None"
  ) {
    removeModalAttribute();
    let firstPassengerInformations = JSON.parse(
      button__createCustomer.getAttribute("data-passenger-informations")
    );
    let name = firstPassengerInformations.name;
    let surName = firstPassengerInformations.surname;
    let valueToFind = "";
    if (name != null) {
      valueToFind = [firstPassengerInformations.name.trim()];
    }
    if (surName != null) {
      valueToFind = [firstPassengerInformations.surname.trim()];
    }
    if (name != null && surName != null) {
      valueToFind = [
        firstPassengerInformations.name.trim(),
        firstPassengerInformations.surname.trim(),
      ];
    }
    button__createCustomer.addEventListener("click", async () => {
      try {
        const response = await $.ajax({
          type: "POST",
          dataType: "json",
          url: `/home/pnr/${pnrIdNew}/find-customer/`,
          data: {
            csrfmiddlewaretoken: csrftoken,
            value: JSON.stringify(valueToFind),
          },
        });
        
        console.log('====================================');
        console.log("CLIENT FOUND")
        console.log(response);
        console.log('====================================');

        if (response.isCustomerFind) {
          setTimeout(() => {
            removeModalAttribute();
            $("#add-customer").modal("hide");
          }, 0);
          toastr.success(`Le client ${valueToFind} a été déja créé`);

          $("#createNewClientForOtherPassenger").modal("show");
          $("#clientIntituteInformation").text(response.clientIntitule);
          $("#clientEmailInformation").text(response.clientEmail);
          $("#clientPhoneInformation").text(response.clientPhone);
          $("#clientAddressInformation").text(response.clientAddress);
          $("#clientPostalCodeInformation").text(response.clientPostalCode);
          $("#clientCityInformation").text(response.clientCity);
          $("#clientDepartementInformation").text(response.clientDepartment);
          $("#clientCountryInformation").text(response.clientCountry);

          const findCreatorInformation = document.querySelector("#findCreatorInformation")
          try {
            findCreatorInformation.setAttribute("data-client", JSON.stringify(response))
          } catch (exception) {
            console.log('====================================');
            console.log(exception);
            console.log('====================================');
          }

        } else {
          setTimeout(() => {
            setModalAttribute();
            $("#add-customer").modal("show");
          }, 0);

          toastr.info(`Le client ${valueToFind} n'est pas encore créé`);
        }
      } catch (error) {
        console.log(error);
      }
      removeModalAttribute();
    });

    if (button__confirmSelectionCustomer) {
      const findCreatorInformation = document.querySelector("#findCreatorInformation")
      button__confirmSelectionCustomer.addEventListener("click", () => {
        const getClientData = findCreatorInformation.getAttribute("data-client") 
        const response = JSON.parse(getClientData)

        try {
          if (response) {
            select__customersList.insertAdjacentHTML('afterbegin', `
              <option value=${response.clientId} selected="true"> ${response.clientIntitule} </option>
            `);
          } 
        } catch (error) {
          console.log('====================================');
          console.log("CLIENT NOT FOUND")
          console.log(error);
          console.log('====================================');
        }
      });
    }    

    button__createNewClientForOtherPassenger.addEventListener("click", () => {
      $("#createNewClientForOtherPassenger").modal("hide");
    });

    function removeModalAttribute() {
      button__createCustomer.removeAttribute("data-target");
      button__createCustomer.removeAttribute("data-toggle");
    }

    function setModalAttribute() {
      button__createCustomer.setAttribute("data-target", "#add-customer");
      button__createCustomer.setAttribute("data-toggle", "modal");
    }
  }
}

const input__confirmationCustomerOrderCheckbox = document.querySelectorAll(
  "#ConfirmationCustomerOrderCheckbox"
);
const jsonParseTotalAmount = JSON.parse(
  totalAmountPerCheckboxChecked.getAttribute("data-each-amount-order")
);
// if (input__confirmationCustomerOrderCheckbox.length > 0) {
//     input__confirmationCustomerOrderCheckbox.forEach((input) => {
//         let customerId = input.getAttribute("data-customer-id").trim()
//         const totalAmount = jsonParseTotalAmount.filter((data) => data.customer_id == customerId)
//         let eachAmountPerPassenger = totalAmount[0].total
//         if (eachAmountPerPassenger == 0) {
//             input.setAttribute("disabled", true)
//         } else {
//             input.removeAttribute("disabled")
//         }
//     })
// }
// if (ConfirmationCustomerDefault.length > 0) {
//     ConfirmationCustomerDefault.forEach((customer) => {
//         let customerId = customer.getAttribute("data-customer-id").trim()
//         const totalAmount = jsonParseTotalAmount.filter((data) => data.customer_id == customerId)
//         let eachAmountPerPassenger = totalAmount[0].total
//         if (eachAmountPerPassenger == 0) {
//             customer.classList.add("text-success")
//         } else {
//             customer.classList.remove("text-success")
//         }
//     })
// }
const span__confirmationCustomerDefault = document.querySelectorAll(
  ".confirmation-customer-default"
);
// if (span__confirmationCustomerDefault.length > 0) {
//     span__confirmationCustomerDefault.forEach((span) => {
//         let customerId = span.getAttribute("data-customer-id").trim()
//         const totalAmount = jsonParseTotalAmount.filter((data) => data.customer_id == customerId)
//         let eachAmountPerPassenger = totalAmount[0].total
//         if (eachAmountPerPassenger == 0) {
//             span.classList.add("text-success")
//         } else {
//             span.classList.remove("text-success")
//         }
//     })
// }

let count__ticketHaveNoPassenger = document.querySelectorAll(".tooltips.empty-passenger");
let error__noPassengerForTicket = document.getElementById("error__noPassengerForTicket");

$("#error__noPassengerForTicket").hide();

error__noPassengerForTicket.innerHTML = `Mail PNR manquant pour le(s) billet(s) : `;
if (count__ticketHaveNoPassenger.length > 0) {
  $("#error__noPassengerForTicket").show();
  count__ticketHaveNoPassenger.forEach((ticket) => {
    error__noPassengerForTicket.innerHTML += `
      <span class="text-sm"> ${ticket.getAttribute("data-ticket-number")} </span>
    `;
  });

  // Bloquer la création de la commande quand il manque le mail du PNR pour le billet
} else {
  $("#error__noPassengerForTicket").hide();
}

// ----------- AVOIR COMPAGNIE -----------------------------
$('#ticket-avoir').hide();
$('#select_Passenger').hide();
$('#multipleSelect').hide();
$('#avoir-company-id').hide();

$('#SelectProduct').on('change', function(){
  select_product = $('#SelectProduct').val();

  if(select_product == 19){
    $('#SelectProduct').hide();
    $('#taxe-input-line').hide();
    $('#ticket-avoir').show();
    $('#passenger_segment').hide();
    document.getElementById('div-company').hidden = false;


    const parent = document.getElementById("select_Passenger");
    const child = document.getElementById("child_passenger");

    const parent_passenger_segment = document.getElementById("multipleSelect");
    const child_passenger_segment = document.getElementById("child_passenger_segment");


    if (child) {
      parent.removeChild(child);
    }
    if (child_passenger_segment) {
      parent_passenger_segment.removeChild(child_passenger_segment);
    }

    var pnr_id = $('#pnr_id').data('id');
    console.log(pnr_id);
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
          $('#select_Passenger').show();
          parent.innerHTML = ''

          passengers.map((passenger) => {
            const newOption = document.createElement("option");
            newOption.id = "child_passenger";
            newOption.value = passenger['passenger_id'];
            if (passenger['passenger_name'] !== null && passenger['passenger_surname'] != null) {
              newOption.textContent = passenger['passenger_surname'] + ' ' + passenger['passenger_name'];
            }
            if (passenger['passenger_name'] !== null && passenger['passenger_surname'] == null) {
              newOption.textContent = passenger['passenger_name'];
            }
            if (passenger['passenger_name'] == null && passenger['passenger_surname'] !== null) {
              newOption.textContent = passenger['passenger_surname'];
            }
            parent.append(newOption);
          });
        } 
        let segments = data.context.segments;
        parent_passenger_segment.innerHTML = '';

        if (segments.length > 0) {
          
          const myOptions = segments.map((segment) => {
            return {
              label: segment['segment'],
              value: segment['segment_id'],
            };
          });

          VirtualSelect.init({
            ele: '#multipleSelect',
            multiple: true,
          })

          document.querySelector('#multipleSelect').setOptions(myOptions);

          const validatePassengerSegment = (isValid) => {
            if (isValid) {
              $("#multipleSelect").attr("style", "border: 1px solid green")
              $("#multipleSelect").removeClass("border border-danger")
            } else {
              $("#multipleSelect").removeAttr("style", "border: 1px solid green")
              $("#multipleSelect").addClass("border border-danger")
            }
          } 
          
          const multipleSelection = document.querySelector('#multipleSelect')
          $("#multipleSelect").on("change", () => {
            if (multipleSelection.value.length > 0) {
              console.log(true);
              validatePassengerSegment(true)
            } else {
              console.log(false);
              validatePassengerSegment(false)
            }
          })
          

        }

        
      }
    });

  }
});

const validateInputTickerAvoir = (isValid) => {
  if (isValid) {
    $('#ticket-avoir').removeClass("form is-invalid")
    $('#ticket-avoir').addClass("form is-valid")
  } else {
    $('#ticket-avoir').addClass("form is-invalid")
    $('#ticket-avoir').removeClass("form is-valid")
  }
}

$(document).ready(function () {
  $('#ticket-avoir').on('input', function () {
    // document.getElementById('ticket-avoir').style.borderColor = 'black';
    var inputValue = $(this).val();
    var sanitizedValue = inputValue.replace(/[^0-9-]/g, '');
    $(this).val(sanitizedValue);
    
    $("#save-product-select").prop('disabled', false);
    
    if (inputValue.length < 13 || inputValue.length > 16) {
      $("#save-product-select").prop('disabled', true);
      validateInputTickerAvoir(false)
    }
    
    
    if (inputValue.length >= 14 && inputValue.length <= 15) {
      $("#save-product-select").prop('disabled', true);
      validateInputTickerAvoir(false)
    }
    
    if (inputValue.length == 14 && inputValue.charAt(13) !== '-') {
      var modifiedValue = inputValue.slice(0, 13) + '-' + inputValue.slice(13);
      $('#ticket-avoir').val(modifiedValue);
    }

    if (inputValue.length == 13 || inputValue.length == 16) {
      validateInputTickerAvoir(true)
    }
  });
});

$(document).ready(function () {
  $('#transport-input-line').on('input', function () {
    if ($('#SelectProduct').val() == 19) {
      var inputValue = $(this).val();
      var numericValue = parseFloat(inputValue);

      if (!isNaN(numericValue)) {
        if (numericValue > 0) {
          var sanitizedValue = '-' + inputValue;
          $(this).val(sanitizedValue);
        }
      }

    }
  });
});

// Afficher le modal de confirmation de suppression de ticket non commandé
$(document).ready(function () {
  $('.deleteticket').click(function () {
    // if the ticket is of type TKT
    $('#ticketNumber').text($(this).data('ticket-number'));
    $('#ticketId').val($(this).data('ticket-id'));
    $('#ticketTable').val($(this).data('ticket-table'));
    // if the ticket is of type EMD
    if ($(this).data('ticket-designation')) {
      $('#ticketNumber').text($(this).data('ticket-designation'));
    }
    
  });
});

//Supprimer le ticket non commandé
$(document).ready(function(){
  $('#deletTicketModalConfirmation').click(function () {
    var ticketId = $('#ticketId').val();
    var ticketTable = $('#ticketTable').val();
    var ticketNumber = $('#ticketNumber').val();

    $.ajax({
      type: "POST",
      url: "/home/ticket-delete",
      dataType: "json",
      data: {
          ticketId: ticketId,
          ticketNumber: ticketNumber,
          ticketTable: ticketTable,
          csrfmiddlewaretoken: csrftoken,
      },
      success: function (data) {
          if (data.status == 'ok') {
              toastr.success('Ticket supprimé');
                  location.reload();
          } 
          if (data.status == 'error') {
              toastr.error(data.error)
          }
      },
    });
  });
});