

const liElements = $(".filter-menu > .list");
const $pnrMenu = $(".pnr-menu");
const $wrapperMenuFilter = $(".wrapper-menu-filter");

$wrapperMenuFilter.hide();
$pnrMenu.hide();

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
      // Show all input
        user_email_update.hidden = false;
        user_first_name_update.hidden = false;
        user_name_update.hidden = false;
        user_role_update.hidden = false;
      
      // Hide all informations 
        user_email_label.hidden = true;
        user_first_name_label.hidden = true;
        user_name_label.hidden = true;
        user_role_label.hidden = true;
      
      // put the previous information as the value of the respective input
        user_email_update.value = user_email_label.innerText;
        user_name_update.value = user_name_label.innerText;
        user_first_name_update.value = user_first_name_label.innerText;
        user_role_update.value = user_role_label.innerText;

      // Hide Update Password Button 
        UpdatePwdButton.hidden = true;
      // Show Cancel Update button 
        Cancel_update_info.hidden = false;
      // Hide the update info button
        update_info.hidden = true;
      // Show the confirm update info button
        confirm_update_info.hidden = false;

    })

    $('#Cancel_update_info').click(function(){
      // hide all input
        user_email_update.hidden = true;
        user_first_name_update.hidden = true;
        user_name_update.hidden = true;
        user_role_update.hidden = true;

      // show all informations
        user_email_label.hidden = false;
        user_first_name_label.hidden = false;
        user_name_label.hidden = false;
        user_role_label.hidden = false;

      // show Update Password buttton
        UpdatePwdButton.hidden = false;
      // hide update cancel button
        Cancel_update_info.hidden = true;
      
      // show Update informations button 
        update_info.hidden = false;
      // hide Confirm update info button  
        confirm_update_info.hidden = true;

    })

    $('#archive_user').click(function(){
      // Pass all the data to the modal
        $('#user_name').text('archiver '+$(this).data('user-name') +' '+ $(this).data('user-first-name'));
        $('#action').val($(this).data('action'));
        $('#connected_user').val($(this).data('connected-user'));
        $('#user').val($(this).data('user'));

      // Set the modal title
        var modalTitle = document.querySelector('#modalTitle');
        modalTitle.innerText = "Archiver un utilisateur";
        
    })

    $('#reactive_user').click(function(){
      // Pass all the data to the modal
      $('#user_name').text('réactiver '+$(this).data('user-name') +' '+ $(this).data('user-first-name'));
      $('#action').val($(this).data('action'));
      $('#connected_user').val($(this).data('connected-user'));
      $('#user').val($(this).data('user'));

      // Set the modal title 
      var modalTitle = document.querySelector('#modalTitle');
      modalTitle.innerText = "Réactiver un utilisateur";

      // Change the textContent of the confirm button
      var ConfirmButton = document.getElementById('ConfirmArchive');
      ConfirmButton.textContent = 'Réactiver';
      
  })

    $('#confirm_update_info').click(function(){
      // Pass all the data to the modal
        $('#action').val($(this).data('action'));
        $('#connected_user').val($(this).data('connected-user'));
        $('#user').val($(this).data('user'));

    })
    
});

$('#UpdateInfo').click(function () {
  // get all the data from the modal
    var action = $('#action').val();
    var password = $('#password').val();
    var user = $('#user').val(); 
    var connected_user = $('#connected_user').val();

    // Archive an user
    if (action == "archive") {
        $.ajax({
            type: "POST",
            url: "/user/archive",
            dataType: "json",
            data: {
              password: password,
              user: user,
              connected_user: connected_user,

              csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
              if (data.status == 200) {
                toastr.success(data.message)
                location.reload();
              }
              else{
                toastr.error(data.message)
              }
             
            }
          });
      
    }

    // Reactive an user
    if (action == "reactive") {  
        $.ajax({
            type: "POST",
            url: "/user/reactive",
            dataType: "json",
            data: {
              password: password,
              user: user,
              connected_user: connected_user,

              csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
              if (data.status == 200) {
                toastr.success(data.message)
                location.reload();
              }
              else{
                toastr.error(data.message)
              }
             
            }
          });
      
    }

    // Update all info
    if (action == "update_info") {
      var name = $('#user_name_update').val();
      var first_name = $('#user_first_name_update').val();
      var email = $('#user_email_update').val();
      var role = $('#customer-type-int-input').val();
      
      var action = $('#action').val();
      var password = $('#password').val();
      var user = $('#user').val(); 
      var connected_user = $('#connected_user').val();

      $.ajax({
        type: 'POST',
        url: '/user/updateInfo',
        dataType: "json",
        data : {
          name : name,
          first_name : first_name,
          email : email,
          role : role,
          password : password,
          user : user,
          connected_user : connected_user,
          csrfmiddlewaretoken : csrftoken,
        },
        success : function(data){
          if(data.status == 200){
            toastr.success(data.message);
            location.reload();
          }
          else{
            toastr.error(data.message);
          }
        }
      });
    }

    if (action == "update_password") {
      var currentPassword = $('#current-password').val();
      var newPassword = $('#new-password').val();
      var user_id = $('#user_id').val();

      $.ajax({
        type: "POST",
        url: "/user/UpdatePassword",
        dataType: "json",
        data: {
          currentPassword: currentPassword,
          newPassword : newPassword,
          user_id: user_id,
          csrfmiddlewaretoken: csrftoken,
        },
        success: function(data){
          if(data.status == 200){
            toastr.success(data.message);
            location.reload();
          }
          else{
            toastr.error(data.message);
          }
        }
      })
    }
})

