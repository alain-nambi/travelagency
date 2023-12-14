const Np = document.getElementById('np');
const NpArchived = document.getElementById("npArchived");
const Nt = document.getElementById('nt');
const Nlbe = document.getElementById('nlbe');
const Nlse = document.getElementById('nlse');

const ButtonNp = document.getElementById('button-np');
const ButtonNpArchived = document.getElementById("button-np-archived")
// const ButtonNt = document.getElementById('button-nt');
// const ButtonNlbe = document.getElementById('button-nlbe');
// const ButtonNlse = document.getElementById('button-nlse');

ButtonNp.addEventListener('click', (e) => {
    e.preventDefault();
    // console.log(Np.value.replace(/[^A-Z0-9]/ig, ''));
    const pnr_number = Np.value.replace(/[^A-Z0-9]/ig, '');
    if (pnr_number.length == 6) {
        $.ajax({
            type: 'POST',
            url: '/home/get-pnr-user-copying/',
            dataType: 'json',
            data: {
                DocumentNumber: Np.value,
                csrfmiddlewaretoken: csrftoken,
            },
            success: (response) => {
                console.info("PNR has been copied: " + pnr_number.toUpperCase());
                console.log(response);
            },
            error: (response) => {
                console.log(response);
            }
        })
    }
});

ButtonNpArchived.addEventListener('click', (e) => {
    e.preventDefault();
    const pnr_number = NpArchived.value.replace(/[^A-Z0-9]/ig, '');
    if (pnr_number.length == 6) {
        $.ajax({
            type: 'POST',
            url: '/home/get-pnr-user-copying/',
            dataType: 'json',
            data: {
                DocumentNumber: NpArchived.value,
                csrfmiddlewaretoken: csrftoken,
            },
            success: (response) => {
                console.info("PNR archived has been copied: " + pnr_number.toUpperCase());
                console.log(response);
            },
            error: (response) => {
                console.log(response);
            }
        })
    }
});

// ButtonNt.addEventListener('click', (e) => {
//     e.preventDefault();
//     $.ajax({
//         type: 'POST',
//         url: '/home/get-pnr-user-copying/',
//         dataType: 'json',
//         data: {
//             DocumentNumber: Nt.value,
//             csrfmiddlewaretoken: csrftoken,
//         },
//         success: (response) => {
//             console.log(response);
//         },
//         error: (response) => {
//             console.log(response);
//         }
//     })
// });

// ButtonNlbe.addEventListener('click', (e) => {
//     e.preventDefault();
//     $.ajax({
//         type: 'POST',
//         url: '/home/get-pnr-user-copying/',
//         dataType: 'json',
//         data: {
//             DocumentNumber: Nlbe.value,
//             csrfmiddlewaretoken: csrftoken,
//         },
//         success: (response) => {
//             console.log(response);
//         },
//         error: (response) => {
//             console.log(response);
//         }
//     })
// });

// ButtonNlse.addEventListener('click', (e) => {
//     e.preventDefault();
//     console.log(Np.value);
//     $.ajax({
//         type: 'POST',
//         url: '/home/get-pnr-user-copying/',
//         dataType: 'json',
//         data: {
//             DocumentNumber: Nlse.value,
//             csrfmiddlewaretoken: csrftoken,
//         },
//         success: (response) => {
//             console.log(response);
//         },
//         error: (response) => {
//             console.log(response);
//         }
//     })
// });

