const car_suppliers_list = [];

$('#modalLocationInfo').on('hidden.bs.modal', function () {
  console.log("Modal Location fermé");
  if(!sessionStorage.getItem('location_details')){ $('#SelectProduct').val(''); }

});


$('#SelectProduct').on('change', function(){
  select_product = $('#SelectProduct').val();

});

function updateSelectLocationOptions() {

    const parent_location = document.getElementById("location-supplier-list")

    const location_child = document.getElementById("location-supplier-item")


      if (location_child) {
        parent_location.removeChild(location_child);
      }

      var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            
            if (this.readyState == 4 && this.status == 200) {
                                        
            var response = JSON.parse(this.responseText);
            
            const car_suppliers = Array.from(response.car_suppliers);

            parent_location.innerHTML = '';

            // Ajouter des options au choix des classes du Bus

            car_suppliers.map((supplier) =>{
              car_suppliers_list.push(supplier);
              var location_li = document.createElement("li");
              location_li.className="location-supplier-item";
              location_li.setAttribute("data-id", supplier.id);
              location_li.textContent = supplier.name;
              location_li.setAttribute('role', 'option') ;
              location_li.setAttribute('tabindex', "-1") ;
              parent_location.append(location_li);

            });


        }
    };
    xmlhttp.open("GET", '/home/get-service-supplier-list', true);
    xmlhttp.send();
}

$('#modalLocationInfo').on('show.bs.modal', function(){
  updateSelectLocationOptions();
});

