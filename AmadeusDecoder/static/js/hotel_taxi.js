const hotel_supplier_list = [];
const taxi_supplier_list = [];
const departure_location_list = [];
var pnr_id = document.getElementById('pnr_id').getAttribute('data-id');

$('#SelectProduct').on('change', function(){
  console.log("SELECT PRODUCT CLICKED");
  
  select_product = Number($('#SelectProduct').val());
  console.log(" PRODUCT ",select_product);
  if ([12, 15].includes(select_product)) {
    $('#modalTaxiInfo').modal("hide").modal("show");
    if (select_product == 12){
      $('#modalTaxiTitle').text("Informations Taxi");
      $('#taximanDiv').show();
    }
    if (select_product == 15){
      $('#modalTaxiTitle').text("Informations Transfet");
    }
  }

  if ([9, 8, 14].includes(select_product)) {
    $('#modalBusInfo').modal("show");
    if (select_product == 9){$('#modalBusTitle').text("Informations Bus");}
    if (select_product == 8){$('#modalBusTitle').text("Informations SNCF TGV AIR");}
    if (select_product == 14){$('#modalBusTitle').text("Informations TRAIN : SNCF");}

  }

  if (select_product == 11) {
    $('#modalLocationInfo').modal("show");
  }

});

$('#modalHotelInfo').on('hidden.bs.modal', function () {
  console.log("HOTEL MODAL IS CLOSED");
  $(this).removeAttr('aria-hidden');
  if(!sessionStorage.getItem('hotel_info')){ $('#SelectProduct').val(''); }
  
});

$('#modalTaxiInfo').on('hidden.bs.modal', function () {
  console.log("Modal Taxi fermé");
  if(!sessionStorage.getItem('taxi_details')){ $('#SelectProduct').val(''); }

});


$('#SelectProduct').on('change', function(){
  select_product = $('#SelectProduct').val();

});

function updateSelectHotelOptions() {
    const parent_hotel = document.getElementById("hotel-supplier-list")
    const parent_taxi = document.getElementById("taxi-supplier-list")

    const hotel_child = document.getElementById("hotel-supplier-item")
    const taxi_child = document.getElementById("taxi-supplier-item")

      if (hotel_child) {
        parent_hotel.removeChild(hotel_child);
      }
      if (taxi_child) {
        parent_taxi.removeChild(taxi_child);
      }


      var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            
            if (this.readyState == 4 && this.status == 200) {
                                        
            var response = JSON.parse(this.responseText);
            
            const hotel_suppliers = Array.from(response.hotel_suppliers);
            const taxi_suppliers = Array.from(response.taxi_suppliers);

            parent_hotel.innerHTML = '';
            parent_taxi.innerHTML = '';

            // Ajouter des options au choix de fournisseur d'hôtel
            hotel_suppliers.map((supplier) =>{
              hotel_supplier_list.push(supplier);
              var newli = document.createElement("li");
              newli.className="hotel-supplier-item";
              newli.setAttribute("data-id", supplier.id);
              newli.textContent = supplier.name;
              newli.setAttribute('role', 'option') ;
              newli.setAttribute('tabindex', "-1") ;
              parent_hotel.append(newli);

            });

            // Ajouter des options au choix de fournisseur de taxi

            taxi_suppliers.map((supplier) =>{
              taxi_supplier_list.push(supplier);
              var li = document.createElement("li");
              li.className="taxi-supplier-item";
              li.setAttribute("data-id", supplier.id);
              li.textContent = supplier.name;
              li.setAttribute('role', 'option') ;
              li.setAttribute('tabindex', "-1") ;
              parent_taxi.append(li);

            });


        }
    };
    xmlhttp.open("GET", '/home/get-service-supplier-list', true);
    xmlhttp.send();
}

