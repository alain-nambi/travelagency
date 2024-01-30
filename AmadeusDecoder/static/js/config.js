
function tabClicked(tabId) {
    const activeTab = document.querySelector('.nav-item .active');
    const activePanel = document.querySelector('.tab-content.general .tab-pane.active');
    
    if (activeTab) {
        console.log("Salut");
        console.log('active ta:', activeTab.id);
        activeTab.classList.remove('active');
    }

    if (activePanel) {
        activePanel.classList.remove('active','show');
        console.log('active pa:',activePanel.id);
    }

    // Activez l'onglet et le panneau correspondants
    const newTab = document.getElementById(tabId);
    const newPanel = document.getElementById(`${tabId}-panel`);
    console.log('newPanel :',newPanel.id);
    console.log(newPanel);
    if (newTab && newPanel) {
        newTab.classList.add('active');
        newPanel.classList.add('active','show');
    }
}

function InnertabClicked(tabId) {
    const activeTab = document.querySelector('.nav-pills.nav-pills-email .active');
    const activePanel = document.querySelector('.tab-content.content-email .active');
   
    if (activeTab) {
        activeTab.classList.remove('active'); 
    }

    if (activePanel) {
        activePanel.classList.remove('active', 'show');
        activePanel.classList.add('fade');
    }

    // Activez l'onglet et le panneau correspondants
    const newTab = document.getElementById(tabId);
    const newPanel = document.getElementById(`${tabId}-panel`);

    if (newTab && newPanel) {
        console.log('COUCOU--------------------');
        newTab.classList.add('active');
        newPanel.classList.remove('fade');
        newPanel.classList.add('active','show');
    }
}