// Gestion des évènements pour le choix de la classe du Bus
$(document).ready(function(){ 
  // SETUP
  // /////////////////////////////////
  // assign names to things we'll need to use more than once
  locationSupplier = document.querySelector('#myLocationSupplier'); // the input, svg and ul as a group
  const locationInput = locationSupplier.querySelector('input');
  const locationList = locationSupplier.querySelector('ul');
  const locationIcon = locationSupplier.querySelector('svg');
  // const csStatus = document.querySelector('#custom-select-status');

  // when JS is loaded, set up our starting point
  // if JS fails to load, the custom select remains a plain text input
  // create and set start point for the state tracker
  let locationState = "initial";
  locationSupplier.setAttribute('role', 'combobox') ;
  locationSupplier.setAttribute('aria-haspopup', 'listbox') ;
  locationSupplier.setAttribute('aria-owns', 'location-supplier-list') ;
  locationInput.setAttribute('aria-autocomplete', 'both') ;
  locationInput.setAttribute('aria-controls', 'location-supplier-list') ;// ...but the input controls it
  locationList.setAttribute('role', 'listbox') ;


  // EVENTS
  locationSupplier.addEventListener('click', function(e) {
    console.log('CLICKED');
    console.log('BS STATE : ',locationState);
    const locationCurrentFocus = locationFindFocus()
    switch(locationState) {
      case 'initial' : // if state = initial, toggleOpen and set state to opened
        locationToggleList('Open') 
        locationSetState('opened')
        break
      case 'opened':
        // if state = opened and focus on input, toggleShut and set state to initial
        if (locationCurrentFocus === locationInput) {
          locationToggleList('Shut')
          locationSetState('initial')
        } else if (locationCurrentFocus.tagName === 'LI') {
          // if state = opened and focus on list, makeChoice, toggleShut and set state to closed
          locationMakeChoice(locationCurrentFocus)
          console.log('CURRENT FOCUS : ',locationCurrentFocus);
          locationToggleList('Shut')
          locationSetState('closed')
        }
        break
      case 'filtered':
        // if state = filtered and focus on list, makeChoice and set state to closed
        if (locationCurrentFocus.tagName === 'LI') {
          locationMakeChoice(locationCurrentFocus)
          locationToggleList('Shut')
          locationSetState('closed')
        } // if state = filtered and focus on input, do nothing (wait for next user input)

        break
      case 'closed': // if state = closed, toggleOpen and set state to filtered? or opened?
        locationToggleList('Open')
        locationSetState('filtered')
        break
    }
  })

  locationSupplier.addEventListener('keyup', function(e) {
    locationDoKeyAction(e.key)
  })

  document.addEventListener('click', function(e) {
    if (!e.target.closest('#myLocationSupplier')) {
      // click outside of the custom group
      locationToggleList('Shut')
      locationSetState('initial')
    } 
  })

  
    // FUNCTIONS 
    /////////////////////////////////
  
    function locationToggleList(whichWay) {
      if (whichWay === 'Open') {
        locationList.classList.remove('hidden-all')
        locationSupplier.setAttribute('aria-expanded', 'true')
      } else { // === 'Shut'
        locationList.classList.add('hidden-all')
        locationSupplier.setAttribute('aria-expanded', 'false')
      }
    }
  
    function locationFindFocus() {
      const focusPoint = document.activeElement
      return focusPoint
    }
  
    function locationMoveFocus(fromHere, toThere) {
      var ltOptions = document.querySelectorAll('.taxi-supplier-item');
      var aOptions = Array.from(ltOptions);
      // grab the currently showing options, which might have been filtered
      const locationCurrentOptions = aOptions.filter(function(option) {
        if (option.style.display === '') {
          return true
        }
      })
      // don't move if all options have been filtered out
      if (locationCurrentOptions.length === 0) {
        return
      }
      if (toThere === 'input') {
        locationInput.focus()
      }
      // possible start points
      switch(fromHere) {
        case locationInput:
          if (toThere === 'forward') {
              [0].focus()
          } else if (toThere === 'back') {
            locationCurrentOptions[locationCurrentOptions.length - 1].focus()
          }
          break
        case ltOptions[0]: 
          if (toThere === 'forward') {
            locationCurrentOptions[1].focus()
          } else if (toThere === 'back') {
            locationInput.focus()
          }
          break
        case ltOptions[ltOptions.length - 1]:
          if (toThere === 'forward') {
            locationCurrentOptions[0].focus()
          } else if (toThere === 'back') {
            locationCurrentOptions[locationCurrentOptions.length - 2].focus()
          }
          break
        default: // middle list or filtered items 
          const currentItem = locationFindFocus()
          const whichOne = locationCurrentOptions.indexOf(currentItem)
          if (toThere === 'forward') {
            const nextOne = locationCurrentOptions[whichOne + 1]
            nextOne.focus()
          } else if (toThere === 'back' && whichOne > 0) {
            const previousOne = locationCurrentOptions[whichOne - 1]
            previousOne.focus()
          } else { // if whichOne = 0
            locationInput.focus()
          }
          break
      }
    }
  
    function locationDoFilter() {
  
      const terms = locationInput.value
      var ltOptions = document.querySelectorAll('.location-supplier-item');
      var aOptions = Array.from(ltOptions);
  
      const locationFilteredOptions = aOptions.filter(function(option) {
        if (option.innerText.toUpperCase().startsWith(terms.toUpperCase())) {
          return true
        }
      })
      ltOptions.forEach(option => option.style.display = "none")
      locationFilteredOptions.forEach(function(option) {
        option.style.display = ""
      })
      locationSetState('filtered')
    }
  
    function locationMakeChoice(whichOption) {
      
      locationInput.setAttribute('data-id', whichOption.getAttribute('data-id'));
      locationInput.setAttribute('value',whichOption.textContent);
      locationInput.value = whichOption.textContent;
      locationMoveFocus(document.activeElement, 'input')
      locationSetState('closed');
      
    }
  
    function locationSetState(newState) {
      switch (newState) {
        case 'initial': 
          locationState = 'initial'
          break
        case 'opened': 
          locationState = 'opened'
          break
        case 'filtered':
          locationState = 'filtered'
          break
        case 'closed': 
          locationState = 'closed'
      }
    }
  
    function locationDoKeyAction(whichKey) {
      const locationCurrentFocus = locationFindFocus()

      switch(whichKey) {
        case 'Enter':
          var inputsupplier = $("#location-supplier-input").val();
          if (inputsupplier.trim() !== '') {
            car_suppliers_list.push({'id':0,'name':inputsupplier});
            var location_suplier = document.getElementById("location-supplier-list")
            var location_childs = document.querySelectorAll(".location-supplier-item")
            if (location_childs) {
              location_childs.forEach(element => {
                element.remove();
              });

            }

            refreshBSupplierList();
          }

          locationToggleList('Open')
          locationSetState('opened')
          break
  
        case 'Escape':
          // if state = initial, do nothing
          // if state = opened or filtered, set state to initial
          // if state = closed, do nothing
          if (locationState === 'opened' || locationState === 'filtered') {
            locationToggleList('Shut')
            locationSetState('initial')
          }
          break
        default:
          if (locationState === 'initial') {
            // if state = initial, toggle open, tsDoFilter and set state to filtered
            locationToggleList('Open')
           locationDoFilter()
            locationSetState('filtered')
          } else if (locationState === 'opened') {
            // if state = opened, locationDoFilter and set state to filtered
           locationDoFilter()
            locationSetState('filtered')
          } else if (locationState === 'closed') {
            // if state = closed, locationDoFilter and set state to filtered
           locationDoFilter()
            locationSetState('filtered')
          } else { // already filtered
           locationDoFilter()
          }
          break 
      }
    }

    function refreshBSupplierList() {
      const parent_location = document.getElementById("location-supplier-list");
      parent_location.innerHTML = ""; // Clear list before adding new elements
      car_suppliers_list.forEach(supplier => {
          const newLTi = document.createElement("li");
          newLTi.className = "location-supplier-item";
          newLTi.dataset.id = supplier.id;
          newLTi.textContent = supplier.name;
          newLTi.setAttribute('role', 'option');
          newLTi.setAttribute('tabindex', "-1");
          parent_location.append(newLTi);
      });
  }

})