function updatePassengerList(){
  
  $.ajax({
    type: "POST",
    url:"/home/get-passengers-and-segments",
    dataType: "json",
    data:{
      pnr_id: pnr_id,
      csrfmiddlewaretoken: csrftoken,
    },
    success: function(data){
      let passengers = data.context.passengers;

      if (passengers.length ==0){
          $('#taxi_passenger').hide();
      }
      if (passengers.length > 0) {
        const passenger_options = passengers.map((passenger) => {
          let textContent = null
          if (passenger['passenger_name'] !== null && passenger['passenger_surname'] != null ) {
            textContent = passenger['passenger_name'] + ' ' + passenger['passenger_surname'];
          }
          
          if (passenger['passenger_name'] !== null && passenger['passenger_surname'] == null ) {
            textContent = passenger['passenger_name'];
          }

          if (passenger['passenger_name'] == null && passenger['passenger_surname'] !== null ) {
            textContent = passenger['passenger_surname'];
          }

          return {
            label: textContent,
            value: textContent,
          };
        });

        VirtualSelect.init({
          ele: '#taxi_passenger',
          multiple: true,
        });
        document.querySelector('#taxi_passenger').setOptions(passenger_options);

        var disabledOptions = [];
        passenger_options.forEach(option => {
          if (option.value != '') {
            disabledOptions.push(option.value);    
          }
        });

        $('#taxi_passenger').on('change', function () {
          selectedValues = document.querySelector('#taxi_passenger').getSelectedOptions();
            
        });

      }
 
    }
  })

}

$('#modalHotelInfo').on('show.bs.modal', function(){
  updateSelectHotelOptions();
  
});

$('#modalTaxiInfo').on('show.bs.modal', function(){
  updateSelectHotelOptions();
  updatePassengerList();
});


