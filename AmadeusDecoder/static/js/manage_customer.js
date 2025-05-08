$(document).ready(function() {
  // Cache DOM elements
  const elements = {
    customer: {
      // Update inputs
      update: {
        postal: $('#customer_postal_update'),
        intitule: $('#customer_intitule_update'),
        email: $('#customer_email_update'),
        phone: $('#customer_phone_update'),
        adress: $('#customer_adress_update'),
        adress2: $('#customer_adress2_update'),
        departement: $('#customer_departement_update'),
        ville: $('#customer_ville_update'),
        pays: $('#customer_pays_update')
      },
      // Labels
      label: {
        postal: $('#customer_postal_label'),
        intitule: $('#customer_intitule_label'),
        email: $('#customer_email_label'),
        phone: $('#customer_phone_label'),
        adress: $('#customer_adress_label'),
        adress2: $('#customer_adress2_label'),
        departement: $('#customer_departement_label'),
        ville: $('#customer_ville_label'),
        pays: $('#customer_pays_label')
      },
      // Buttons
      buttons: {
        update: $('#customer_update_info'),
        confirm: $('#confirm_customer_update_info'),
        cancel: $('#Cancel_customer_update_info')
      }
    },
    // Filter elements
    filter: {
      pnrMenu: $('.pnrMenu'),
      wrapperMenuFilter: $('.wrapperMenuFilter'),
      allUser: $('#all-user'),
      allUserAfterSearch: $('#all-user-after-search'),
      userResearch: $('#user-research'),
      inputUser: $('#input-user'),
      noFilter: $('#NoFilter'),
      spinner: $('#spinnerLoadingSearch'),
      liElements: $('li.filter-option')
    }
  };

  // Functions for customer information management
  const customerInfo = {
    showUpdateForm: function() {
      // Show all input fields
      Object.values(elements.customer.update).forEach(el => el.prop('hidden', false));
      
      // Hide all labels
      Object.values(elements.customer.label).forEach(el => el.prop('hidden', true));
      
      // Fill inputs with current values
      Object.entries(elements.customer.update).forEach(([key, input]) => {
        const labelValue = elements.customer.label[key].text();
        input.val(labelValue);
      });
      
      // Toggle buttons visibility
      elements.customer.buttons.cancel.prop('hidden', false);
      elements.customer.buttons.update.prop('hidden', true);
      elements.customer.buttons.confirm.prop('hidden', false);
    },
    
    cancelUpdate: function() {
      // Hide all input fields
      Object.values(elements.customer.update).forEach(el => el.prop('hidden', true));
      
      // Show all labels
      Object.values(elements.customer.label).forEach(el => el.prop('hidden', false));
      
      // Toggle buttons visibility
      elements.customer.buttons.cancel.prop('hidden', true);
      elements.customer.buttons.update.prop('hidden', false);
      elements.customer.buttons.confirm.prop('hidden', true);
    },
    
    confirmUpdate: function() {
      // Get data from data attributes
      $('#action').val($(this).data('action'));
      $('#connected_user').val($(this).data('connected-user'));
      $('#user').val($(this).data('user'));
    },
    
    submitUpdate: function() {
      console.log("SUBMITING UPDATE");
      customerId = $("#customer_id").val();
      
      const formData = {
        // Get form values
        customerId: customerId,
        Address: elements.customer.update.adress.val(),
        Address_2: elements.customer.update.adress2.val(),
        Email: elements.customer.update.email.val(),
        Phone: elements.customer.update.phone.val(),
        Country: elements.customer.update.pays.val(),
        City: elements.customer.update.ville.val(),
        Code_postal: elements.customer.update.postal.val(),
        Departement: elements.customer.update.departement.val(),
        
        // Authentication data
        password: $('#password').val(),
        user: $('#user').val(),
        connected_user: $('#connected_user').val(),
        csrfmiddlewaretoken: csrftoken
      };
      
      console.log('FORM DATA : ',formData);
      
      $.ajax({
        type: 'POST',
        url: '/customer/updateInfo',
        dataType: 'json',
        data: formData,
        success: function(data) {
          if (data.status === 200) {
            toastr.success(data.message);
            location.reload();
          } else {
            toastr.error(data.message);
          }
        },
        error: function() {
          toastr.error('Une erreur est survenue lors de la mise à jour.');
        }
      });
    }
  };

  // Functions for user search and filtering
  const userManagement = {
    searchUser: function() {
      const searchTerm = elements.filter.inputUser.val().trim().toLowerCase();
      
      if (!searchTerm) {
        elements.filter.spinner.hide();
        return toastr.warning('La recherche ne doit pas être vide');
      }
      
      elements.filter.spinner.show();
      
      $.ajax({
        type: 'POST',
        url: '/home/user-research',
        dataType: 'json',
        data: {
          user_research: searchTerm,
          csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
          elements.filter.spinner.hide();
          const results = data.results;
          
          if (results.length > 0) {
            // Store search results
            const userResultsData = results.map((user, index) => ({
              id: user.pnr_id,
              position: index,
              number: user.pnr_number
            }));
            
            localStorage.setItem('userAfterSearch', JSON.stringify(userResultsData));
            
            // Update UI
            elements.filter.allUser.hide();
            elements.filter.allUserAfterSearch.empty().show();
            $('#initialPagination').hide();
            
            // Build results table
            const html = userManagement.buildUserTable(results);
            elements.filter.allUserAfterSearch.html(html).trigger('update');
          } else {
            const searchValue = elements.filter.inputUser.val();
            elements.filter.inputUser.val('');
            toastr.error(`Aucun utilisateur ne correspondant à la recherche ~ ${searchValue} ~`);
          }
        },
        error: function() {
          elements.filter.spinner.hide();
          toastr.error('Une erreur est survenue lors de la recherche.');
        }
      });
    },
    
    filterByRole: function(roleId) {
      $.ajax({
        type: 'POST',
        url: '/home/user-filter',
        dataType: 'json',
        data: {
          role_id: roleId,
          csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
          const results = data.results;
          
          if (results.length > 0) {
            // Store filter results
            const userResultsData = results.map((user, index) => ({
              id: user.pnr_id,
              position: index,
              number: user.pnr_number
            }));
            
            localStorage.setItem('userAfterSearch', JSON.stringify(userResultsData));
            
            // Update UI
            elements.filter.allUser.hide();
            elements.filter.allUserAfterSearch.empty().show();
            $('#initialPagination').hide();
            
            // Build results table
            const html = userManagement.buildUserTable(results);
            elements.filter.allUserAfterSearch.html(html).trigger('update');
          } else {
            toastr.error('Aucun utilisateur ne correspondant à la recherche');
          }
          
          userManagement.closeFilter();
        },
        error: function() {
          toastr.error('Une erreur est survenue lors du filtrage.');
        }
      });
    },
    
    buildUserTable: function(users) {
      let html = `
        <thead class="bg-info">
          <tr>
            <th>Nom</th>
            <th>Prénom(s)</th>
            <th>Nom d'utilisateur</th>
            <th>Email</th>
            <th>Rôle</th>
          </tr>
        </thead>
        <tbody class="tbody-user-after-search">
      `;
      
      users.forEach(user => {
        html += `
          <tr 
            onclick="location.href='/user/details/${user.id}/'" 
            style="cursor: pointer;" 
            role="row"
          >
            <td>${user.name}</td>
            <td>${user.first_name}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
          </tr>
        `;
      });
      
      html += '</tbody>';
      return html;
    },
    
    resetFilter: function() {
      elements.filter.liElements.removeClass('active');
      elements.filter.pnrMenu.hide();
      elements.filter.wrapperMenuFilter.hide();
      elements.filter.allUser.show();
      elements.filter.allUserAfterSearch.empty();
    },
    
    closeFilter: function() {
      elements.filter.pnrMenu.hide();
      elements.filter.wrapperMenuFilter.hide();
    }
  };

  // Event bindings
  elements.customer.buttons.update.click(customerInfo.showUpdateForm);
  elements.customer.buttons.cancel.click(customerInfo.cancelUpdate);
  elements.customer.buttons.confirm.click(customerInfo.confirmUpdate);
  $('#UpdateInfo').click(customerInfo.submitUpdate);
  
  elements.filter.userResearch.click(userManagement.searchUser);
  elements.filter.noFilter.click(userManagement.resetFilter);
  
  // Expose functions to global scope
  window.SearchUser = userManagement.searchUser;
  window.ShowUserByType = userManagement.filterByRole;
  window.closeFilter = userManagement.closeFilter;
});