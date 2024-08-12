
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

      updateSelectOptions();
      
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

  const motif_list = [];

function updateSelectOptions() {
    const parent_motif = document.getElementById("ticket-motif-list")
                        
    const child = document.getElementById("ticket_child");
        if (child) {
            parent.removeChild(child);
        }

    const motif_child = document.getElementById("ticket-motif-item")
      if (motif_child) {
        parent_motif.removeChild(motif_child);
      }

        document.getElementById("ticket-motif-list").innerHTML = "";
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            
            if (this.readyState == 4 && this.status == 200) {
                                        
            var response = JSON.parse(this.responseText);
 
            const motifs = Array.from(response.motifs);
            parent_motif.innerHTML = '';

            motifs.map((motif) =>{
                motif_list.push(motif);
                const newli = document.createElement("li");
                newli.className="ticket-motif-item";
                newli.setAttribute("data-value", motif.id);
                newli.textContent = motif.motif;
                newli.setAttribute('role', 'option') ;
                newli.setAttribute('tabindex', "-1") ;
                parent_motif.append(newli);
            });


            }
        };
        xmlhttp.open("GET", '/home/motif/get-all', true);
        xmlhttp.send();

}


$(document).ready(function(){
  // SETUP
  // /////////////////////////////////
  // assign names to things we'll need to use more than once
  const csSelector = document.querySelector('#TicketMotifSelect'); // the input, svg and ul as a group
  const csInput = csSelector.querySelector('input');
  const csList = csSelector.querySelector('ul');
  const csIcons = csSelector.querySelector('svg');
  const csStatus = document.querySelector('#ticket-motif-status');

  // when JS is loaded, set up our starting point
  // if JS fails to load, the custom select remains a plain text input
  // create and set start point for the state tracker
  let csState = "initial";
  // inform assistive tech (screen readers) of the names & roles of the elements in our group
  csSelector.setAttribute('role', 'combobox') ;
  csSelector.setAttribute('aria-haspopup', 'listbox') ;
  csSelector.setAttribute('aria-owns', 'ticket-motif-list') ;// container owns the list...
  csInput.setAttribute('aria-autocomplete', 'both') ;
  csInput.setAttribute('aria-controls', 'ticket-motif-list') ;// ...but the input controls it
  csList.setAttribute('role', 'listbox') ;


  // EVENTS
  // /////////////////////////////////
  csSelector.addEventListener('click', function(e) {
    const currentFocus = findFocus()
    switch(csState) {
      case 'initial' : // if state = initial, toggleOpen and set state to opened
        toggleList('Open')
        setState('opened')
        break
      case 'opened':
        // if state = opened and focus on input, toggleShut and set state to initial
        if (currentFocus === csInput) {
          toggleList('Shut')
          setState('initial')
        } else if (currentFocus.tagName === 'LI') {
          // if state = opened and focus on list, makeChoice, toggleShut and set state to closed
          makeChoice(currentFocus)
          toggleList('Shut')
          setState('closed')
        }
        break
      case 'filtered':
        // if state = filtered and focus on list, makeChoice and set state to closed
        if (currentFocus.tagName === 'LI') {
          makeChoice(currentFocus)
          toggleList('Shut')
          setState('closed')
        } // if state = filtered and focus on input, do nothing (wait for next user input)

        break
      case 'closed': // if state = closed, toggleOpen and set state to filtered? or opened?
        toggleList('Open')
        setState('filtered')
        break
    }
  })

  csSelector.addEventListener('keyup', function(e) {
    doKeyAction(e.key)
  })

  document.addEventListener('click', function(e) {
    if (!e.target.closest('#TicketMotifSelect')) {
      // click outside of the custom group
      toggleList('Shut')
      setState('initial')
    } 
  })
  
    // FUNCTIONS 
    // /////////////////////////////////
  
    function toggleList(whichWay) {
      if (whichWay === 'Open') {
        csList.classList.remove('hidden-all')
        csSelector.setAttribute('aria-expanded', 'true')
      } else { // === 'Shut'
        csList.classList.add('hidden-all')
        csSelector.setAttribute('aria-expanded', 'false')
      }
    }
  
    function findFocus() {
      const focusPoint = document.activeElement
      return focusPoint
    }
  
    function moveFocus(fromHere, toThere) {
      var csOptions = document.querySelectorAll('.ticket-motif-item');
      var aOptions = Array.from(csOptions);
      // grab the currently showing options, which might have been filtered
      const aCurrentOptions = aOptions.filter(function(option) {
        if (option.style.display === '') {
          return true
        }
      })
      // don't move if all options have been filtered out
      if (aCurrentOptions.length === 0) {
        return
      }
      if (toThere === 'input') {
        csInput.focus()
      }
      // possible start points
      switch(fromHere) {
        case csInput:
          if (toThere === 'forward') {
            aCurrentOptions[0].focus()
          } else if (toThere === 'back') {
            aCurrentOptions[aCurrentOptions.length - 1].focus()
          }
          break
        case csOptions[0]: 
          if (toThere === 'forward') {
            aCurrentOptions[1].focus()
          } else if (toThere === 'back') {
            csInput.focus()
          }
          break
        case csOptions[csOptions.length - 1]:
          if (toThere === 'forward') {
            aCurrentOptions[0].focus()
          } else if (toThere === 'back') {
            aCurrentOptions[aCurrentOptions.length - 2].focus()
          }
          break
        default: // middle list or filtered items 
          const currentItem = findFocus()
          const whichOne = aCurrentOptions.indexOf(currentItem)
          if (toThere === 'forward') {
            const nextOne = aCurrentOptions[whichOne + 1]
            nextOne.focus()
          } else if (toThere === 'back' && whichOne > 0) {
            const previousOne = aCurrentOptions[whichOne - 1]
            previousOne.focus()
          } else { // if whichOne = 0
            csInput.focus()
          }
          break
      }
    }
  
    function doFilter() {
  
      const terms = csInput.value
      var csOptions = document.querySelectorAll('.ticket-motif-item');
      var aOptions = Array.from(csOptions);
  
      const aFilteredOptions = aOptions.filter(function(option) {
        if (option.innerText.toUpperCase().startsWith(terms.toUpperCase())) {
          return true
        }
      })
      csOptions.forEach(option => option.style.display = "none")
      aFilteredOptions.forEach(function(option) {
        option.style.display = ""
      })
      setState('filtered')
      updateStatus(aFilteredOptions.length)
    }
  
    function updateStatus(howMany) {
      csStatus.textContent = howMany + " options available."
    }
  
    function makeChoice(whichOption) {
      csInput.setAttribute('data-id', whichOption.getAttribute('data-value'));
      csInput.setAttribute('value',whichOption.textContent);
      moveFocus(document.activeElement, 'input')
      VerifMotifValue();
      setState('closed');
      
      // update aria-selected, if using
    }
  
    function setState(newState) {
      switch (newState) {
        case 'initial': 
          csState = 'initial'
          break
        case 'opened': 
          csState = 'opened'
          break
        case 'filtered':
          csState = 'filtered'
          break
        case 'closed': 
          csState = 'closed'
      }
      // console.log({csState})
    }
  
    function doKeyAction(whichKey) {
      const currentFocus = findFocus()

      switch(whichKey) {
        case 'Enter':
          var inputMotif = $("#ticket-motif-input").val();
          if (inputMotif.trim() !== '') {
            motif_list.push({'id':'','motif':inputMotif});
            var parent_motif = document.getElementById("ticket-motif-list")
            var motif_child = document.getElementById("ticket-motif-item")
            if (motif_child) {
              parent_motif.removeChild(motif_child);
            }

            motif_list.map((motif)=>{
              var newli = document.createElement("li");
              newli.className="ticket-motif-item";
              newli.setAttribute('id',motif['id']);
              newli.textContent = motif['motif'];
              newli.setAttribute('role', 'option') ;
              newli.setAttribute('tabindex', "-1") ;
              parent_motif.append(newli);
            })

          }

          toggleList('Open')
          setState('opened')
          break
  
        case 'Escape':
          // if state = initial, do nothing
          // if state = opened or filtered, set state to initial
          // if state = closed, do nothing
          if (csState === 'opened' || csState === 'filtered') {
            toggleList('Shut')
            setState('initial')
          }
          break
        default:
          if (csState === 'initial') {
            // if state = initial, toggle open, doFilter and set state to filtered
            toggleList('Open')
            doFilter()
            setState('filtered')
          } else if (csState === 'opened') {
            // if state = opened, doFilter and set state to filtered
            doFilter()
            setState('filtered')
          } else if (csState === 'closed') {
            // if state = closed, doFilter and set state to filtered
            doFilter()
            setState('filtered')
          } else { // already filtered
            doFilter()
          }
          break 
      }
    }

})