// Gestion des éVènements pour le choix du fournisseur d'hôtel
$(document).ready(function () {
  // SETUP
  const hotelSupplier = document.querySelector('#myHotelSupplier');
  const hsInput = hotelSupplier.querySelector('input');
  const hsList = hotelSupplier.querySelector('ul');

  let hsState = "initial";
  let hotel_supplier_list = []; // Assurez-vous que cette variable est définie ailleurs dans votre code

  // Configuration des attributs ARIA
  hotelSupplier.setAttribute('role', 'combobox');
  hotelSupplier.setAttribute('aria-haspopup', 'listbox');
  hotelSupplier.setAttribute('aria-owns', 'hotel-supplier-list');
  hsInput.setAttribute('aria-autocomplete', 'both');
  hsInput.setAttribute('aria-controls', 'hotel-supplier-list');
  hsList.setAttribute('role', 'listbox');

  // EVENEMENTS
  hotelSupplier.addEventListener('click', function (e) {
      const hsCurrentFocus = hsFindFocus();
      switch (hsState) {
          case 'initial':
              hsToggleList('Open');
              setState('opened');
              break;
          case 'opened':
              if (hsCurrentFocus === hsInput) {
                  hsToggleList('Shut');
                  setState('initial');
              } else if (hsCurrentFocus.tagName === 'LI') {
                  makeChoice(hsCurrentFocus);
                  hsToggleList('Shut');
                  setState('closed');
              }
              break;
          case 'filtered':
              if (hsCurrentFocus.tagName === 'LI') {
                  makeChoice(hsCurrentFocus);
                  hsToggleList('Shut');
                  setState('closed');
              }
              break;
          case 'closed':
              hsToggleList('Open');
              setState('filtered');
              break;
      }
  });

  hsInput.addEventListener('keyup', function (e) {
      doKeyAction(e.key);
  });

  document.addEventListener('click', function (e) {
      if (!e.target.closest('#myHotelSupplier')) {
        
        hsToggleList('Shut');
        setState('closed');
      }
  });

  // FONCTIONS
  function hsToggleList(whichWay) {
      if (whichWay === 'Open') {        
        hsList.classList.remove('hidden-all');
        hotelSupplier.setAttribute('aria-expanded', 'true');
      } else {
          hsList.classList.add('hidden-all');
          hotelSupplier.setAttribute('aria-expanded', 'false');
      }
  }

  function hsFindFocus() {
      return document.activeElement;
  }

  function makeChoice(whichOption) {
      hsInput.dataset.id = whichOption.dataset.id;
      hsInput.value = whichOption.textContent;
      hsMoveFocus(document.activeElement, 'input');
      setState('closed');
  }

  function setState(newState) {
      hsState = newState;
  }

  function doKeyAction(whichKey) {
      const hsCurrentFocus = hsFindFocus();
      switch (whichKey) {
          case 'Enter':
              let inputSupplier = hsInput.value.trim();
              if (inputSupplier !== '' && !hotel_supplier_list.some(s => s.name === inputSupplier)) {
                  hotel_supplier_list.push({ 'id': 0, 'name': inputSupplier });
                  refreshSupplierList();
              }
              hsToggleList('Open');
              setState('opened');
              break;
          case 'Escape':
              if (hsState === 'opened' || hsState === 'filtered') {
                  hsToggleList('Shut');
                  setState('initial');
              }
              break;
          default:
              if (hsState !== 'closed') {
                  hsToggleList('Open');
                  hsDoFilter();
                  setState('filtered');
              }
              break;
      }
  }

  function hsDoFilter() {
      const terms = hsInput.value.trim().toUpperCase();
      const items = document.querySelectorAll('.hotel-supplier-item');
      items.forEach(option => {
          option.style.display = option.textContent.toUpperCase().startsWith(terms) ? "" : "none";
      });
      setState('filtered');
  }

  function hsMoveFocus(fromHere, toThere) {
    var csOptions = document.querySelectorAll('.hotel-supplier-item');
    var aOptions = Array.from(csOptions);
    // grab the currently showing options, which might have been filtered
    const hsCurrentOptions = aOptions.filter(function(option) {
      if (option.style.display === '') {
        return true
      }
    })
    // don't move if all options have been filtered out
    if (hsCurrentOptions.length === 0) {
      return
    }
    if (toThere === 'input') {
      hsInput.focus()
    }
    // possible start points
    switch(fromHere) {
      case hsInput:
        if (toThere === 'forward') {
          hsCurrentOptions[0].focus()
        } else if (toThere === 'back') {
          hsCurrentOptions[hsCurrentOptions.length - 1].focus()
        }
        break
      case csOptions[0]: 
        if (toThere === 'forward') {
          hsCurrentOptions[1].focus()
        } else if (toThere === 'back') {
          hsInput.focus()
        }
        break
      case csOptions[csOptions.length - 1]:
        if (toThere === 'forward') {
          hsCurrentOptions[0].focus()
        } else if (toThere === 'back') {
          hsCurrentOptions[hsCurrentOptions.length - 2].focus()
        }
        break
      default: // middle list or filtered items 
        const currentItem = hsFindFocus()
        const whichOne = hsCurrentOptions.indexOf(currentItem)
        if (toThere === 'forward') {
          const nextOne = hsCurrentOptions[whichOne + 1]
          nextOne.focus()
        } else if (toThere === 'back' && whichOne > 0) {
          const previousOne = hsCurrentOptions[whichOne - 1]
          previousOne.focus()
        } else { // if whichOne = 0
          hsInput.focus()
        }
        break
    }
  }


  function refreshSupplierList() {
      const parent_hotel = document.getElementById("hotel-supplier-list");
      parent_hotel.innerHTML = ""; // Clear list before adding new elements
      hotel_supplier_list.forEach(supplier => {
          const newLi = document.createElement("li");
          newLi.className = "hotel-supplier-item";
          newLi.dataset.id = supplier.id;
          newLi.textContent = supplier.name;
          newLi.setAttribute('role', 'option');
          newLi.setAttribute('tabindex', "-1");
          parent_hotel.append(newLi);
      });
  }
});

