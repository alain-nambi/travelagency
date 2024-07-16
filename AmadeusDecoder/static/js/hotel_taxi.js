
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
        toggleList('Shut')
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
        updateStatus(hsFilteredOptions.length)
      }
    
      function updateStatus(howMany) {
        csStatus.textContent = howMany + " options available."
      }
    
      function makeChoice(whichOption) {
        hsInput.setAttribute('data-id', whichOption.getAttribute('data-value'));
        hsInput.setAttribute('value',whichOption.textContent);
        hsMoveFocus(document.activeElement, 'input')
        VerifMotifValue();
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
              motif_list.push({'id':'','motif':inputsupplier});
              var parent_motif = document.getElementById("hotel-supplier-list")
              var motif_child = document.getElementById("hotel-supplier-item")
              if (motif_child) {
                parent_motif.removeChild(motif_child);
              }
  
              motif_list.map((motif)=>{
                var newli = document.createElement("li");
                newli.className="hotel-supplier-item";
                newli.setAttribute('id',motif['id']);
                newli.textContent = motif['motif'];
                newli.setAttribute('role', 'option') ;
                newli.setAttribute('tabindex', "-1") ;
                parent_motif.append(newli);
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
  
  