// Update Password

$('#ConfirmNewPassword').click(function(){
  // Pass all the data to the modal
    $('#action').val($(this).data('action'));
    $('#connected_user').val($(this).data('connected-user'));
    $('#user').val($(this).data('user'));

});

$(document).ready(function () {

  $("#user-research").on("click", function () {
    SearchUser();
  });

  $('#NoFilter').on("click", function() {
    

    liElements.removeClass("active");
    $pnrMenu.hide();
    $wrapperMenuFilter.hide();
    $("#all-user").show();
    $("#all-user-after-search").remove();
  })
});

function closeFilter(){
    $pnrMenu.hide();
    $wrapperMenuFilter.hide();
}
// Search function for user list

function SearchUser() {
  
  var user_research = $("#input-user").val().toLowerCase();
  if (user_research.trim() != "") {
    $("#spinnerLoadingSearch").show();
    $.ajax({
      type: "POST",
      url: "/home/user-research",
      dataType: "json",
      data: {
        user_research: user_research,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (data) {
        let SEARCH_RESULT = data.results;

        if (SEARCH_RESULT.length > 0) {
          document.querySelector("#all-user-after-search").innerHTML = "";

          $("#all-user-after-search").show();
          $("#initialPagination").hide();
          $("#spinnerLoadingSearch").hide();

          let pnrAfterSearch = SEARCH_RESULT.map((invoice, index) => {
            return { id: invoice.pnr_id, position: index, number: invoice.pnr_number };
          });
          

          localStorage.setItem(
            "userAfterSearch",
            JSON.stringify(pnrAfterSearch)
          );

          // $("tbody.tbody-unordered-pnr").remove();
          $("#all-user").remove();
          $("#all-user-after-search").show();


          var html = `<thead class="bg-info">
                <tr>
                  <th>Nom</th>
                  <th>Prénom(s)</th>
                  <th>Nom d'utilisateur</th>
                  <th>Email</th>
                  <th>Rôle</th>
                </tr>
              </thead>
              <tbody class="tbody-user-after-search">`;
              SEARCH_RESULT.forEach(user => {
                html += `
                <tr 
                  onclick="location.href='/user/details/${user.id}/'" 
                  style="cursor: pointer;" 
                  role="row"
                >
                  <td> 
                    ${user.name}  
                  </td>             
                  <td> ${user.first_name} </td>
                  <td> ${user.username} </td>

                  <td> ${user.email} </td>
                  <td> ${user.role} </td>
                  
                </tr>`;
              }); 

          html += `</tbody>`;
          $("all-user-after-search").html(html); // Mise à jour du contenu de la table
          $("#all-user-after-search").html(html).trigger("update");
              
        } else {
          $("#spinnerLoadingSearch").hide();
          const input__searchPnrValue = $("#input-user").val();
          $("#input-user").val("");
          toastr.error(
            `Aucun utilisateur ne correspondant à la recherche ~ ${input__searchPnrValue} ~`
          );
        }
      },
    });
  } else {
    $("#spinnerLoadingSearch").hide();
    toastr.warning(`La recherche ne doit pas être vide`);
  }
}

function ShowUserByType(role_id){
  console.log('filtre');
  console.log('role_id : ',role_id);
    // $("#spinnerLoadingSearch").show();
    $.ajax({
      type: "POST",
      url: "/home/user-filter",
      dataType: "json",
      data: {
        role_id: role_id,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (data) {
        let SEARCH_RESULT = data.results;

        if (SEARCH_RESULT.length > 0) {
          document.querySelector("#all-user-after-search").innerHTML = "";

          $("#all-user-after-search").show();
          $("#initialPagination").hide();
          $("#spinnerLoadingSearch").hide();

          let pnrAfterSearch = SEARCH_RESULT.map((invoice, index) => {
            return { id: invoice.pnr_id, position: index, number: invoice.pnr_number };
          });
          

          localStorage.setItem(
            "userAfterSearch",
            JSON.stringify(pnrAfterSearch)
          );

          // $("tbody.tbody-unordered-pnr").remove();
          $("#all-user").hide();
          $("#all-user-after-search").show();

          var html = `<thead class="bg-info">
                <tr>
                  <th>Nom</th>
                  <th>Prénom(s)</th>
                  <th>Nom d'utilisateur</th>
                  <th>Email</th>
                  <th>Rôle</th>
                </tr>
              </thead>
              <tbody class="tbody-user-after-search">`;
              SEARCH_RESULT.forEach(user => {
                html += `
                <tr 
                  onclick="location.href='/user/details/${user.id}/'" 
                  style="cursor: pointer;" 
                  role="row"
                >
                  <td> 
                    ${user.name}  
                  </td>             
                  <td> ${user.first_name} </td>
                  <td> ${user.username} </td>

                  <td> ${user.email} </td>
                  <td> ${user.role} </td>
                  
                </tr>`;
              }); 

          html += `</tbody>`;
          $("all-user-after-search").html(html); // Mise à jour du contenu de la table
          $("#all-user-after-search").html(html).trigger("update");

        } else {
          // $("#spinnerLoadingSearch").hide();
          toastr.error(
            `Aucun utilisateur ne correspondant à la recherche `
          );
        }
        closeFilter();
      },
    });
}

