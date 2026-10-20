// Cache des éléments DOM fréquemment utilisés
const DOM = {
    // Éléments de mise à jour des informations
    updateElements: {
      name: document.getElementById('user_name_update'),
      firstName: document.getElementById('user_first_name_update'),
      email: document.getElementById('user_email_update'),
      role: document.getElementById('user_role_update')
    },
    // Éléments d'affichage des informations
    labelElements: {
      name: document.getElementById('user_name_label'),
      firstName: document.getElementById('user_first_name_label'),
      email: document.getElementById('user_email_label'),
      role: document.getElementById('user_role_label')
    },
    // Boutons
    buttons: {
      updatePwd: document.getElementById('UpdatePwdButton'),
      cancelUpdate: document.getElementById('Cancel_update_info'),
      updateInfo: document.getElementById('update_info'),
      confirmUpdate: document.getElementById('confirm_update_info')
    },
    // Éléments de recherche et filtrage
    search: {
      input: $('#input-user'),
      button: $('#user-research'),
      spinner: $('#spinnerLoadingSearch'),
      results: $('#all-user-after-search')
    },
    // Éléments de filtrage
    filter: {
      menu: $('.filter-menu > .list'),
      pnrMenu: $('.pnr-menu'),
      wrapper: $('.wrapper-menu-filter'),
      noFilter: $('#NoFilter')
    },
    // Tables
    tables: {
      allUsers: $('#all-user')
    }
  };
  
  // Initialisation - Masquer les éléments au chargement
  DOM.filter.wrapper.hide();
  DOM.filter.pnrMenu.hide();
  
  /**
   * Ferme le menu déroulant
   */
  function closeCollapse() {
    $('#collapseExample').collapse('hide');
  }

  /**
 * Ferme le filtre
 */
function closeFilter() {
    DOM.filter.pnrMenu.hide();
    DOM.filter.wrapper.hide();
  }
  
  /**
   * Affiche le formulaire de mise à jour des informations utilisateur
   */
  function showUpdateForm() {
    // Afficher tous les champs de saisie
    Object.values(DOM.updateElements).forEach(el => el.hidden = false);
    
    // Masquer toutes les informations
    Object.values(DOM.labelElements).forEach(el => el.hidden = true);
    
    // Pré-remplir les champs avec les valeurs actuelles
    DOM.updateElements.name.value = DOM.labelElements.name.innerText;
    DOM.updateElements.firstName.value = DOM.labelElements.firstName.innerText;
    DOM.updateElements.email.value = DOM.labelElements.email.innerText;
    DOM.updateElements.role.value = DOM.labelElements.role.innerText;
    
    // Gérer l'affichage des boutons
    DOM.buttons.updatePwd.hidden = true;
    DOM.buttons.cancelUpdate.hidden = false;
    DOM.buttons.updateInfo.hidden = true;
    DOM.buttons.confirmUpdate.hidden = false;
  }
  
  /**
   * Masque le formulaire de mise à jour et affiche les informations
   */
  function hideUpdateForm() {
    // Masquer tous les champs de saisie
    Object.values(DOM.updateElements).forEach(el => el.hidden = true);
    
    // Afficher toutes les informations
    Object.values(DOM.labelElements).forEach(el => el.hidden = false);
    
    // Gérer l'affichage des boutons
    DOM.buttons.updatePwd.hidden = false;
    DOM.buttons.cancelUpdate.hidden = true;
    DOM.buttons.updateInfo.hidden = false;
    DOM.buttons.confirmUpdate.hidden = true;
  }

/**
 * Configure le modal pour l'archivage d'un utilisateur
 * @param {Object} data - Données de l'utilisateur
 */
  function setupArchiveModal(data) {
    $('#user_name').text('archiver ' + data.userName + ' ' + data.userFirstName);
    $('#action').val(data.action);
    $('#connected_user').val(data.connectedUser);
    $('#user').val(data.user);
    
    // Définir le titre du modal
    document.querySelector('#modalTitle').innerText = "Archiver un utilisateur";
  }
  
  /**
   * Configure le modal pour la réactivation d'un utilisateur
   * @param {Object} data - Données de l'utilisateur
   */
  function setupReactiveModal(data) {
    $('#user_name').text('réactiver ' + data.userName + ' ' + data.userFirstName);
    $('#action').val(data.action);
    $('#connected_user').val(data.connectedUser);
    $('#user').val(data.user);
    
    // Définir le titre du modal
    document.querySelector('#modalTitle').innerText = "Réactiver un utilisateur";
    
    // Changer le texte du bouton de confirmation
    document.getElementById('ConfirmArchive').textContent = 'Réactiver';
  }

  /**
 * Effectue une requête AJAX
 * @param {Object} options - Options de la requête
 * @returns {Promise} - Promise de la requête
 */
