const commentField = document.getElementById('comment');
const pnrId = window.location.pathname.split('/').reverse()[1];
const commentStateUpdateButton = document.getElementById('comment-state');

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };
  
const csrftoken = getCookie("csrftoken");

/*
    Ajax function to send data from 'comment' field to database
*/
$('#send-comment').on('click',function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/comment/',
        dataType: 'json',
        data: {
            comment: commentField.value.trim(),
            pnr_id: pnrId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (response) => {
            console.log(response.comment);
            toastr.success('Votre constat été envoyé avec succès');
        },
        error: (response) => {
            console.log(response)
        }
    });
    $("#comment-form").get(0).reset();
    $('.pnr-signal').removeClass("open");
})

const updateState = (event, commentId)=> {
    $.ajax({
        type: 'POST',
        url: 'update-comment-state/',
        dataType: 'json',
        data: {
            comment_id: commentId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (response) =>{
            console.log(response.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
        },
        error: (response) =>{
            console.log(response);
        }
    });
};

const updateStateDetail = (event, commentId)=> {
    $.ajax({
        type: 'POST',
        url: 'update-comment-state/',
        dataType: 'json',
        data: {
            comment_id: commentId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (response) =>{
            console.log(response.comment);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Traitée';
        },
        error: (response) =>{
            console.log(response);
        }
    });
};


// Sélection des éléments DOM
const showOtherCommandsMenu = document.getElementById("showOtherCommandsMenu");
const otherCommandsMenu = document.querySelector(".other-commands-menu");
const fixedHeaderCard = document.querySelector(".fixed-header")
const stickyTrTable = document.querySelector(".sticky-tr-table")
const pnrManagementMenuTrigger = document.querySelector("#pnrManagementMenu")

if (showOtherCommandsMenu) {
    // Fonction pour mettre à jour le style des éléments
    function updateElementStyles(isShown) {
        if (!isShown) {
            fixedHeaderCard.style = "top: 3.4rem !important";
            stickyTrTable.style = "top: 6.4rem !important";
            pnrManagementMenuTrigger.style = "margin-top: 1rem !important; visibility: visible";
        } else {
            fixedHeaderCard.style.removeProperty("top");
            stickyTrTable.style.removeProperty("top");
            pnrManagementMenuTrigger.style.removeProperty("margin-top");
        }
    }


    // Initialisation du statut du menu depuis le localStorage
    let isCommandMenuShown = JSON.parse(localStorage.getItem("isCommandMenuShown")) || false;

    if (!isCommandMenuShown) {
        otherCommandsMenu.classList.add('d-none');
        otherCommandsMenu.classList.remove('d-block');
    }

    if (fixedHeaderCard && stickyTrTable && pnrManagementMenuTrigger) {
        updateElementStyles(isCommandMenuShown)
    }
    
    const buttonText = isCommandMenuShown ? 'Minimiser les commandes' : 'Afficher autres commandes';
    showOtherCommandsMenu.textContent = buttonText;

    // Fonction pour basculer l'affichage du menu
    function toggleCommandMenu() {
        isCommandMenuShown = !isCommandMenuShown;

        // Enregistrement de l'état actuel du menu dans le localStorage
        localStorage.setItem("isCommandMenuShown", isCommandMenuShown);

        const buttonText = isCommandMenuShown ? 'Minimiser les commandes' : 'Afficher autres commandes';
        const displayClass = isCommandMenuShown ? 'd-block' : 'd-none';
        
        // Mise à jour du texte du bouton et de la classe d'affichage du menu
        showOtherCommandsMenu.textContent = buttonText;
        otherCommandsMenu.classList.remove('d-none', 'd-block');
        otherCommandsMenu.classList.add(displayClass);
    }

    // Ajout de l'événement click sur le bouton showOtherCommandsMenu
    showOtherCommandsMenu.addEventListener("click", (event) => {
        event.preventDefault();
        toggleCommandMenu();

        if (fixedHeaderCard && stickyTrTable && pnrManagementMenuTrigger) {
            // Mise à jour du style des éléments
            updateElementStyles(isCommandMenuShown)
        }
    });
}



