function closeCollapse() {
    $('#collapseExample').collapse('hide');
}

$(document).ready(function(){
    user_name_update = document.getElementById('user_name_update');
    user_first_name_update = document.getElementById('user_first_name_update');
    user_email_update = document.getElementById('user_email_update');
    user_role_update = document.getElementById('user_role_update');

    user_name_label = document.getElementById('user_name_label');
    user_first_name_label = document.getElementById('user_first_name_label');
    user_email_label = document.getElementById('user_email_label');
    user_role_label = document.getElementById('user_role_label');

    UpdatePwdButton = document.getElementById('UpdatePwdButton');
    Cancel_update_info = document.getElementById('Cancel_update_info');

    $('#update_info').click(function(){
        user_email_update.hidden = false;
        user_first_name_update.hidden = false;
        user_name_update.hidden = false;
        user_role_update.hidden = false;

        user_email_label.hidden = true;
        user_first_name_label.hidden = true;
        user_name_label.hidden = true;
        user_role_label.hidden = true;

        user_email_update.value = user_email_label.innerText;
        user_name_update.value = user_name_label.innerText;
        user_first_name_update.value = user_first_name_label.innerText;
        user_role_update.value = user_role_label.innerText;


        UpdatePwdButton.hidden = true;
        Cancel_update_info.hidden = false;
        update_info.hidden = true;
        confirm_update_info.hidden = false;

    })

    $('#Cancel_update_info').click(function(){
        user_email_update.hidden = true;
        user_first_name_update.hidden = true;
        user_name_update.hidden = true;
        user_role_update.hidden = true;

        user_email_label.hidden = false;
        user_first_name_label.hidden = false;
        user_name_label.hidden = false;
        user_role_label.hidden = false;

        UpdatePwdButton.hidden = false;
        Cancel_update_info.hidden = true;
        
        update_info.hidden = false;
        confirm_update_info.hidden = true;

    })

    $('#archive_user').click(function(){
        $('#user_name').text($(this).data('user-name') +' '+ $(this).data('user-first-name'));
        $('#action').val($(this).data('action'));
        $('#connected_user').val($(this).data('connected_user'));
        $('#user').val($(this).data('user'));
    })

    $('#confirm_update_info').click(function(){
        $('#action').val($(this).data('action'));
        $('#connected_user').val($(this).data('connected_user'));
        $('#user').val($(this).data('user'));
    })

    $('#UpdateInfo').click(function(){
        var action = $('#action').val();
        var password = $('#password').val();
        
        if (action == "archive") {
            $.ajax({
                type: "POST",
                url: "/user/archive",
                dataType: "json",
                data: {
                    connected_user : connected_user,
                    user : user,
                    password : password,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function (response) {
                    location.href = response.file_url;
                },
                error: function(error){
                    console.log(error);
                }
            });
        }
    })

    
});