function ajaxRequest(options) {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: options.type || 'POST',
        url: options.url,
        dataType: options.dataType || 'json',
        data: {
          ...options.data,
          csrfmiddlewaretoken: csrftoken
        },
        success: resolve,
        error: reject
      });
    });
  }
  
  /**
   * Gère la réponse d'une requête AJAX
   * @param {Object} data - Données de réponse
   * @param {boolean} reload - Indique si la page doit être rechargée en cas de succès
   */
  function handleAjaxResponse(data, reload = true) {
    if (data.status === 200) {
      toastr.success(data.message);
      if (reload) {
        location.reload();
      }
    } else {
      toastr.error(data.message);
    }
  }

  /**
 * Archive un utilisateur
 * @param {Object} data - Données de l'utilisateur
 */
async function archiveUser(data) {
    try {
      const response = await ajaxRequest({
        url: '/user/archive',
        data: {
          password: data.password,
          user: data.user,
          connected_user: data.connectedUser
        }
      });
      handleAjaxResponse(response);
    } catch (error) {
      toastr.error('Une erreur est survenue lors de l\'archivage de l\'utilisateur');
      console.error(error);
    }
}

  /**
 * Réactive un utilisateur
 * @param {Object} data - Données de l'utilisateur
 */
async function reactiveUser(data) {
    try {
      const response = await ajaxRequest({
        url: '/user/reactive',
        data: {
          password: data.password,
          user: data.user,
          connected_user: data.connectedUser
        }
      });
      handleAjaxResponse(response);
    } catch (error) {
      toastr.error('Une erreur est survenue lors de la réactivation de l\'utilisateur');
      console.error(error);
    }
}

/**
 * Met à jour les informations d'un utilisateur
 * @param {Object} data - Données de l'utilisateur
 */
async function updateUserInfo(data) {
    try {
      const response = await ajaxRequest({
        url: '/user/updateInfo',
        data: {
          name: data.name,
          first_name: data.firstName,
          email: data.email,
          role: data.role,
          password: data.password,
          user: data.user,
          connected_user: data.connectedUser
        }
      });
      handleAjaxResponse(response);
    } catch (error) {
      toastr.error('Une erreur est survenue lors de la mise à jour des informations');
      console.error(error);
    }
}

/**
 * Met à jour le mot de passe d'un utilisateur
 * @param {Object} data - Données de l'utilisateur
 */
async function updateUserPassword(data) {
    try {
        console.log('Updating User Password');
        
      const response = await ajaxRequest({
        url: '/user/UpdatePassword',
        data: {
          password: data.password,
          newPassword: data.newPassword,
          user_id: data.userId
        }
      });
      handleAjaxResponse(response);
    } catch (error) {
      toastr.error('Une erreur est survenue lors de la mise à jour du mot de passe');
      console.error(error);
    }
}

/**
 * Recherche des utilisateurs
 */
async function searchUsers() {
    const searchTerm = DOM.search.input.val().toLowerCase().trim();
    
    if (!searchTerm) {
      DOM.search.spinner.hide();
      toastr.warning('La recherche ne doit pas être vide');
      return;
    }
    
    DOM.search.spinner.show();
    
    try {
      const data = await ajaxRequest({
        url: '/home/user-research',
        data: { user_research: searchTerm }
      });
      
      handleSearchResults(data.results, searchTerm);
    } catch (error) {
      DOM.search.spinner.hide();
      toastr.error('Une erreur est survenue lors de la recherche');
      console.error(error);
    }
}

/**
 * Filtre les utilisateurs par rôle
 * @param {string} roleId - ID du rôle
 */
async function filterUsersByRole(roleId) {
    try {
      const data = await ajaxRequest({
        url: '/home/user-filter',
        data: { role_id: roleId }
      });
      
      handleSearchResults(data.results);
      closeFilter();
    } catch (error) {
      toastr.error('Une erreur est survenue lors du filtrage');
      console.error(error);
    }
}

