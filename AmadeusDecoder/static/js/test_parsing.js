// Test Parssage ---------------------------------------
$(document).ready(function () {
    const fileTestButton = document.getElementById('fileTestButton');

    // Verify if we should show the textarea or the input file
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

    // Upload file
    $(document).on('click', '#fileUploadButton', function() {
        const fileInput = $('#fileInput')[0];  
        const file = fileInput.files[0];
        
        // Create a FormData object and append the file and CSRF token
        const formData = new FormData();
        formData.append('file', file);
        formData.append('csrfmiddlewaretoken', csrftoken);

        $.ajax({
            type: "POST",
            url: "/setting/test-parsing-upload-file",
            data: formData,
            contentType: false,  // Set content type to false for FormData
            processData: false,  // Prevent jQuery from processing the data
            success: function (data) {
                
                if (data.status == 200) {

                    toastr.success('File uploaded');
                    //Show the image of the uploaded PDF
                    var container_image = document.getElementById('pdf_image');
                    container_image.style.height='400px';
                    container_image.style.overflow = 'auto';
                    container_image.style.margin = '20px 0 20px 0';
                    var imagesData = JSON.parse(data.pdf_image);

                    imagesData.forEach(function(image) {
                        var pdf_image = document.createElement('img');
                        pdf_image.src = 'data:image/jpeg;base64,' + image;
                        pdf_image.style.imageRendering = 'pixelated'; // Utiliser l'interpolation de pixel pour éviter le flou
                        pdf_image.style.filter = 'brightness(1) contrast(1)';
                        pdf_image.style.width = '70%'; 
                        pdf_image.style.height = 'auto';
                        container_image.appendChild(pdf_image);
                    });

                    fileTestButton.hidden = false;
                } else {
                    toastr.error('File Not uploaded');
                }
            }
        });
    });

    // Test PNR, TKT, TST (ALTEA)
    $(document).on('click', '#TestTextButton', function() {
        var data = $('#data').val();
        var newTestButton = document.getElementById('NewTest');
        $.ajax({
            type: "POST",
            url: "/setting/test-parsing-text",
            dataType: "json",
            data: {
                data: data,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                if (data.status == 200) {
                    toastr.success('Test Done');
                    // Show the content of what had been tested
                    var test_container = document.getElementById('text_content');
                    test_container.style.overflow = 'auto';
                    test_container.style.height = '400px';
                    test_container.style.margin = '20px 0 20px 0';

                    var divContent = document.createElement('textarea');
                    divContent.textContent = data.content;
                    divContent.style.width = '600px';
                    divContent.style.height = '400px';
                    divContent.style.padding = '20px';

                    test_container.appendChild(divContent);

                    newTestButton.hidden = false;

                } else {
                    error_console.hidden = false;
                    
                    // Show error
                    var error_list = data.error.split(',');
                    error_list.forEach(error => {
                        var paragraphe = document.createElement('p');
                        paragraphe.textContent = error;
                        error_console.appendChild(paragraphe);
                    });

                    newTestButton.hidden = false;
                        
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });

    });

    // reload page
    $(document).on('click','#NewTest', function() {
        location.reload();
    });
});

$(document).ready(function () {
    const error_console = document.getElementById('console');

    // TEST ZENITH
    $(document).on('click', '#fileTestButton', function() {
        const fileInput = $('#fileInput')[0];  
        const file = fileInput.files[0];
        $.ajax({
            type: "POST",
            url: "/setting/test-parsing-zenith",
            dataType: "json",
            data: {
                uploaded_file_name: file.name,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {  

                if (data.status == 200) {
                    toastr.success('File uploaded');
                } else {
                    //Show the traceback error on the div console in the page
                    error_console.hidden = false;
                    
                    var error_list = data.error.split(',');
                    error_list.forEach(error => {
                        var paragraphe = document.createElement('p');
                        paragraphe.textContent = error;
                        error_console.appendChild(paragraphe);
                    });
                    
                }
            }
        });
    });
});
