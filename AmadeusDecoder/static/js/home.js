// Function to add appropriate CSS class based on PNR read status
function updatePNRStatus(pnrId, isRead) {
    const trTable = document.querySelector(`#trAllPnr[data-pnr-id="${pnrId}"]`);
    if (!trTable) return; // Exit if element not found

    // Toggle CSS classes based on PNR read status
    trTable.classList.toggle("lue", isRead);
    trTable.classList.toggle("non-lue", !isRead);
}

// Function to check PNR read status
function checkIfPNRHasBeenRead(pnrList) {
    $.ajax({
        type: "POST",
        url: "/home/check-read-pnr/",
        dataType: "json",
        data: {
            pnr_list_to_check: pnrList,
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

// Initial call to check PNR read status
const pnrList = JSON.parse(localStorage.getItem("pnrIds")) || []

checkIfPNRHasBeenRead(pnrList);

// Initialize intervalID variable
let intervalID;

// Function to start checking PNR read status periodically
function startChecking(time) {
    // Set interval to check PNR read status
    intervalID = setInterval(() => {
        checkIfPNRHasBeenRead(pnrList);
    }, time);
}

// Function to stop checking PNR read status
function stopChecking() {
    clearInterval(intervalID);
}

// Check if URL is on "/home/" before executing the code
if (window.location.pathname === "/home/") {
    // Start checking PNR read status when window is active 
    const time = 10000
    startChecking(time);

    // Stop checking PNR read status when window is inactive
    window.addEventListener('focus', () => startChecking(time));
    window.addEventListener('blur', stopChecking);
}
