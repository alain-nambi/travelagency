const Np = document.getElementById('np');
const Nt = document.getElementById('nt');
const Nlbe = document.getElementById('nlbe');
const Nlse = document.getElementById('nlse');

const ButtonNp = document.getElementById('button-np');
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

