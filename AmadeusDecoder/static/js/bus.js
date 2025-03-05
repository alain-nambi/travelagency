const bus_supplier_list = [];

$('#modalBusInfo').on('hidden.bs.modal', function () {
  console.log("Modal Bus fermé");
  if(!sessionStorage.getItem('bus_details')){ $('#SelectProduct').val(''); }

});


$('#SelectProduct').on('change', function(){
  select_product = $('#SelectProduct').val();

});

function updateSelectBusOptions() {

    const parent_bus = document.getElementById("bus-supplier-list")

    const bus_child = document.getElementById("bus-supplier-item")


      if (bus_child) {
        parent_bus.removeChild(bus_child);
      }

      var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            
            if (this.readyState == 4 && this.status == 200) {
                                        
            var response = JSON.parse(this.responseText);
            
            const bus_classes = Array.from(response.bus_classes);

            parent_bus.innerHTML = '';

            // Ajouter des options au choix des classes du Bus

            bus_classes.map((supplier) =>{
              bus_supplier_list.push(supplier);
              var busli = document.createElement("li");
              busli.className="bus-supplier-item";
              busli.setAttribute("data-id", supplier.id);
              busli.textContent = supplier.name;
              busli.setAttribute('role', 'option') ;
              busli.setAttribute('tabindex', "-1") ;
              parent_bus.append(busli);

            });


        }
    };
    xmlhttp.open("GET", '/home/get-service-supplier-list', true);
    xmlhttp.send();
}

function updateBusPassengerList(){
  
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
          $('#bus_passenger').hide();
      }
      if (passengers.length > 0) {
        const bus_passenger_options = passengers.map((passenger) => {
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
          ele: '#bus_passenger',
          multiple: true,
        });
        document.querySelector('#bus_passenger').setOptions(bus_passenger_options);

        let disabledOptions = [];
        bus_passenger_options.forEach(option => {
          if (option.value != '') {
            disabledOptions.push(option.value);    
          }
        });

        $('#bus_passenger').on('change', function () {
          selectedValues = document.querySelector('#bus_passenger').getSelectedOptions();
            
        });

      }
 
    }
  })

}


$('#modalBusInfo').on('show.bs.modal', function(){
  updateSelectBusOptions();
  updateBusPassengerList();
});