// Enregistrer la reservation de bus
$('#ConfirmAddLocation').on('click', function(){ 
  var conducteur = document.getElementById('conducteur').value;
  var locationSupplier = document.getElementById('location-supplier-input').value;
  var modele = document.getElementById('modele').value;
  var date_prise_car = document.getElementById('date_prise_car').value;
  var time_prise_car = document.getElementById('time_prise_car').value;
  var lieu_car = document.getElementById('lieu_car').value;

  var date_return_car = document.getElementById('date_return_car').value;
  var time_return_car = document.getElementById('time_return_car').value;
  var lieu_return_car = document.getElementById('lieu_return_car').value;
  


  if(!conducteur || !locationSupplier || !modele || !date_prise_car || !time_prise_car || !lieu_car || !date_return_car || !time_return_car || !lieu_return_car ){
    toastr.error('Veuillez remplir tous les champs.');
    return;
  }

  const date_formatted_prise_car = (new Date(date_prise_car)).toLocaleDateString('fr-FR');
  const date_formatted_return_car = (new Date(date_return_car)).toLocaleDateString('fr-FR');


  $('#ht_details').show();
  $('#passenger_segment').hide()

  $('#ht_details').append(`<p>Fournisseur :${locationSupplier}<br/>`);
  $('#ht_details').append(`<p>Conducteur :${conducteur}<br/>`);
  $('#ht_details').append(`<p>Modèle :${modele}<br/>`);

  $('#ht_details').append(`Prise du Véhicule : </br>`);
  $('#ht_details').append(`Lieu : ${lieu_car} - ${date_formatted_prise_car} ${time_prise_car} </p>`);

  $('#ht_details').append(`Restitution du Véhicule : </br>`);
  $('#ht_details').append(`Lieu : ${lieu_return_car} - ${date_formatted_return_car} ${time_return_car} </p>`);

 // Enregistrer le fournisseur s'il est nouveau 
  location_input = document.getElementById('location-supplier-input')
  data_id = location_input.getAttribute('data-id');
  if (data_id == 0) {
    addServiceSupplier(locationSupplier,11);
  }
  // Enregistrer toutes les informations dans sessionStorage

  location_details = {'fournisseur':locationSupplier,'conducteur':conducteur,'modele':modele,'lieu_prise':lieu_car,'date_prise':date_prise_car,'heure_prise':time_prise_car,'lieu_return':lieu_return_car,'date_return':date_return_car,'heure_return':time_return_car};
  sessionStorage.setItem('location_details',JSON.stringify(location_details));

  toastr.success('Informations ajoutées.')

})
