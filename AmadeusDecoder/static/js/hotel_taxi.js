const hotel_supplier_list = [];
const taxi_supplier_list = [];
const departure_location_list = [];


$('#SelectProduct').on('change', function(){
  select_product = $('#SelectProduct').val();

  if(select_product == 10){
    $('#modalHotelInfo').modal("show");
  }

  if(select_product == 12){
    $('#modalTaxiInfo').modal("show");
  }
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
              newli.setAttribute("data-value", supplier.id);
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

$('#modalHotelInfo').on('show.bs.modal', function(){
  updateSelectHotelOptions();
});

$('#modalTaxiInfo').on('show.bs.modal', function(){
  updateSelectHotelOptions();
});

// Gestion des écènements pour le choix du fournisseur d'hôtel
$(document).ready(function(){
    // SETUP
    // /////////////////////////////////
    // assign names to things we'll need to use more than once
    const hotelSupplier = document.querySelector('#myHotelSupplier'); // the input, svg and ul as a group
    const hsInput = hotelSupplier.querySelector('input');
    const hsList = hotelSupplier.querySelector('ul');
    const hsIcons = hotelSupplier.querySelector('svg');
    // const csStatus = document.querySelector('#custom-select-status');
  
    // when JS is loaded, set up our starting point
    // if JS fails to load, the custom select remains a plain text input
    // create and set start point for the state tracker
    let hsState = "initial";
    // inform assistive tech (screen readers) of the names & roles of the elements in our group
    hotelSupplier.setAttribute('role', 'combobox') ;
    hotelSupplier.setAttribute('aria-haspopup', 'listbox') ;
    hotelSupplier.setAttribute('aria-owns', 'hotel-supplier-list') ;// container owns the list...
    hsInput.setAttribute('aria-autocomplete', 'both') ;
    hsInput.setAttribute('aria-controls', 'hotel-supplier-list') ;// ...but the input controls it
    hsList.setAttribute('role', 'listbox') ;
  
  
    // EVENTS
    // /////////////////////////////////
    hotelSupplier.addEventListener('click', function(e) {
      const hsCurrentFocus = hsFindFocus()
      switch(hsState) {
        case 'initial' : // if state = initial, toggleOpen and set state to opened
          hsToggleList('Open')
          setState('opened')
          break
        case 'opened':
          // if state = opened and focus on input, toggleShut and set state to initial
          if (hsCurrentFocus === hsInput) {
            hsToggleList('Shut')
            setState('initial')
          } else if (hsCurrentFocus.tagName === 'LI') {
            // if state = opened and focus on list, makeChoice, toggleShut and set state to closed
            makeChoice(hsCurrentFocus)
            hsToggleList('Shut')
            setState('closed')
          }
          break
        case 'filtered':
          // if state = filtered and focus on list, makeChoice and set state to closed
          if (hsCurrentFocus.tagName === 'LI') {
            makeChoice(hsCurrentFocus)
            hsToggleList('Shut')
            setState('closed')
          } // if state = filtered and focus on input, do nothing (wait for next user input)
  
          break
        case 'closed': // if state = closed, toggleOpen and set state to filtered? or opened?
          hsToggleList('Open')
          setState('filtered')
          break
      }
    })
  
    hotelSupplier.addEventListener('keyup', function(e) {
      doKeyAction(e.key)
    })
  
    document.addEventListener('click', function(e) {
      if (!e.target.closest('#myHotelSupplier')) {
        // click outside of the custom group
        hsToggleList('Shut')
        setState('initial')
      } 
    })
    
      // FUNCTIONS 
      // /////////////////////////////////
    
      function hsToggleList(whichWay) {
        if (whichWay === 'Open') {
          hsList.classList.remove('hidden-all')
          hotelSupplier.setAttribute('aria-expanded', 'true')
        } else { // === 'Shut'
          hsList.classList.add('hidden-all')
          hotelSupplier.setAttribute('aria-expanded', 'false')
        }
      }
    
      function hsFindFocus() {
        const focusPoint = document.activeElement
        return focusPoint
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
    
      function hsDoFilter() {
    
        const terms = hsInput.value
        var csOptions = document.querySelectorAll('.hotel-supplier-item');
        var aOptions = Array.from(csOptions);
    
        const hsFilteredOptions = aOptions.filter(function(option) {
          if (option.innerText.toUpperCase().startsWith(terms.toUpperCase())) {
            return true
          }
        })
        csOptions.forEach(option => option.style.display = "none")
        hsFilteredOptions.forEach(function(option) {
          option.style.display = ""
        })
        setState('filtered')
      }
    

      function makeChoice(whichOption) {
        hsInput.setAttribute('data-id', whichOption.getAttribute('data-value'));
        hsInput.setAttribute('value',whichOption.textContent);
        hsMoveFocus(document.activeElement, 'input')
        setState('closed');
        
        // update aria-selected, if using
      }
    
      function setState(newState) {
        switch (newState) {
          case 'initial': 
            hsState = 'initial'
            break
          case 'opened': 
            hsState = 'opened'
            break
          case 'filtered':
            hsState = 'filtered'
            break
          case 'closed': 
            hsState = 'closed'
        }
        // console.log({hsState})
      }
    
      function doKeyAction(whichKey) {
        const hsCurrentFocus = hsFindFocus()
  
        switch(whichKey) {
          case 'Enter':
            var inputsupplier = $("#hotel-supplier-input").val();
            if (inputsupplier.trim() !== '') {
              hotel_supplier_list.push({'id':'','name':inputsupplier});
              var parent_hotel = document.getElementById("hotel-supplier-list")
              var hotel_childs = document.querySelectorAll('.hotel-supplier-item')
              if (hotel_childs) {
                hotel_childs.forEach(element => {
                  element.remove();
                });

              }

  
              hotel_supplier_list.map((supplier)=>{
                var newli = document.createElement("li");
                newli.className="hotel-supplier-item";
                newli.setAttribute('id',supplier['id']);
                newli.textContent = supplier['name'];
                newli.setAttribute('role', 'option') ;
                newli.setAttribute('tabindex', "-1") ;
                parent_hotel.append(newli);
              })

  
            }
  
            hsToggleList('Open')
            setState('opened')
            break
    
          case 'Escape':
            // if state = initial, do nothing
            // if state = opened or filtered, set state to initial
            // if state = closed, do nothing
            if (hsState === 'opened' || hsState === 'filtered') {
              hsToggleList('Shut')
              setState('initial')
            }
            break
          default:
            if (hsState === 'initial') {
              // if state = initial, toggle open, hsDoFilter and set state to filtered
              hsToggleList('Open')
              hsDoFilter()
              setState('filtered')
            } else if (hsState === 'opened') {
              // if state = opened, hsDoFilter and set state to filtered
              hsDoFilter()
              setState('filtered')
            } else if (hsState === 'closed') {
              // if state = closed, hsDoFilter and set state to filtered
              hsDoFilter()
              setState('filtered')
            } else { // already filtered
              hsDoFilter()
            }
            break 
        }
      }
  
  })
  
// Gestion des écènements pour le choix du fournisseur de taxi
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
    // /////////////////////////////////
  
    function tsToggleList(whichWay) {
      console.log("whichway : ", whichWay);
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
      
      // update aria-selected, if using
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
            taxi_supplier_list.push({'id':'','name':inputsupplier});
            var taxi_suplier = document.getElementById("taxi-supplier-list")
            var taxi_childs = document.querySelectorAll(".taxi-supplier-item")
            if (taxi_childs) {
              taxi_childs.forEach(element => {
                element.remove();
              });

            }

            taxi_supplier_list.map((taxi_supp)=>{
              var newli = document.createElement("li");
              newli.className="taxi-supplier-item";
              newli.setAttribute('data-id',taxi_supp['id']);
              newli.textContent = taxi_supp['name'];
              newli.setAttribute('role', 'option') ;
              newli.setAttribute('tabindex', "-1") ;
              taxi_suplier.append(newli);
            })
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

})



// Enregistrer la reservation d'hôtel
$('#ConfirmAddHotel').on('click', function(){
  var name = document.getElementById('hotel-supplier-input').value;
  var arrivalDate = document.getElementById('arrivalDate').value;
  var arrivalTime = document.getElementById('arrivalTime').value;
  var departureDate = document.getElementById('departureDate').value;
  var departureTime = document.getElementById('departureTime').value;
  var room = document.getElementById('room').value;
  var adults = document.getElementById('adults').value;
  var kids = document.getElementById('kids').value;
  var pnr_id = document.getElementById('pnr_id').getAttribute('data-id');

 // Enregistrer le fournisseur s'il est nouveau 
  hotel_input = document.getElementById('hotel-supplier-input')
  data_id = hotel_input.getAttribute('data-id');
  if (data_id == "null") {
    addServiceSupplier(name,10);
  }
  
  // Enregistrer toutes les informations dans sessionStorage
  hotel_info = {'name':name,'arrivalDate':arrivalDate,'arrivalTime':arrivalTime,'departureDate':departureDate,'departureTime':departureTime,'room':room,'adults':adults,'kids':kids};
  sessionStorage.setItem('hotel_info',JSON.stringify(hotel_info));

  toastr.success('Informations ajoutées.')


})

// Enregistrer la reservation de taxi
$('#ConfirmAddTaxi').on('click', function(){ 
  var name = document.getElementById('taxi-supplier-input').value;
  var taxiDate = document.getElementById('taxiDate').value;
  var taxiTime = document.getElementById('taxiTime').value;
  var passagers = document.getElementById('passagers').value;
  var location = document.getElementById('location').value;
  var pnr_id = document.getElementById('pnr_id').getAttribute('data-id');

 // Enregistrer le fournisseur s'il est nouveau 
  taxi_input = document.getElementById('taxi-supplier-input')
  data_id = taxi_input.getAttribute('data-id');
  if (data_id == "null") {
    addServiceSupplier(name,12);
  }
  // Enregistrer toutes les informations dans sessionStorage

  taxi_details = {'name':name,'date':taxiDate,'heure':taxiTime,'passagers':passagers,'depart':location};
  sessionStorage.setItem('taxi_details',JSON.stringify(taxi_details));

  toastr.success('Informations ajoutées.')

})

// Ajouter un fournisseur 
function addServiceSupplier(supplier_name, service_id){
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