// Gestion des évènements pour le choix du trajet de taxi
$(document).ready(function(){ 
  // SETUP
  // /////////////////////////////////
  // assign names to things we'll need to use more than once
  taxiSupplier = document.querySelector('#myTaxiSupplier'); // the input, svg and ul as a group
  const tsInput = taxiSupplier.querySelector('input');
  const tsList = taxiSupplier.querySelector('ul');
  const tsIcon = taxiSupplier.querySelector('svg');
  // const csStatus = document.querySelector('#custom-select-status');

  // when JS is loaded, set up our starting point
  // if JS fails to load, the custom select remains a plain text input
  // create and set start point for the state tracker
  let tsState = "initial";
  taxiSupplier.setAttribute('role', 'combobox') ;
  taxiSupplier.setAttribute('aria-haspopup', 'listbox') ;
  taxiSupplier.setAttribute('aria-owns', 'taxi-supplier-list') ;
  tsInput.setAttribute('aria-autocomplete', 'both') ;
  tsInput.setAttribute('aria-controls', 'taxi-supplier-list') ;// ...but the input controls it
  tsList.setAttribute('role', 'listbox') ;


  // EVENTS
  taxiSupplier.addEventListener('click', function(e) {
    console.log('CLICKED');
    console.log('TS STATE : ',tsState);
    const tsCurrentFocus = tsFindFocus()
    switch(tsState) {
      case 'initial' : // if state = initial, toggleOpen and set state to opened
        tsToggleList('Open') 
        tsSetState('opened')
        break
      case 'opened':
        // if state = opened and focus on input, toggleShut and set state to initial
        if (tsCurrentFocus === tsInput) {
          tsToggleList('Shut')
          tsSetState('initial')
        } else if (tsCurrentFocus.tagName === 'LI') {
          // if state = opened and focus on list, makeChoice, toggleShut and set state to closed
          tsMakeChoice(tsCurrentFocus)
          console.log('CURRENT FOCUS : ',tsCurrentFocus);
          tsToggleList('Shut')
          tsSetState('closed')
        }
        break
      case 'filtered':
        // if state = filtered and focus on list, makeChoice and set state to closed
        if (tsCurrentFocus.tagName === 'LI') {
          tsMakeChoice(tsCurrentFocus)
          tsToggleList('Shut')
          tsSetState('closed')
        } // if state = filtered and focus on input, do nothing (wait for next user input)

        break
      case 'closed': // if state = closed, toggleOpen and set state to filtered? or opened?
        tsToggleList('Open')
        tsSetState('filtered')
        break
    }
  })

  taxiSupplier.addEventListener('keyup', function(e) {
    tsDoKeyAction(e.key)
  })

  document.addEventListener('click', function(e) {
    if (!e.target.closest('#myTaxiSupplier')) {
      // click outside of the custom group
      tsToggleList('Shut')
      tsSetState('initial')
    } 
  })

  
    // FUNCTIONS 
    /////////////////////////////////
  
    function tsToggleList(whichWay) {
      if (whichWay === 'Open') {
        tsList.classList.remove('hidden-all')
        taxiSupplier.setAttribute('aria-expanded', 'true')
      } else { // === 'Shut'
        tsList.classList.add('hidden-all')
        taxiSupplier.setAttribute('aria-expanded', 'false')
      }
    }
  
    function tsFindFocus() {
      const focusPoint = document.activeElement
      return focusPoint
    }
  
    function tsMoveFocus(fromHere, toThere) {
      var csOptions = document.querySelectorAll('.taxi-supplier-item');
      var aOptions = Array.from(csOptions);
      // grab the currently showing options, which might have been filtered
      const tsCurrentOptions = aOptions.filter(function(option) {
        if (option.style.display === '') {
          return true
        }
      })
      // don't move if all options have been filtered out
      if (tsCurrentOptions.length === 0) {
        return
      }
      if (toThere === 'input') {
        tsInput.focus()
      }
      // possible start points
      switch(fromHere) {
        case tsInput:
          if (toThere === 'forward') {
              [0].focus()
          } else if (toThere === 'back') {
            tsCurrentOptions[tsCurrentOptions.length - 1].focus()
          }
          break
        case csOptions[0]: 
          if (toThere === 'forward') {
            tsCurrentOptions[1].focus()
          } else if (toThere === 'back') {
            tsInput.focus()
          }
          break
        case csOptions[csOptions.length - 1]:
          if (toThere === 'forward') {
            tsCurrentOptions[0].focus()
          } else if (toThere === 'back') {
            tsCurrentOptions[tsCurrentOptions.length - 2].focus()
          }
          break
        default: // middle list or filtered items 
          const currentItem = tsFindFocus()
          const whichOne = tsCurrentOptions.indexOf(currentItem)
          if (toThere === 'forward') {
            const nextOne = tsCurrentOptions[whichOne + 1]
            nextOne.focus()
          } else if (toThere === 'back' && whichOne > 0) {
            const previousOne = tsCurrentOptions[whichOne - 1]
            previousOne.focus()
          } else { // if whichOne = 0
            tsInput.focus()
          }
          break
      }
    }
  
    function tsDoFilter() {
  
      const terms = tsInput.value
      var csOptions = document.querySelectorAll('.taxi-supplier-item');
      var aOptions = Array.from(csOptions);
  
      const tsFilteredOptions = aOptions.filter(function(option) {
        if (option.innerText.toUpperCase().startsWith(terms.toUpperCase())) {
          return true
        }
      })
      csOptions.forEach(option => option.style.display = "none")
      tsFilteredOptions.forEach(function(option) {
        option.style.display = ""
      })
      tsSetState('filtered')
    }
  
    function tsMakeChoice(whichOption) {
      
      tsInput.setAttribute('data-id', whichOption.getAttribute('data-id'));
      tsInput.setAttribute('value',whichOption.textContent);
      tsInput.value = whichOption.textContent;
      tsMoveFocus(document.activeElement, 'input')
      tsSetState('closed');
      
    }
  
    function tsSetState(newState) {
      switch (newState) {
        case 'initial': 
          tsState = 'initial'
          break
        case 'opened': 
          tsState = 'opened'
          break
        case 'filtered':
          tsState = 'filtered'
          break
        case 'closed': 
          tsState = 'closed'
      }
    }
  
    function tsDoKeyAction(whichKey) {
      const tsCurrentFocus = tsFindFocus()

      switch(whichKey) {
        case 'Enter':
          var inputsupplier = $("#taxi-supplier-input").val();
          if (inputsupplier.trim() !== '') {
            taxi_supplier_list.push({'id':0,'name':inputsupplier});
            var taxi_suplier = document.getElementById("taxi-supplier-list")
            var taxi_childs = document.querySelectorAll(".taxi-supplier-item")
            if (taxi_childs) {
              taxi_childs.forEach(element => {
                element.remove();
              });

            }

            refreshTSupplierList();
          }

          tsToggleList('Open')
          tsSetState('opened')
          break
  
        case 'Escape':
          // if state = initial, do nothing
          // if state = opened or filtered, set state to initial
          // if state = closed, do nothing
          if (tsState === 'opened' || tsState === 'filtered') {
            tsToggleList('Shut')
            tsSetState('initial')
          }
          break
        default:
          if (tsState === 'initial') {
            // if state = initial, toggle open, tsDoFilter and set state to filtered
            tsToggleList('Open')
            tsDoFilter()
            tsSetState('filtered')
          } else if (tsState === 'opened') {
            // if state = opened, tsDoFilter and set state to filtered
            tsDoFilter()
            tsSetState('filtered')
          } else if (tsState === 'closed') {
            // if state = closed, tsDoFilter and set state to filtered
            tsDoFilter()
            tsSetState('filtered')
          } else { // already filtered
            tsDoFilter()
          }
          break 
      }
    }

    function refreshTSupplierList() {
      const parent_taxi = document.getElementById("taxi-supplier-list");
      parent_taxi.innerHTML = ""; // Clear list before adding new elements
      taxi_supplier_list.forEach(supplier => {
          const newTLi = document.createElement("li");
          newTLi.className = "taxi-supplier-item";
          newTLi.dataset.id = supplier.id;
          newTLi.textContent = supplier.name;
          newTLi.setAttribute('role', 'option');
          newTLi.setAttribute('tabindex', "-1");
          parent_taxi.append(newTLi);
      });
    }

})