// Gestion des évènements pour le choix de la classe du Bus
$(document).ready(function(){ 
  // SETUP
  // /////////////////////////////////
  // assign names to things we'll need to use more than once
  busSupplier = document.querySelector('#myBusSupplier'); // the input, svg and ul as a group
  const bsInput = busSupplier.querySelector('input');
  const bsList = busSupplier.querySelector('ul');
  const bsIcon = busSupplier.querySelector('svg');
  // const csStatus = document.querySelector('#custom-select-status');

  // when JS is loaded, set up our starting point
  // if JS fails to load, the custom select remains a plain text input
  // create and set start point for the state tracker
  let bsState = "initial";
  busSupplier.setAttribute('role', 'combobox') ;
  busSupplier.setAttribute('aria-haspopup', 'listbox') ;
  busSupplier.setAttribute('aria-owns', 'bus-supplier-list') ;
  bsInput.setAttribute('aria-autocomplete', 'both') ;
  bsInput.setAttribute('aria-controls', 'bus-supplier-list') ;// ...but the input controls it
  bsList.setAttribute('role', 'listbox') ;


  // EVENTS
  busSupplier.addEventListener('click', function(e) {
    console.log('CLICKED');
    console.log('BS STATE : ',bsState);
    const bsCurrentFocus = bsFindFocus()
    switch(bsState) {
      case 'initial' : // if state = initial, toggleOpen and set state to opened
        bsToggleList('Open') 
        bsSetState('opened')
        break
      case 'opened':
        // if state = opened and focus on input, toggleShut and set state to initial
        if (bsCurrentFocus === bsInput) {
          bsToggleList('Shut')
          bsSetState('initial')
        } else if (bsCurrentFocus.tagName === 'LI') {
          // if state = opened and focus on list, makeChoice, toggleShut and set state to closed
          bsMakeChoice(bsCurrentFocus)
          console.log('CURRENT FOCUS : ',bsCurrentFocus);
          bsToggleList('Shut')
          bsSetState('closed')
        }
        break
      case 'filtered':
        // if state = filtered and focus on list, makeChoice and set state to closed
        if (bsCurrentFocus.tagName === 'LI') {
          bsMakeChoice(bsCurrentFocus)
          bsToggleList('Shut')
          bsSetState('closed')
        } // if state = filtered and focus on input, do nothing (wait for next user input)

        break
      case 'closed': // if state = closed, toggleOpen and set state to filtered? or opened?
        bsToggleList('Open')
        bsSetState('filtered')
        break
    }
  })

  busSupplier.addEventListener('keyup', function(e) {
    bsDoKeyAction(e.key)
  })

  document.addEventListener('click', function(e) {
    if (!e.target.closest('#myBusSupplier')) {
      // click outside of the custom group
      bsToggleList('Shut')
      bsSetState('initial')
    } 
  })

  
    // FUNCTIONS 
    /////////////////////////////////
  
    function bsToggleList(whichWay) {
      if (whichWay === 'Open') {
        bsList.classList.remove('hidden-all')
        busSupplier.setAttribute('aria-expanded', 'true')
      } else { // === 'Shut'
        bsList.classList.add('hidden-all')
        busSupplier.setAttribute('aria-expanded', 'false')
      }
    }
  
    function bsFindFocus() {
      const focusPoint = document.activeElement
      return focusPoint
    }
  
    function bsMoveFocus(fromHere, toThere) {
      var csOptions = document.querySelectorAll('.taxi-supplier-item');
      var aOptions = Array.from(csOptions);
      // grab the currently showing options, which might have been filtered
      const bsCurrentOptions = aOptions.filter(function(option) {
        if (option.style.display === '') {
          return true
        }
      })
      // don't move if all options have been filtered out
      if (bsCurrentOptions.length === 0) {
        return
      }
      if (toThere === 'input') {
        bsInput.focus()
      }
      // possible start points
      switch(fromHere) {
        case bsInput:
          if (toThere === 'forward') {
              [0].focus()
          } else if (toThere === 'back') {
            bsCurrentOptions[bsCurrentOptions.length - 1].focus()
          }
          break
        case csOptions[0]: 
          if (toThere === 'forward') {
            bsCurrentOptions[1].focus()
          } else if (toThere === 'back') {
            bsInput.focus()
          }
          break
        case csOptions[csOptions.length - 1]:
          if (toThere === 'forward') {
            bsCurrentOptions[0].focus()
          } else if (toThere === 'back') {
            bsCurrentOptions[bsCurrentOptions.length - 2].focus()
          }
          break
        default: // middle list or filtered items 
          const currentItem = bsFindFocus()
          const whichOne = bsCurrentOptions.indexOf(currentItem)
          if (toThere === 'forward') {
            const nextOne = bsCurrentOptions[whichOne + 1]
            nextOne.focus()
          } else if (toThere === 'back' && whichOne > 0) {
            const previousOne = bsCurrentOptions[whichOne - 1]
            previousOne.focus()
          } else { // if whichOne = 0
            bsInput.focus()
          }
          break
      }
    }
  
    function bsDoFilter() {
  
      const terms = bsInput.value
      var csOptions = document.querySelectorAll('.bus-supplier-item');
      var aOptions = Array.from(csOptions);
  
      const bsFilteredOptions = aOptions.filter(function(option) {
        if (option.innerText.toUpperCase().startsWith(terms.toUpperCase())) {
          return true
        }
      })
      csOptions.forEach(option => option.style.display = "none")
      bsFilteredOptions.forEach(function(option) {
        option.style.display = ""
      })
      bsSetState('filtered')
    }
  
    function bsMakeChoice(whichOption) {
      
      bsInput.setAttribute('data-id', whichOption.getAttribute('data-id'));
      bsInput.setAttribute('value',whichOption.textContent);
      bsInput.value = whichOption.textContent;
      bsMoveFocus(document.activeElement, 'input')
      bsSetState('closed');
      
    }
  
    function bsSetState(newState) {
      switch (newState) {
        case 'initial': 
          bsState = 'initial'
          break
        case 'opened': 
          bsState = 'opened'
          break
        case 'filtered':
          bsState = 'filtered'
          break
        case 'closed': 
          bsState = 'closed'
      }
    }
  
    function bsDoKeyAction(whichKey) {
      const bsCurrentFocus = bsFindFocus()

      switch(whichKey) {
        case 'Enter':
          var inputsupplier = $("#bus-supplier-input").val();
          if (inputsupplier.trim() !== '') {
            bus_supplier_list.push({'id':0,'name':inputsupplier});
            var bus_suplier = document.getElementById("bus-supplier-list")
            var bus_childs = document.querySelectorAll(".bus-supplier-item")
            if (bus_childs) {
              bus_childs.forEach(element => {
                element.remove();
              });

            }

            refreshBSupplierList();
          }

          bsToggleList('Open')
          bsSetState('opened')
          break
  
        case 'Escape':
          // if state = initial, do nothing
          // if state = opened or filtered, set state to initial
          // if state = closed, do nothing
          if (bsState === 'opened' || bsState === 'filtered') {
            bsToggleList('Shut')
            bsSetState('initial')
          }
          break
        default:
          if (bsState === 'initial') {
            // if state = initial, toggle open, tsDoFilter and set state to filtered
            bsToggleList('Open')
            bsDoFilter()
            bsSetState('filtered')
          } else if (bsState === 'opened') {
            // if state = opened, bsDoFilter and set state to filtered
            bsDoFilter()
            bsSetState('filtered')
          } else if (bsState === 'closed') {
            // if state = closed, bsDoFilter and set state to filtered
            bsDoFilter()
            bsSetState('filtered')
          } else { // already filtered
            bsDoFilter()
          }
          break 
      }
    }

    function refreshBSupplierList() {
      const parent_bus = document.getElementById("bus-supplier-list");
      parent_bus.innerHTML = ""; // Clear list before adding new elements
      bus_supplier_list.forEach(supplier => {
          const newBLi = document.createElement("li");
          newBLi.className = "bus-supplier-item";
          newBLi.dataset.id = supplier.id;
          newBLi.textContent = supplier.name;
          newBLi.setAttribute('role', 'option');
          newBLi.setAttribute('tabindex', "-1");
          parent_bus.append(newBLi);
      });
  }

})


