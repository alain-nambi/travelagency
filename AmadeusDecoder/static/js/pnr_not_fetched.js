                                                                                                                     
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

function updatePnrStatus(pnrNumbers) {
    if (!Array.isArray(pnrNumbers)) return;
    pnrNumbers.forEach(pnrNum => {
        const row = document.querySelector(`tr[data-pnr="${pnrNum}"]`);
        if (row) {
            const statusCell = row.querySelector('td:last-child');
            if (statusCell) {
                statusCell.innerHTML = '<button class="btn btn-success py-0">Remonté</button>';
                row.classList.add('table-success');
            }
        }
    });
}

let lastCheck = localStorage.getItem('lastPnrCheck') || new Date(Date.now() - 60000).toISOString();

function pollForUpdates(){
    fetch(`/ajax/updated-pnrs/?since=${encodeURIComponent(lastCheck)}`)
        .then(r => r.json())
        .then(data => {
            if(data.updated_pnrs?.length){
                updatePnrStatus(data.updated_pnrs);
            }
            lastCheck = new Date().toISOString();
            localStorage.setItem('lastPnrCheck', lastCheck);
        });
}

// Démarrer le polling
setInterval(pollForUpdates, 10000);
pollForUpdates();