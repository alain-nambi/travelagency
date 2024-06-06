
$(document).ready(function(){

    customer_postal_update = document.getElementById('customer_postal_update');
    customer_intitule_update = document.getElementById('customer_intitule_update');
    customer_email_update = document.getElementById('customer_email_update');
    customer_phone_update = document.getElementById('customer_phone_update');
    customer_adress_update = document.getElementById('customer_adress_update');
    customer_adress2_update = document.getElementById('customer_adress2_update');

    customer_departement_update = document.getElementById('customer_departement_update');
    customer_ville_update = document.getElementById('customer_ville_update');
    customer_pays_update = document.getElementById('customer_pays_update');

    customer_postal_label = document.getElementById('customer_postal_label');
    customer_ville_label = document.getElementById('customer_ville_label');
    customer_email_label = document.getElementById('customer_email_label');
    customer_pays_label = document.getElementById('customer_pays_label');
    customer_intitule_label = document.getElementById('customer_intitule_label');
    customer_phone_label = document.getElementById('customer_phone_label');
    customer_adress_label = document.getElementById('customer_adress_label');
    customer_adress2_label = document.getElementById('customer_adress2_label');
    customer_departement_label = document.getElementById('customer_departement_label');

    confirm_customer_update_info = document.getElementById('confirm_customer_update_info');
    Cancel_update_info = document.getElementById('Cancel_customer_update_info');
    customer_update_info = document.getElementById('customer_update_info');

    $('#customer_update_info').click(function(){
      // Show all input
        customer_ville_update.hidden = false;
        customer_departement_update.hidden = false;
        customer_postal_update.hidden = false;
        customer_pays_update.hidden = false;
        customer_email_update.hidden = false;
        customer_intitule_update.hidden = false;
        customer_phone_update.hidden = false;
        customer_adress_update.hidden = false;
        customer_adress2_update.hidden = false;
        
      
      // Hide all informations 
        customer_email_label.hidden = true;
        customer_ville_label.hidden = true;
        customer_postal_label.hidden = true;
        customer_pays_label.hidden = true;
        customer_intitule_label.hidden = true;
        customer_phone_label.hidden = true;
        customer_adress_label.hidden = true;
        customer_adress2_label.hidden = true;
        customer_departement_label.hidden = true;

      
      // put the previous information as the value of the respective input
        customer_ville_update.value = customer_ville_label.innerText;
        customer_postal_update.value = customer_postal_label.innerText;
        customer_departement_update.value = customer_departement_label.innerText;
        customer_pays_update.value = customer_pays_label.innerText;
        customer_intitule_update.value = customer_intitule_label.innerText;
        customer_phone_update.value = customer_phone_label.innerText;
        customer_adress_update.value = customer_adress_label.innerText;
        customer_adress2_update.value = customer_adress2_label.innerText;
        customer_email_update.value = customer_email_label.innerText;

      // Show Cancel Update button 
        Cancel_update_info.hidden = false;
      // Hide the update info button
        customer_update_info.hidden = true;
      // Show the confirm update info button
        confirm_customer_update_info.hidden = false;

    })

    $('#Cancel_customer_update_info').click(function(){
      // hide all input
      customer_ville_update.hidden = true;
      customer_departement_update.hidden = true;
      customer_postal_update.hidden = true;
      customer_pays_update.hidden = true;
      customer_email_update.hidden = true;
      customer_intitule_update.hidden = true;
      customer_phone_update.hidden = true;
      customer_adress_update.hidden = true;
      customer_adress2_update.hidden = true;
      // show all informations
      customer_email_label.hidden = false;
      customer_ville_label.hidden = false;
      customer_postal_label.hidden = false;
      customer_pays_label.hidden = false;
      customer_intitule_label.hidden = false;
      customer_phone_label.hidden = false;
      customer_adress_label.hidden = false;
      customer_adress2_label.hidden = false;
      customer_departement_label.hidden = false;

      // hide update cancel button
      Cancel_update_info.hidden = true;
      
      // show Update informations button 
      customer_update_info.hidden = false;
      // hide Confirm update info button  
      confirm_customer_update_info.hidden = true;

    })

    

    $('#confirm_customer_update_info').click(function(){
      // Pass all the data to the modal
        $('#action').val($(this).data('action'));
        $('#connected_user').val($(this).data('connected-user'));
        $('#user').val($(this).data('user'));

    })
    
});

$('#UpdateInfo').click(function () {
  // get all the data from the modal
    var password = $('#password').val();
    var user = $('#user').val(); 
    var connected_user = $('#connected_user').val();

    // Update all info
    var ville = customer_ville_update.val();
    var departement = customer_departement_update.val();
    var sode_postal = customer_postal_update.val();
    var pays = customer_pays_update.val();
    var email = customer_email_update.val();
    var intitule = customer_intitule_update.val();
    var phone = customer_phone_update.val();
    var adress = customer_adress_update.val();
    var adress2 = customer_adress2_update.val();

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
    

})



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

