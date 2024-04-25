// Function to add appropriate CSS class based on PNR read status
function updatePNRStatus(pnrId, isRead) {
    const trTable = document.querySelector(`#trAllPnr[data-pnr-id="${pnrId}"]`);
    if (!trTable) return; // Exit if element not found

    // Toggle CSS classes based on PNR read status
    trTable.classList.toggle("lue", isRead);
    trTable.classList.toggle("non-lue", !isRead);
}

// Function to check PNR read status
function checkIfPNRHasBeenRead(pnrIdSelected) {
    $.ajax({
        type: "POST",
        url: "/home/check-read-pnr/",
        dataType: "json",
        data: {
            pnr_list_to_check: pnrIdSelected,
            csrfmiddlewaretoken: getCookies("csrftoken"),
        },
        success: (response) => {
            console.log(response);

            // Update CSS classes based on response
            response.PNR.forEach((pnr) => {
                updatePNRStatus(pnr.id, pnr.is_read);
            });
        },
        error: (error) => {
            console.log(error);
        },
    });
}


// Définir une fonction pour lancer le script
function runScript() {
    // Vérifier si l'URL actuelle correspond à "/home/"
    if (window.location.pathname === "/home/") {
        // Lancer le script pour vérifier le statut des PNR
        let intervalID = setInterval(() => { 
            console.log("Navigué vers /home/" + window.location.pathname);
            const pnrIdSelected = JSON.parse(localStorage.getItem("pnrIdSelected"))
            checkIfPNRHasBeenRead(pnrIdSelected);
        }, 1000);

        setTimeout(() => {
            clearInterval(intervalID);
        }, 2000)

        // // Ajouter un écouteur d'événements pour l'événement popstate
        // window.addEventListener('popstate', () => {
        //     // Effacer l'intervalle lors de la navigation loin de "/home/"
        //     clearInterval(intervalID);
        // });
    }
}

// Appeler la fonction pour lancer le script au chargement initial de la page
runScript();

// Appeler à nouveau la fonction si l'utilisateur navigue vers "/home/" à partir d'une autre page
window.addEventListener('popstate', () => {
    runScript();
});
