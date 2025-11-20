
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
        $('#connected_user').val($(this).data('connected-user'));
        $('#customer').val($(this).data('customer'));

    })
    
});

$('#UpdateCutomer').click(function () {
  // get all the data from the modal
    var customer_id = $('#customer').val(); 
    var connected_user = $('#connected_user').val();

    // Update all info
    var ville = customer_ville_update.value;
    var departement = customer_departement_update.value;
    var code_postal = customer_postal_update.value;
    var pays = customer_pays_update.value;
    var email = customer_email_update.value;
    var intitule = customer_intitule_update.value;
    var phone = customer_phone_update.value;
    var adress = customer_adress_update.value;
    var adress2 = customer_adress2_update.value;

      var password = $('#password').val();
      $.ajax({
        type: 'POST',
        url: '/customer/updateInfo',
        dataType: "json",
        data : {
          Id:customer_id,
          City : ville,
          Adress : adress,
          Adress2 : adress2,
          Code_postal : code_postal,
          Country : pays,
          Email : email,
          Departement: departement,
          intitule:intitule,
          Phone:phone,
          connected_user : connected_user,
          password: password,
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

function searchCustomers(query, page = 1) {
    if (query.trim() === "") {
        console.log("Recherche vide, affichage de la liste complète ou message.");
    }

    $("#spinnerLoadingSearch").show(); // Supposant que vous avez un spinner

    $.ajax({
        type: "GET", // Utilisez GET pour les recherches
        url: "/customer-search/", // L'URL de votre vue Django
        dataType: "json",
        data: {
            query: query,
            page: page,
        },
        success: function (data) {
            $("#spinnerLoadingSearch").hide();
            if (data.results.length > 0) {
                // console.log("DATA : ",data.results);
                
                updateCustomerTable(data.results,data.total_results);
                
                updatePagination(data);
                
                
            } else {
                toastr.info(`Aucun client ne correspondant à la recherche "${query}"`);
                $("#all-customer").show();
                $("#customer-search-results").hide();
            }
        },
        error: function (xhr, status, error) {
            $("#spinnerLoadingSearch").hide();
            toastr.error("Erreur lors de la recherche des clients.");
            console.error("AJAX Error:", status, error);
        }
    });
}

// Fonction pour mettre à jour le tableau HTML avec les données reçues
function updateCustomerTable(customers,total_results) {
  document.querySelector(".tbody-customer-search-results").innerHTML = "";

  $("#all-customer").hide(); 
  $("#customer-search-results").show(); 
  $('.info-footer-pnr').hide();
  $('#SearchPaginatorSection').removeAttr('hidden').show();
  // $('.total-results-display').removeAttr('hidden').show();
  $('.total-results-count').text(total_results);

    let htmlContent = "";

    customers.forEach(client => {

        let display_name_col1 = '';
        let display_name_col2 = '';

        if (client.last_name && client.first_name) {
            display_name_col1 = client.last_name;
            display_name_col2 = client.first_name;
        } else if (client.last_name) {
            display_name_col1 = client.last_name;
            display_name_col2 = ''; // Vide si seulement last_name
        } else if (client.first_name) {
            display_name_col1 = client.first_name;
            display_name_col2 = ''; // Vide si seulement first_name
        } else {
            display_name_col1 = client.intitule || ''; // Affiche intitule si les deux sont vides
            display_name_col2 = '';
        }

        htmlContent += `
        <tr
            onclick="location.href='/customer/details/${client.id}/'"
            style="cursor: pointer;"
            role="row"
        >
            <td>${display_name_col1}</td>
            <td>${display_name_col2}</td>
            <td>${client.intitule}</td>
            <td>${client.address_1}</td>
            <td>${client.type}</td>
            <td>${client.country}</td>
        </tr>`;
    });

    // Met à jour le contenu du tableau de recherche
    $(".tbody-customer-search-results").html(htmlContent);
}

// This function will be called inside your AJAX success handler.
function updatePagination(data) {
  const paginationContainer = document.getElementById('searchPagination');
  paginationContainer.innerHTML = ''; // Clear existing pagination

  const {
      has_previous,
      has_next,
      next_page_number,
      previous_page_number,
      current_page,
      num_pages
  } = data;

  // Create a new pagination list element
  const ul = document.createElement('ul');
  ul.className = 'pagination pagination-sm m-0';

  // Helper function to create a page item link
  const createPageItem = (text, pageNumber, isActive = false, isEllipsis = false) => {
      const li = document.createElement('li');
      li.className = 'page-item';
      if (isActive) li.classList.add('active');

      const a = document.createElement('a');
      a.className = 'page-link';
      a.textContent = text;
      
      if (isEllipsis) {
          a.href = '#'; // Make ellipsis non-clickable
      } else {
          a.href = '#';
          a.addEventListener('click', (e) => {
              e.preventDefault();
              // Get the current search query from the input field
              const query = $("#input-customer").val();
              
              // Call the search function for the new page
              searchCustomers(query, pageNumber);
          });
      }
      
      li.appendChild(a);
      return li;
  };

  // 1. "Previous" button
  if (has_previous) {
      ul.appendChild(createPageItem('« Précédent', previous_page_number));
  }

  // 2. Page links
  const maxPagesToShow = 5; // e.g., 2 before, 2 after current page + current page
  let startPage = Math.max(1, current_page - Math.floor(maxPagesToShow / 2));
  let endPage = Math.min(num_pages, startPage + maxPagesToShow - 1);
  
  if (endPage - startPage + 1 < maxPagesToShow) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
  }

  // First page link and ellipsis
  if (startPage > 1) {
      ul.appendChild(createPageItem('1', 1));
      if (startPage > 2) {
          ul.appendChild(createPageItem('...', null, false, true));
      }
  }

  // Pages in the middle
  for (let i = startPage; i <= endPage; i++) {
      ul.appendChild(createPageItem(i.toString(), i, i === current_page));
  }
  
  // Last page link and ellipsis
  if (endPage < num_pages) {
      if (endPage < num_pages - 1) {
          ul.appendChild(createPageItem('...', null, false, true));
      }
      ul.appendChild(createPageItem(num_pages.toString(), num_pages));
  }

  // 3. "Next" button
  if (has_next) {
      ul.appendChild(createPageItem('Suivant »', next_page_number));
  }

  // Append the new pagination list to the container
  paginationContainer.appendChild(ul);
}

$(document).ready(function () {
    $("#input-customer").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        
        // Appelez la fonction de recherche côté serveur
        searchCustomers(value);
    });
});