// Enregistrer la reservation d'hôtel
$('#ConfirmAddHotel').on('click', function(){
  const name = document.getElementById('hotel-supplier-input').value;
  const arrivalDate = document.getElementById('arrivalDate').value;
  const departureDate = document.getElementById('departureDate').value;
  const hotel_client = document.getElementById('hotel_client').value;

  if (!name || !arrivalDate || !departureDate || !hotel_client) {
    toastr.error('Veuillez remplir tous les champs.');
    return;
  }

  const formattedArrivalDate = (new Date(arrivalDate)).toLocaleDateString('fr-FR');
  const formattedDepartureDate = (new Date(departureDate)).toLocaleDateString('fr-FR');

  $('#ht_details').show();

  $('#ht_details').append(`<p>Hotel :${name}<br/>`);
  $('#ht_details').append(`Arrivée : ${formattedArrivalDate}</br>`);
  $('#ht_details').append(`Sortie : ${formattedDepartureDate}</p>`);

  $('#passenger_segment').hide()
  $('#ht_passenger').show();
  $('#ht_passenger').append(`<p>Client :${hotel_client}</p>`);

 // Enregistrer le fournisseur s'il est nouveau    
  hotel_input = document.getElementById('hotel-supplier-input')    
  data_id = hotel_input.getAttribute('data-id');
  console.log('hotel_input : ', hotel_input);
  if (data_id == 0) {
    addServiceSupplier(name,10);
  }

  // Enregistrer toutes les informations dans sessionStorage
  hotel_info = {'name':name,'arrivalDate':arrivalDate,'departureDate':departureDate,'client':hotel_client};
  sessionStorage.setItem('hotel_info',JSON.stringify(hotel_info));

  toastr.success('Informations ajoutées.')


})

