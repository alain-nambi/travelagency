const validateFeeModify = document.getElementById('submitFeeModify');


if (validateFeeModify != null) {
    validateFeeModify.addEventListener('click', (e)=> {
        request_id = $('#request_id').val();
        token = $('#request_token').val();
        amount = $('#request_amount').val();
        choice_type = $('#choice_type').val();
    
        if (request_id != "" && token != "" && request_amount != "") {
            window.location.href= `/home/fee-request-accepted/${request_id}/${amount}/${choice_type}/${token}`
        } else {
            toastr.error("Veuillez renseigner les champs.")
        }
    })
}

