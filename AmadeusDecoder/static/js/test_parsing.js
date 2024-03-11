// Test Parssage ---------------------------------------
$(document).ready(function () {
    $(document).on('change', '#SelectTypeParsing', function () {
        if ($(this).val() == 'rd' || $(this).val() == 'ewa' ) {
            document.getElementById('input_file').hidden = false;
            document.getElementById('textarea').hidden = true;

        }
        else{
            document.getElementById('input_file').hidden = true;
            document.getElementById('textarea').hidden = false;

        }
    });

    $(document).on('click', '#fileUploadButton', function() {
        var type = $('#SelectTypeParsing').val();
        const fileInput = $('#fileInput')[0];  
        const file = fileInput.files[0];


        // Create a FormData object and append the file and CSRF token
        const formData = new FormData();
        formData.append('file', file);
        formData.append('csrfmiddlewaretoken', csrftoken);

        if (type == "ewa") {
            $.ajax({
                type: "POST",
                url: "/setting/test-parsing-zenith",
                data: formData,
                contentType: false,  // Set content type to false for FormData
                processData: false,  // Prevent jQuery from processing the data
                success: function (data) {
                    if (data.status == 200) {
                        toastr.success('File uploaded');
                        location.reload();
                    } else {
                        toastr.error('coucou',data.error);
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        }
        if (type == "rd") {
            $.ajax({
                type: "POST",
                url: "/setting/test-parsing-zenith-receipt",
                data: formData,
                contentType: false,  // Set content type to false for FormData
                processData: false,  // Prevent jQuery from processing the data
                success: function (data) {
                    if (data.status == 200) {
                        toastr.success('File uploaded');
                        location.reload();
                    } else {
                        toastr.error('coucou',data.error);
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        }
    });
});