function handleSearchResults(results, searchTerm = '') {
    DOM.search.spinner.hide();
  
    if (results.length === 0) {
      const message = searchTerm 
        ? `Aucun utilisateur ne correspond à la recherche ~ ${searchTerm} ~` 
        : 'Aucun utilisateur ne correspond à la recherche';
  
        toastr.error(message);
        if (searchTerm) {
          DOM.search.input.val('');
        }
        return;
    }
      
    // Stocker les résultats dans localStorage
    const userAfterSearch = results.map((user, index) => ({
        id: user.id,
        position: index,
        number: user.username
    }));
    
    localStorage.setItem('userAfterSearch', JSON.stringify(userAfterSearch));
    // Préparer et afficher les résultats
    DOM.search.results.html(generateUserTableHTML(results)).show();
    DOM.tables.allUsers.hide();
    $('#initialPagination').hide();
}

/**
 * Génère le HTML pour la table des utilisateurs
 * @param {Array} users - Liste des utilisateurs
 * @returns {string} - HTML de la table
 */

function generateUserTableHTML(users) {
    return `
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
        ${users.map(user => `
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
        `).join('')}
      </tbody>
    `;
  }
  
// Initialisation des gestionnaires d'événements au chargement du document
$(document).ready(function() {
    // Gestionnaires pour la mise à jour des informations
    if (DOM.buttons.updateInfo) {
      DOM.buttons.updateInfo.addEventListener('click', showUpdateForm);
    }
    
    if (DOM.buttons.cancelUpdate) {
      DOM.buttons.cancelUpdate.addEventListener('click', hideUpdateForm);
    }
    
    // Gestionnaire pour l'archivage d'un utilisateur
    $('#archive_user').click(function() {
      setupArchiveModal({
        userName: $(this).data('user-name'),
        userFirstName: $(this).data('user-first-name'),
        action: $(this).data('action'),
        connectedUser: $(this).data('connected-user'),
        user: $(this).data('user')
      });
    });
    
    // Gestionnaire pour la réactivation d'un utilisateur
    $('#reactive_user').click(function() {
      setupReactiveModal({
        userName: $(this).data('user-name'),
        userFirstName: $(this).data('user-first-name'),
        action: $(this).data('action'),
        connectedUser: $(this).data('connected-user'),
        user: $(this).data('user')
      });
    });
    
    // Gestionnaire pour la confirmation de mise à jour des informations
    $('#confirm_update_info').click(function() {
      $('#action').val($(this).data('action'));
      $('#connected_user').val($(this).data('connected-user'));
      $('#user').val($(this).data('user'));
    });
    
    // Gestionnaire pour la confirmation du nouveau mot de passe
    $('#ConfirmNewPassword').click(function() {
      $('#action').val($(this).data('action'));
      $('#connected_user').val($(this).data('connected-user'));
      $('#user').val($(this).data('user'));
    });
    
    // Gestionnaire pour la recherche d'utilisateurs
    DOM.search.button.on('click', searchUsers);
    
    // Gestionnaire pour réinitialiser les filtres
    DOM.filter.noFilter.on('click', function() {
      DOM.filter.menu.removeClass('active');
      DOM.filter.pnrMenu.hide();
      DOM.filter.wrapper.hide();
      DOM.tables.allUsers.show();
      $('#all-user-after-search').remove();
    });
});

// Gestionnaire pour la mise à jour des informations
$('#UpdateInfo').click(function() {
    const action = $('#action').val();
    const password = $('#password').val();
    const user = $('#user').val();
    const connectedUser = $('#connected_user').val();
    
    switch (action) {
      case 'archive':
        archiveUser({ password, user, connectedUser });
        break;
        
      case 'reactive':
        reactiveUser({ password, user, connectedUser });
        break;
        
      case 'update_info':
        updateUserInfo({
          name: $('#user_name_update').val(),
          firstName: $('#user_first_name_update').val(),
          email: $('#user_email_update').val(),
          role: $('#customer-type-int-input').val(),
          password,
          user,
          connectedUser
        });
        break;
        
      case 'update_password':
        console.log('Case Update Password');
        console.log('USER ID : ',user);
        
        
        updateUserPassword({
          password,
          newPassword: $('#new-password').val(),
          userId: user
        });
        break;
    }
});

// Fonction pour filtrer les utilisateurs par type
function ShowUserByType(roleId) {
    filterUsersByRole(roleId);
}