// Enregistrer la reservation de bus
$('#ConfirmAddBus').on('click', function(){ 
  var bus_trajet = document.getElementById('bus_trajet').value;
  var bus_class = document.getElementById('bus-supplier-input').value;
  var busDate = document.getElementById('busDate').value;
  var busArrivalTime = document.getElementById('busArrivalTime').value;
  var busDepartureTime = document.getElementById('busDepartureTime').value;
  var bus_passenger = document.querySelector('#bus_passenger').getSelectedOptions();
  console.log("BUS PASSEGER : ",bus_passenger);
  

  if(!bus_trajet || !bus_class || !busDate || !busArrivalTime || !busDepartureTime || !bus_passenger){
    toastr.error('Veuillez remplir tous les champs.');
    return;
  }

  const busFormattedDate = (new Date(busDate)).toLocaleDateString('fr-FR');

  $('#ht_details').show();
  $('#passenger_segment').hide()

  bus_passengers = [];
  bus_passenger.forEach(element => {
    console.log("bus passenger value : ", element.value);
    bus_passengers.push(element.value);
    $('#ht_passenger').append(`<p>${element.value}</p>`);
  })

  $('#ht_details').append(`<p>Trajet/Classe :${bus_trajet}/ ${bus_class} <br/>`);
  $('#ht_details').append(`Départ : ${busFormattedDate} ${busDepartureTime} </br>`);
  $('#ht_details').append(`Arrivé : ${busFormattedDate} ${busArrivalTime} </p>`);


 // Enregistrer le fournisseur s'il est nouveau 
  bus_input = document.getElementById('bus-supplier-input')
  data_id = bus_input.getAttribute('data-id');
  if (data_id == 0) {
    addServiceSupplier(bus_class,9);
  }
  // Enregistrer toutes les informations dans sessionStorage

  bus_details = {'trajet':bus_trajet,'classe':bus_class,'date':busDate,'departureTime':busDepartureTime,'arrivalTime':busArrivalTime,'passenger':bus_passengers};
  sessionStorage.setItem('bus_details',JSON.stringify(bus_details));

  toastr.success('Informations ajoutées.')

})