// Enregistrer la reservation de taxi
$('#ConfirmAddTaxi').on('click', function(){ 
  var taxiDate = document.getElementById('taxiDate').value;
  var taxi_passenger = document.querySelector('#taxi_passenger').getSelectedOptions();
  var trajet = document.getElementById('taxi-supplier-input').value;
  var taxiDepartureTime = document.getElementById('taxiDepartureTime').value;
  var taxiArrivalTime = document.getElementById('taxiArrivalTime').value;
  var taximan = document.getElementById('taximan').value;


  if(!taxiDate || !trajet || !taxiDepartureTime || !taxiArrivalTime || !taxi_passenger){
    toastr.error('Veuillez remplir tous les champs.');
    return;
  }

  const formattedtaxiDate = (new Date(taxiDate)).toLocaleDateString('fr-FR');
  console.log("taxi passenger : ",taxi_passenger);

  $('#ht_details').show();
  $('#passenger_segment').hide()
  $('#ht_passenger').show();
  
  taxi_passengers = [];
  taxi_passenger.forEach(element => {
    console.log("taxi passenger value : ", element.value);
    taxi_passengers.push(element.value);
    $('#ht_passenger').append(`<p>${element.value}</p>`);
  });
  if(taximan.trim() != ""){
    $('#ht_details').append(`<p>Chauffeur :${taximan}<br/>`);
  }
  
  $('#ht_details').append(`Trajet :${trajet}<br/>`);
  $('#ht_details').append(`Départ : ${formattedtaxiDate} ${taxiDepartureTime} </br>`);
  $('#ht_details').append(`Arrivé : ${formattedtaxiDate} ${taxiArrivalTime} </p>`);


 // Enregistrer le fournisseur s'il est nouveau 
  taxi_input = document.getElementById('taxi-supplier-input')
  data_id = taxi_input.getAttribute('data-id');
  if (data_id == 0) {
    addServiceSupplier(trajet,12);
  }
  // Enregistrer toutes les informations dans sessionStorage

  taxi_details = {'trajet':trajet,'date':taxiDate,'departureTime':taxiDepartureTime,'arrivalTime':taxiArrivalTime,'taxiPassenger':taxi_passengers,'taximan':taximan};
  sessionStorage.setItem('taxi_details',JSON.stringify(taxi_details));

  toastr.success('Informations ajoutées.')

})


// Ajouter un fournisseur 
function addServiceSupplier(supplier_name, service_id){
  console.log('Service supplier added !!!!');
  $.ajax({
    type: "POST",
    url: "/home/add-service-supplier",
    dataType: "json",
    data:{
        name : supplier_name,
        service : service_id,
        csrfmiddlewaretoken: csrftoken,
    },
    success: (response) => {
        console.log(`response`, response);
      toastr.success(response.message)
    },
    error: (error) => {
        console.log(`error`, error);
    }
  })
}