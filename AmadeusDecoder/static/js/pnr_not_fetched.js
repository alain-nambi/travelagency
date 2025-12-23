
document.querySelectorAll('#filter-row input, #filter-row select').forEach(input => {
    input.addEventListener('input', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const column = this.dataset.column;
        const value = this.value.trim();

        if (value) {
            urlParams.set(column, value);
        } else {
            urlParams.delete(column);
        }
        urlParams.set('page', '1'); // réinitialiser la pagination
        window.location.search = urlParams.toString();
    });
});

function clearFilters() {
    // Garde seulement le chemin de base (sans paramètres GET)
    const baseUrl = window.location.pathname;
    window.location.href = baseUrl;
}

const updateNotFetchedState = (event, notFetchedId)=> {
    $.ajax({
        type: 'POST',
        url: '/not-fetched-list/update-state/',
        dataType: 'json',
        data: {
            not_fetched_id: notFetchedId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (response) =>{
            console.log('Update success:', response);
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-success');
            event.target.textContent = 'Remonté';
            
            // Forcer une vérification immédiate
            setTimeout(pollForUpdates, 100);
        },
        error: (response) =>{
            console.log('Update error:', response);
        }
    });
};

// Ouvrir le sidebar
document.getElementById('openPnrHistory').addEventListener('click', function(e){
    e.preventDefault();
    openPnrSidebar();
})

// Fermer le sidebar
document.getElementById('closeRightSidebar').addEventListener('click', function(){
    closePnrSidebar();
})

document.getElementById('rightSidebarOverlay').addEventListener('click', function(){
    closePnrSidebar();
})

// Recherche dans le sidebar
let pnrHistoryData = [];
document.getElementById('searchPnrHistory').addEventListener('input', function(e){
    const searchTerm = e.target.value.toLowerCase()
    filterPnrHistory(searchTerm);
})

function openPnrSidebar(){
    const sidebar = document.getElementById('pnrHistorySidebar');
    const overlay = document.getElementById('rightSidebarOverlay');
    
    if (sidebar && overlay) {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.classList.add('sidebar-open');
        
        // Charger les données
        loadPnrHistory();
    }

}

function closePnrSidebar() {
    const sidebar = document.getElementById('pnrHistorySidebar');
    const overlay = document.getElementById('rightSidebarOverlay');

    if (sidebar && overlay) {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('sidebar-open');
        
        // Réinitialiser la recherche
        const searchInput = document.getElementById('searchPnrHistory');
        if (searchInput) {
        searchInput.value = '';
        }
    }
}

function loadPnrHistory(){
    const sidebarContent = document.getElementById('rightSidebarContent');

    // Afficher le loader
    sidebarContent.innerHTML = `
        <div class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
            <span class="sr-only">Chargement...</span>
        </div>
        </div>
        `;

    // Appel AJAX pour récupérer les PNR de l'utilisateur
    fetch('/not-fetched-list/my-history/')
        .then(response => response.json())
        .then(data => {
            pnrHistoryData = data.pnrs || [];
            displayPnrHistory(pnrHistoryData);
        })
        .catch(error => {
            console.error('Erreur:', error);
            sidebarContent.innerHTML = `
                <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                Erreur lors du chargement des données
                </div>
            `;
        });
}

function displayPnrHistory(pnrs){
    const sidebarContent = document.getElementById('rightSidebarContent');

    if (pnrs.length === 0){
        sidebarContent.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>Aucun PNR signalé</p>
        </div>
        `;
        return;
    }

    let html = '';
    pnrs.forEach(pnr => {
        const statusClass = pnr.status === 0 ? 'remonte' : 'non-remonte';
        const statusText = pnr.status === 0 ? 'Remonté' : 'Non Remonté';

         // Déterminer si on peut cliquer sur tout le bloc
        const isClickable = (pnr.status === 0 && pnr.details_url);
        const tagOpen = isClickable ? `<a href="${pnr.details_url}" class="pnr-item-link">` : `<div>`;
        const tagClose = isClickable ? `</a>` : `</div>`;

        html += `
        ${tagOpen}
            <div class="pnr-item" data-pnr-number="${pnr.pnr_number}">
                <div class="pnr-item-header">
                    <span class="pnr-number">${pnr.pnr_number}</span>
                    <span class="not-fetched-pnr-status ${statusClass}">${statusText}</span>
                </div>
                <div class="pnr-context">${pnr.context || 'Pas de contexte'}</div>
                <div class="pnr-date">
                    <i class="far fa-clock"></i>
                    ${formatDate(pnr.date_creation)}
                </div>
            </div>
        ${tagClose}
        `;
    });

    sidebarContent.innerHTML = html;

}

function filterPnrHistory(searchTerm) {
  if (!searchTerm) {
    displayPnrHistory(pnrHistoryData);
    return;
  }
  
  const filtered = pnrHistoryData.filter(pnr => 
    pnr.pnr_number.toLowerCase().includes(searchTerm) ||
    (pnr.context && pnr.context.toLowerCase().includes(searchTerm))
  );
  
  displayPnrHistory(filtered);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = String(date.getFullYear()).slice(-2);
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  return `${day}/${month}/${year} ${hours}:${minutes}`;
}

// Fermer le sidebar en cliquant n'importe où ailleurs sur la page
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('pnrHistorySidebar');
    const overlay = document.getElementById('rightSidebarOverlay');
    const openButton = document.getElementById('openPnrHistory');

    // Vérifier si le sidebar est ouvert
    if (sidebar && sidebar.classList.contains('active')) {
        // Vérifier si le clic n'est pas sur le sidebar, l'overlay ou le bouton d'ouverture
        if (!sidebar.contains(e.target) && 
            !overlay.contains(e.target) && 
            !openButton.contains(e.target)) {
        closePnrSidebar();
        }
    }
});