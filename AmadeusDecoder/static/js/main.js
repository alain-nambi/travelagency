const getCookies = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};


// Add margin-top for screen with lesser or equal to 1280
const pushedSideBarMenu = document.querySelector("#pushed-sidebar")
const pnrManagementMenu = document.querySelector("#pnrManagementMenu")
const layoutHomeMenu = document.querySelector("#layoutHomeMenu")
const screenWidth = window.innerWidth;

if (pushedSideBarMenu) {
  pushedSideBarMenu.addEventListener("click", (_e) => {
    if (layoutHomeMenu) {
      setTimeout(() => {
        let sideBarTrigger = localStorage.getItem("sidebar")
        let layoutHomeMenuheight = layoutHomeMenu.offsetHeight
  
        // console.log(screenWidth);
  
        if (sideBarTrigger == "opened" && screenWidth <= 1280) {
          pnrManagementMenu.setAttribute("style", `margin-top: calc(${layoutHomeMenuheight}px - 20px) !important; visibility: visible;`)
        } else {
          pnrManagementMenu.setAttribute("style", "visibility: visible;")
        }
      }, 100)
    } else {
      console.log("Layout is not visible");
    }
  })
}

// End of Adding margin-top for screen with lesser or equal to 1280

/**Makes the list of active filters in the homepage scrollable vertically.
  @param {listActiveFilter} - The list of active filters in the homepage scrollable filter menu.
*/

// Cette partie du code vérifie si l'élément avec l'id "listActiveFilter" existe dans le document HTML.
const listActiveFilter = document.querySelector("#listActiveFilter");

// Si l'élément existe, on exécute le code à l'intérieur de cette condition.
if (listActiveFilter) {
  let pressed = false; // Variable pour suivre l'état du bouton de la souris (enfoncé ou non)
  let startX = 0; // Variable pour stocker la position initiale de la souris

  // Événement déclenché lorsque le bouton de la souris est enfoncé sur l'élément
  listActiveFilter.addEventListener("mousedown", (e) => {
    // console.log("MOUSE IS DOWN");
    pressed = true; // Le bouton de la souris est enfoncé
    startX = e.clientX; // On enregistre la position initiale de la souris
    listActiveFilter.style.cursor = 'grabbing'; // On change le curseur de la souris
  });

  // Événement déclenché lorsque la souris quitte l'élément
  listActiveFilter.addEventListener("mouseleave", (e) => {
    // console.log("MOUSE IS LEAVING");
    pressed = false; // Le bouton de la souris n'est plus enfoncé
  });

  // Événement déclenché lorsque le bouton de la souris est relâché sur l'élément
  listActiveFilter.addEventListener("mouseup", (e) => {
    // console.log("MOUSE IS UP");
    pressed = false; // Le bouton de la souris n'est plus enfoncé
    listActiveFilter.style.cursor = 'grab'; // On change le curseur de la souris
  });

  // let animationFrameId;

  // Événement déclenché lorsque la souris est déplacée sur l'élément
  listActiveFilter.addEventListener("mousemove", (e) => {
    // console.log("MOUSE IS MOVING");
    // Si le bouton de la souris n'est pas enfoncé, on ne fait rien
    if (!pressed) {
      return;
    }

    listActiveFilter.scrollLeft += startX - e.clientX; // Calcule la distance parcourue par la souris et met à jour le défilement horizontal

    // Annule l'animation frame précédente pour éviter d'effectuer plusieurs animations en même temps
    // cancelAnimationFrame(animationFrameId);

    // Définit une nouvelle animation frame pour effectuer le défilement horizontal
    // animationFrameId = requestAnimationFrame(() => {

    // });
  });
}

/* END OF LIST ACTIVE FILTER FOR FILTER MENU IN HOMEPAGE */

//spinner loading
// $(document).ready(function () {
//   "use strict";
//   $(".loading").show("fade");
//   $(".spinner-wrapper").show();
//   $(".spinner-wrapper").css("position", "fixed");
//   setTimeout(function () {
//     $(".content-all-pnr").css({ visibility: "visible" });
//     $(".spinner-wrapper").hide();
//     $(".spinner-wrapper").css("position", "relative");
//   }, 2000);
// });

// Add agency selected value in document cookies
const agencyListSelection = document.querySelector("#agencyListSelection")

$(document).ready(function () {

  // LOADING THE CURRENT PAGE IF buttonMenuAgencyFilter IS CLICKED
  const buttonMenuAgencyFilter = document.querySelector("#buttonMenuAgencyFilter")
  if (buttonMenuAgencyFilter) {
    buttonMenuAgencyFilter.addEventListener("click", function (e) {
      e.preventDefault()
      if (agencyListSelection.value !== "-1") {
        setTimeout(() => {
          window.location.reload()
        }, 600)
      } else {
        if ($("#alertAgencyFilter").length < 1) {
          $(".alert-agency-filter").append(`
            <span id="alertAgencyFilter" class="text-sm text-danger mt-1 d-flex align-items-center" style="gap: 5px">
              <i class="fa fa-circle-exclamation"></i>
              Veuillez séléctionner une agence
            </span>
          `
          )
        }
      }
    })
  }


  // Retrieve the sorting information from local storage
  let isSortedByCreator = localStorage.getItem('isSortedByCreator');

  // Check if the sorting information is null (not set)
  if (isSortedByCreator === null) {
    // Set the default sorting order and update the icon classes accordingly
    $("#icon__pnrCreator").addClass("fa-arrows-up-down");
    $("#icon__pnrCreator").removeClass("fa-arrow-up");
    $("#icon__pnrCreator").removeClass("fa-arrow-down");
  }
  // Check if the sorting order is ascending
  else if (isSortedByCreator === 'asc') {
    // Update the icon classes to indicate ascending sorting order
    $("#icon__pnrCreator").removeClass("fa-arrows-up-down");
    $("#icon__pnrCreator").removeClass("fa-arrow-up");
    $("#icon__pnrCreator").addClass("fa-arrow-down");
  }
  // If the sorting order is not null and not ascending, assume it is descending
  else {
    // Update the icon classes to indicate descending sorting order
    $("#icon__pnrCreator").removeClass("fa-arrows-up-down");
    $("#icon__pnrCreator").removeClass("fa-arrow-down");
    $("#icon__pnrCreator").addClass("fa-arrow-up");
  }

  // Handle click event on '.pnr-creator-list' elements
  $('.pnr-creator-list').on('click', function (event) {
    event.preventDefault();

    // Remove any previous sorting order information from Cookies
    Cookies.remove('creation_date_order_by', { path: '/home' });
    localStorage.removeItem('isOrderedByDateCreated');

    // Determine the new sorting order based on the current sorting order
    let newSortOrder;
    if (isSortedByCreator === null || isSortedByCreator === 'asc') {
      // If the current sorting order is null or ascending, set descending order
      newSortOrder = 'desc';
      localStorage.setItem('isSortedByCreator', newSortOrder);
      Cookies.set('isSortedByCreator', '-agent__username');
    } else {
      // If the current sorting order is descending, set ascending order
      newSortOrder = 'asc';
      localStorage.setItem('isSortedByCreator', newSortOrder);
      Cookies.set('isSortedByCreator', 'agent__username');
    }

    // Reload the page to apply the new sorting order
    window.location.reload();
  });
});

$(document).ready(function () {
  const isPnrFilterSelected = getCookies("filter_pnr")
  const isCreatorSelected = getCookies("creator_pnr_filter")
  const isDateRangeSelected = getCookies("dateRangeFilter")
  const isStatusSelected = getCookies("filter_pnr_by_status")
  const isAgencySelected = getCookies("agency_name_filter")

  // console.log('====================================');
  // console.log(isPnrFilterSelected);
  // console.log(isCreatorSelected);
  // console.log(isDateRangeSelected);
  // console.log(isStatusSelected);
  // console.log('====================================');

  const isPnrFilterSelectedValue = (pnr) => {
    const buttonPnrFilter = `
      <button 
        style="
          border: none; 
          background: transparent; 
          color: #fff;
        " 
        title="Supprimer le filtre PNR"
        id="buttonPnrFilter"
      >
        <i 
          id="iconCreatorFilter"
          class="fas fa-times-circle pr-2 pl-1"
          style="font-size: 14px;"
        ></i>
      </button>
    `
    const replaceButton = `
      <div class="pr-2"></div>
    `

    const userRoleId = $("#listActiveFilter").data("user-role")
    return `
      <div
        style="
          color: #fff;
          background: #17a2b8;
          border-radius: 6px;
          cursor: drag;
          padding: 2px 1px;
        "
        class="d-flex align-items-center ml-2 my-2"
      >
        <span  
          cy-data="span-status-filter-name" 
          style="font-size: 10px"
          class="pl-2"
        >
          ${pnr}
        </span>
        ${userRoleId !== 3 ? buttonPnrFilter : replaceButton}
      </div>
    `
  }

  // Add filter badge for agency selected value
  const isAgencySelectedValue = (agency) => {
    const agencyName = agency != "0" ? agency : "Pas d'agence";

    const cancelAgencyFilter = `
      <button 
        style="
          border: none; 
          background: transparent; 
          color: #fff;
        " 
        title="Supprimer le filtre d'Agence"
        id="buttonCancelAgencyFilter"
      >
        <i 
          id="iconAgencyFilter"
          class="fas fa-times-circle pr-2 pl-1"
          style="font-size: 14px;"
        ></i>
      </button>
    `

    return `
      <div
        style="
          color: #fff;
          background: #17a2b8;
          border-radius: 6px;
          cursor: drag;
          padding: 2px 1px;
        "
        class="d-flex align-items-center ml-2 my-2"
      >
        <span  
          cy-data="span-status-filter-name" 
          style="font-size: 10px"
          class="pl-2"
        >
          Agence : ${agencyName}
        </span>
        ${cancelAgencyFilter}
      </div>
    `
  }

  const isCreatorSelectedValue = (creator) => {
    const USERS_DATA = document.getElementById("getAllUsername")
    const creators = JSON.parse(creator)
    let usernames = []

    try {
      if (USERS_DATA) {
        const JSON_USERS_DATA = JSON.parse(USERS_DATA.getAttribute("data-users"))

        // console.log('====================================');
        // console.log(JSON_USERS_DATA);
        // console.log('====================================');
        console.log(creators);

        if (creators.length == 1 && creators[0] == "0") {
          usernames = "Tout"
        } else if (creators.includes('Empty')) {
          usernames = "Non attribué"
        }
        else if (creators.length == 1 && creators[0] == "Empty") {
          usernames = 'Non attribué'
        }
        else {
          // console.log('====================================');
          // console.log("usernames");
          // console.log('====================================');
          creators.forEach((creator) => {
            if (!usernames.includes(creator)) {
              usernames.push(JSON_USERS_DATA.find((user) => user.id === parseInt(creator)).username)
            }
          })

          // Sort the array in alphabetical order using the compare function
          usernames.sort((a, b) => a.localeCompare(b));
        }
      }
    } catch (error) {
      console.log("Error on getting USERS DATA", error)
      usernames = "Tout"
    }

    // console.log(usernames);

    let username = "";
    if (usernames.length === 0 || usernames == "Tout") {
      username = "Créateur: Tout"
    } else if (usernames == "Non attribué") {
      username = "Créateur: Non attribué"
    } else if (usernames.length > 1 && usernames != "Tout" && usernames != "Non attribué") {
      username = `Créateur (${usernames.length}) : ${usernames.join(" | ")}`
    } else {
      username = `Créateur: ${usernames}`
    }

    // console.log('====================================');
    // console.log(username);
    // console.log('====================================');

    return `
      <div
        style="
          color: #fff;
          background: #17a2b8;
          border-radius: 6px;
          cursor: drag;
          padding: 2px 1px;
        "
        class="d-flex align-items-center ml-2 my-2"
      >
        <span  
          cy-data="span-creator-name" 
          style="font-size: 10px"
          class="pl-2"
        >
          ${username}
        </span>
        <button 
          style="
            border: none; 
            background: transparent; 
            color: #fff;
          " 
          title="Supprimer le filtre Créateur"
          id="buttonCreatorNameFilter"
        >
          <i 
            id="iconCreatorFilter"
            class="fas fa-times-circle pr-2 pl-1"
            style="font-size: 14px;"
          ></i>
        </button>
      </div>
    `
  }

  const isDateRangeSelectedValue = (date) => {
    const dateStart = date.split(" * ")[0];
    const dateEnd = date.split(" * ")[1];

    // Convertir le chaine de caractère en objet Date() 
    const objDateStart = new Date(dateStart);
    const objDateEnd = new Date(dateEnd);

    // Fonction pour formater une date en format FR
    function formatDateFR(date) {
      const options = { day: 'numeric', month: 'long', year: 'numeric' };
      return date.toLocaleDateString('fr-FR', options);
    }

    return `
      <div
        style="
          color: #fff;
          background: #17a2b8;
          border-radius: 6px;
          cursor: drag;
          padding: 2px 1px;
        "
        class="d-flex align-items-center ml-2 my-2"
      >
        <span  
          cy-data="span-date-range" 
          style="font-size: 10px"
          class="pl-2"
        >
          Date de création: ${formatDateFR(objDateStart)} au ${formatDateFR(objDateEnd)}
        </span>
        <button 
          style="
            border: none; 
            background: transparent; 
            color: #fff;
          " 
          title="Supprimer le filtre Date de création"
          id="buttonDateRangeFilter"
        >
          <i 
            id="iconCreatorFilter"
            class="fas fa-times-circle pr-2 pl-1"
            style="font-size: 14px;"
          ></i>
        </button>
      </div>
    `
  }

  const isStatusSelectedValue = (status) => {
    return `
      <div
        style="
          color: #fff;
          background: #17a2b8;
          border-radius: 6px;
          cursor: drag;
          padding: 2px 1px;
        "
        class="d-flex align-items-center ml-2 my-2"
      >
        <span  
          cy-data="span-status-filter-name" 
          style="font-size: 10px"
          class="pl-2"
        >
          ${status}
        </span>
        <button 
          style="
            border: none; 
            background: transparent; 
            color: #fff;
          " 
          title="Supprimer le filtre Status"
          id="buttonStatusFilter"
        >
          <i 
            id="iconCreatorFilter"
            class="fas fa-times-circle pr-2 pl-1"
            style="font-size: 14px;"
          ></i>
        </button>
      </div>
    `
  }

  // Use JS object instead of if-else conditions or switch case
  const pnrFilterSelectedValues = {
    None: "Tous les PNR",
    False: "PNR: non envoyé",
    True: "PNR: envoyé",
    null: "PNR: non envoyé",
  };

  const statusSelectedValues = {
    0: "PNR: émis",
    1: "PNR: non émis",
    2: "PNR: émis et non émis",
    null: "PNR: émis",
  };

  // Add pnr filter selected value
  if (isPnrFilterSelected !== "None") {
    $("#listActiveFilter").append(`${isPnrFilterSelectedValue(pnrFilterSelectedValues[isPnrFilterSelected])}`);
  }

  // Add pnr status selected value
  if (isStatusSelected !== "2") {
    $("#listActiveFilter").append(`${isStatusSelectedValue(statusSelectedValues[isStatusSelected])}`);
  }

  // Add creator selected value
  if (isCreatorSelected !== null) {
    $("#listActiveFilter").append(`${isCreatorSelectedValue(isCreatorSelected)}`)
  }

  // Add date range selected value
  if (isDateRangeSelected !== null) {
    $("#listActiveFilter").append(`${isDateRangeSelectedValue(isDateRangeSelected)}`)
  }

  // Add agency selected value
  if (isAgencySelected !== null) {
    $("#listActiveFilter").append(`${isAgencySelectedValue(isAgencySelected)}`)
  }

  const listActiveFilter = document.querySelector("#listActiveFilter")
  const userRoleId = $("#listActiveFilter").data("user-role")

  if (listActiveFilter) {
    $("#buttonCreatorNameFilter").on("click", (e) => {
      Cookies.remove("creator_pnr_filter", { path: "/home" })
      window.location.reload()
    })
    $("#buttonDateRangeFilter").on("click", (e) => {
      Cookies.remove("dateRangeFilter", { path: "/home" })
      window.location.reload()
    })
    $("#buttonStatusFilter").on("click", (e) => {
      Cookies.remove("filter_pnr_by_status", { path: "/home" })
      document.cookie = `filter_pnr_by_status=2; SameSite=Lax`
      localStorage.setItem("filterByPnrStatus", "all")
      window.location.reload()
    })
    $("#buttonPnrFilter").on("click", (e) => {
      if (userRoleId !== 3) {
        Cookies.remove("filter_pnr", { path: "/home" })
        document.cookie = `filter_pnr=None; SameSite=Lax`
        localStorage.removeItem("filterPnrBy")
        window.location.reload()
      }
    })
    $("#buttonCancelAgencyFilter").on("click", (e) => {
      Cookies.remove("agency_name_filter", { path: "/home" })
      localStorage.removeItem("agency_name_filter")
      window.location.reload()
    })
  }
})

$(function () {
  const selectNormalize = $("#normalize").selectize({
    onChange: (value) => {
      const userIds = new Set(value)
      const arrayOfUserIds = Array.from(userIds)
      document.cookie = `creator_pnr_filter=${JSON.stringify(arrayOfUserIds)}; SameSite=Lax`;
      localStorage.setItem("creator_pnr_filter", JSON.stringify(arrayOfUserIds));
    }
  })

  // console.log(selectNormalize);

  if (selectNormalize[0]) {
    const control = selectNormalize[0].selectize;
    $("#cancelCreatorFilter").on("click", function () {
      control.clear();
    });
  }

  // if (selectNormalize) {
  //   selectNormalize.value="";
  //   selectNormalize.addEventListener("change", (e) => {
  //     if (e.target.value !== "") {
  //       document.cookie = `creator_pnr_filter=${e.target.value}; SameSite=Lax`;
  //       localStorage.setItem("creator_pnr_filter", JSON.stringify(e.target.value));
  //     }
  //   })
  // }

  // Convertit l'objet Date actuel en une chaîne de caractères représentant la date actuelle au format spécifié ("day month year") et spécifie la locale française.
  const currentDateToString = new Date(Date.now());
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  const localeDateString = currentDateToString.toLocaleDateString('fr-FR', options);

  // Cache tous les éléments de menu de filtre lors du chargement de la page.
  const $wrapperMenuFilter = $(".wrapper-menu-filter");
  const $closeButtonFilter = $(".close-button-filter");
  const $pnrMenu = $(".pnr-menu");
  const $pnrStatus = $(".pnr-status");
  const $dateRangeMenu = $(".date-range-menu");
  const $creatorMenu = $(".creator-group-menu");
  const $agencyMenu = $(".agency-list-menu");
  const liElements = $(".filter-menu > .list");
  const $pnrLiElements = $(".pnr-menu .pnr-list");
  const $pnrStatusLiElements = $(".pnr-status .pnr-list");

  $wrapperMenuFilter.hide();
  $pnrMenu.hide();
  $pnrStatus.hide();
  $dateRangeMenu.hide();
  $creatorMenu.hide();
  $agencyMenu.hide();

  $closeButtonFilter.on("click", function (e) {
    isMenuOpen = !isMenuOpen;
    isMenuOpen ? $wrapperMenuFilter.show() : $wrapperMenuFilter.hide();
    $(this).toggleClass("active", isMenuOpen);
    liElements.removeClass("active");
    $pnrMenu.hide();
    $pnrStatus.hide();
    $dateRangeMenu.hide();
    $creatorMenu.hide();
    $agencyMenu.hide();
  })

  // Initialise des variables booléennes pour suivre l'état des menus ouverts et les filtres sélectionnés.
  let isMenuOpen = false;

  // Attache un gestionnaire d'événements pour afficher/cacher le menu de filtre lorsqu'on clique sur le bouton Menu Filter. Il bascule également la classe CSS active sur le bouton pour refléter son état.
  $("#buttonMenuFilter").click(function (e) {
    isMenuOpen = !isMenuOpen;
    isMenuOpen ? $wrapperMenuFilter.show() : $wrapperMenuFilter.hide();
    $(this).toggleClass("active", isMenuOpen);
    liElements.removeClass("active");
    $pnrMenu.hide();
    $pnrStatus.hide();
    $dateRangeMenu.hide();
    $creatorMenu.hide();
    $agencyMenu.hide();
  });

  document.addEventListener('click', function (event) {
    // console.log(event.target);

    // Vérifie si la variable isMenuOpen est définie et est de type boolean
    if (typeof isMenuOpen === 'boolean') {
      // Vérifie si le menu est ouvert (isMenuOpen est true) et si l'élément cliqué se trouve en dehors du menu
      if (isMenuOpen && !event.target.closest("#buttonMenuFilter, .wrapper-menu-filter, .pnr-menu, .pnr-status, .date-range-menu, .creator-group-menu, .filter-menu > .list, .pnr-menu .pnr-list, .pnr-status .pnr-list, #reportrange, .daterangepicker, .next, .prev, .creator-group-menu, .agency-list, .agency-list-menu.absolute")) {
        // Si les conditions sont remplies, cela signifie que vous avez cliqué en dehors du menu, donc le menu doit être fermé

        // Inverse la valeur de isMenuOpen (true devient false, et vice versa)
        isMenuOpen = !isMenuOpen;

        // Vérifie si les variables sont définies avant de les utiliser
        if ($wrapperMenuFilter && $pnrMenu && $pnrStatus && $dateRangeMenu && $creatorMenu && $agencyMenu) {
          // Masque les éléments suivants pour les rendre invisibles sur la page
          $wrapperMenuFilter.hide();
          $pnrMenu.hide();
          $pnrStatus.hide();
          $dateRangeMenu.hide();
          $creatorMenu.hide();
          $agencyMenu.hide();
        } else {
          console.error('Une ou plusieurs variables ne sont pas définies.');
        }
      }
    } else {
      console.error('La variable isMenuOpen doit être définie et de type boolean.');
    }

    // console.log(isMenuOpen);
  });

  // Attache un gestionnaire d'événements pour chaque élément de menu de filtre afin de sélectionner/désélectionner les filtres et d'afficher/cacher les menus correspondants.
  liElements.click(function (li) {
    liElements.removeClass("active");

    if (this.classList.contains("list-one")) {
      $pnrMenu.show();
      $dateRangeMenu.hide();
      $creatorMenu.hide();
      $pnrStatus.hide();
      $agencyMenu.hide();
    }

    if (this.classList.contains("list-two")) {
      $dateRangeMenu.show();
      $pnrMenu.hide();
      $creatorMenu.hide();
      $pnrStatus.hide();
      $agencyMenu.hide();
    }

    if (this.classList.contains("list-three")) {
      $dateRangeMenu.hide();
      $pnrMenu.hide();
      $creatorMenu.show();
      $pnrStatus.hide();
      $agencyMenu.hide();
    }

    if (this.classList.contains("list-four")) {
      $dateRangeMenu.hide();
      $pnrMenu.hide();
      $creatorMenu.hide();
      $pnrStatus.show();
      $agencyMenu.hide();
    }

    if (this.classList.contains("list-six")) {
      $dateRangeMenu.hide();
      $pnrMenu.hide();
      $creatorMenu.hide();
      $pnrStatus.hide();
      $agencyMenu.show();
    }

    this.classList.add("active");
  });

  // Ajoute la classe CSS opacity-0 à l'icône de coche dans le menu PNR pour la cacher.
  $(".pnr-menu i.fa-check").addClass("opacity-0");

  // Sélectionne toutes les icônes de coche dans le menu PNR et stocke-les dans la variable $pnrCheckIcons. 
  const $pnrCheckIcons = $pnrLiElements.find('i.fa-check');
  const $pnrStatusCheckIcons = $pnrStatusLiElements.find('i.fa-check');

  // console.log($pnrCheckIcons);

  // Récupère le type de filtre actuel à partir de l'objet localStorage.
  const filterType = localStorage.getItem('filterPnrBy');
  const filterStatus = localStorage.getItem('filterByPnrStatus')

  // Initialise un objet qui associe chaque type de filtre à son sélecteur CSS correspondant afin d'éviter la duplication de code.
  const filterSelectors = {
    'all': '#showAllPnr i.fa-check',
    'not send': '#showNotInvoicedPnr i.fa-check',
    'send': '#showInvoicedPnr i.fa-check',
  };

  const filterStatusSelectors = {
    'issued': '#showIssuedPnr i.fa-check',
    'not_issued': '#showNotIssuedPnr i.fa-check',
    'all': '#showAllPnrWithoutIssuing i.fa-check'
  }

  // Nous pouvons utiliser l'opérateur ternaire pour simplifier la logique conditionnelle.
  const selector = filterSelectors[filterType] ? filterSelectors[filterType] : filterSelectors['all'];
  const selectorStatus = filterStatusSelectors[filterStatus] ? filterStatusSelectors[filterStatus] : filterStatusSelectors['issued']

  // Au lieu d'utiliser addClass et removeClass séparément, nous pouvons les chaîner ensemble.
  $pnrCheckIcons.removeClass('opacity-100').addClass('opacity-0');
  $pnrStatusCheckIcons.removeClass('opacity-100').addClass('opacity-0')

  // Si un sélecteur a été trouvé, nous pouvons appliquer la classe d'opacité aux éléments correspondants.
  if (selector) {
    const $visibleIcons = $pnrCheckIcons.filter(selector);
    $visibleIcons.addClass('opacity-100').removeClass('opacity-0');
  }

  // console.log('====================================');
  // console.log(filterStatusSelectors['issued']);
  // console.log('====================================');

  if (selectorStatus) {
    const $visibleIcons = $pnrStatusCheckIcons.filter(selectorStatus)
    $visibleIcons.addClass('opacity-100').removeClass('opacity-0');
  }

  // console.log($($pnrLiElements).find("i.fa-check"));

  $pnrLiElements.click(function () {
    // Retirer la classe "opacity-100" de tous les éléments i
    $(".pnr-menu i.fa-check").removeClass("opacity-100");
    $(".pnr-menu i.fa-check").addClass("opacity-0");

    // Ajouter la classe "opacity-100" à l'élément i du clic en cours
    $(this).find("i.fa-check").addClass("opacity-100");
    $(this).find("i.fa-check").removeClass("opacity-0");

    if (this.classList.contains("list-one")) {
      // Faire quelque chose pour le premier élément de la liste
      localStorage.setItem("filterPnrBy", "all")
      document.cookie = `filter_pnr=None; SameSite=Lax`
    }

    if (this.classList.contains("list-two")) {
      // Faire quelque chose pour le deuxième élément de la liste
      localStorage.setItem("filterPnrBy", "send")
      document.cookie = `filter_pnr=True; SameSite=Lax`
    }

    if (this.classList.contains("list-three")) {
      // Faire quelque chose pour le troisième élément de la liste
      localStorage.setItem("filterPnrBy", "not send")
      document.cookie = `filter_pnr=False; SameSite=Lax`
    }

    setTimeout(() => {
      window.location.reload()
    }, 600)
  });

  $pnrStatusLiElements.click(function () {
    // Retirer la classe "opacity-100" de tous les éléments i
    $(".pnr-status i.fa-check").removeClass("opacity-100");
    $(".pnr-status i.fa-check").addClass("opacity-0");

    // Ajouter la classe "opacity-100" à l'élément i du clic en cours
    $(this).find("i.fa-check").addClass("opacity-100");
    $(this).find("i.fa-check").removeClass("opacity-0");

    if (this.classList.contains("list-one")) {
      // Faire quelque chose pour le premier élément de la liste
      localStorage.setItem("filterByPnrStatus", "issued")
      document.cookie = `filter_pnr_by_status=0; SameSite=Lax`
    }

    if (this.classList.contains("list-two")) {
      // Faire quelque chose pour le deuxième élément de la liste
      localStorage.setItem("filterByPnrStatus", "not_issued")
      document.cookie = `filter_pnr_by_status=1; SameSite=Lax`
    }

    if (this.classList.contains("list-three")) {
      // Faire quelque chose pour le deuxième élément de la liste
      localStorage.setItem("filterByPnrStatus", "all")
      document.cookie = `filter_pnr_by_status=2; SameSite=Lax`
    }

    setTimeout(() => {
      window.location.reload()
    }, 600)
  })

  $(".alert-agency-filter").html('')
  if (agencyListSelection) {
    agencyListSelection.addEventListener("change", (e) => {
      document.cookie = `agency_name_filter=${e.target.value}; SameSite=Lax`;
      localStorage.setItem("agency_name_filter", JSON.stringify(e.target.value));
    })
  }

  // Ajoutez la date locale dans les éléments HTML avec l'ID "dateRangeBegin" et "dateRangeEnd"
  $('#dateRangeBegin, #dateRangeEnd').text(localeDateString);

  // Définit une fonction de rappel pour le choix de date
  function cbStart(start) {
    // Récupère la date de début et de fin depuis localStorage s'ils existent
    const startDateFromLocalStorage = JSON.parse(localStorage.getItem("startDate"));

    // Affiche la plage de dates sélectionnée dans l'élément avec l'ID "reportrange"
    // Si aucune date n'a été récupérée depuis localStorage, affiche la plage de dates courante
    const displayStartDate = startDateFromLocalStorage || start;
    $('#spanReportDateRangeBegin').html(displayStartDate);
  }

  function cbEnd(start) {
    // Récupère la date de début et de fin depuis localStorage s'ils existent
    const EndDateFromLocalStorage = JSON.parse(localStorage.getItem("endDate"));

    // Affiche la plage de dates sélectionnée dans l'élément avec l'ID "reportrange"
    // Si aucune date n'a été récupérée depuis localStorage, affiche la plage de dates courante
    const displayStartDate = EndDateFromLocalStorage || start;
    $('#spanReportDateRangeEnd').html(displayStartDate);
  }

  // Initialise le plugin DateRangePicker sur l'élément avec l'ID "reportrange"
  $('#reportrangebegin').daterangepicker({
    opens: 'right',
    singleDatePicker: true,
    showDropdowns: true,
    minDate: "01/01/2023",
    autoApply: true,
  }, function (start, end, label) {
    // Formate les dates de début et de fin pour l'affichage et le stockage
    const storageFormat = 'YYYY-MM-DD';

    const startDateDisplay = start._d.toLocaleDateString('fr-FR', options);

    const startDateStorage = start.format(storageFormat);

    // Stocke la plage de dates sélectionnée dans un cookie
    document.cookie = `dateRangeBegin=${startDateStorage}; SameSite=Lax`;

    // Stocke la date de début et de fin sélectionnée dans localStorage
    localStorage.setItem("startDate", JSON.stringify(startDateDisplay));

    // Met à jour la plage de dates affichée en appelant la fonction de rappel
    cbStart(startDateDisplay);
  });

  $('#reportrangeend').daterangepicker({
    opens: 'right',
    singleDatePicker: true,
    showDropdowns: true,
    minDate: "01/01/2023",
    autoApply: true,
  }, function (start, end, label) {
    // Formate les dates de début et de fin pour l'affichage et le stockage
    const storageFormat = 'YYYY-MM-DD';

    const startDateDisplay = start._d.toLocaleDateString('fr-FR', options);
    const endDateDisplay = end._d.toLocaleDateString('fr-FR', options);

    const startDateStorage = start.format(storageFormat);

    // Stocke la plage de dates sélectionnée dans un cookie
    document.cookie = `dateRangeEnd=${startDateStorage}; SameSite=Lax`;

    // Stocke la date de début et de fin sélectionnée dans localStorage
    localStorage.setItem("endDate", JSON.stringify(startDateDisplay));

    // Met à jour la plage de dates affichée en appelant la fonction de rappel
    cbEnd(startDateDisplay);
  });

  // Initialise la plage de dates affichée en appelant la fonction de rappel avec la date courante
  cbStart(localeDateString);
  cbEnd(localeDateString);

  // Ajoute un gestionnaire d'événements pour le bouton de filtre pour forcer le rechargement de la page
  $("#buttonMenuFilterByCreationDateRange").on("click", () => {
    const startDateStorage = Cookies.get('dateRangeBegin')
    const endDateStorage = Cookies.get('dateRangeEnd')

    $('#reportrangebegin').removeClass('border border-danger')
    $(".alert-report-range-begin").html('')

    // Function to get the date range from a string date.
    function getDateRange(stringDate) {
      // Split the string date into an array of strings, separated by spaces.
      const dateParts = stringDate.split(" ");

      // Return the first element of the array, which is the date range.
      return dateParts[0];
    }

    // Function to filter the months array by key.
    function getMonth(months, key) {
      // Find the index of the month object in the array that has the specified key.
      const foundMonth = months.findIndex(m => Object.keys(m).includes(key.split(" ")[1]));

      // If the month object is found, return the month number, otherwise return null.
      return foundMonth < 10 ? "0" + (foundMonth + 1) : foundMonth + 1;
    }

    // Function to get the full year from a string date.
    function getFullYear(stringDate) {
      // Split the string date into an array of strings, separated by spaces.
      const dateParts = stringDate.split(" ");

      // Return the third element of the array, which is the full year.
      return dateParts[2];
    }

    if (startDateStorage && endDateStorage) {
      if (startDateStorage > endDateStorage) {
        $('#reportrangebegin').addClass('border border-danger')
        if ($("#alertDateRangeBegin").length < 1) {
          $(".alert-report-range-begin").append(`
            <span id="alertDateRangeBegin" class="text-sm text-danger mt-1 d-flex align-items-center" style="gap: 5px">
              <i class="fa fa-circle-exclamation"></i>
              La date de début doit être inférieure à la date de fin
            </span>
          `
          )
        }
      } else {
        document.cookie = `dateRangeFilter=${startDateStorage} * ${endDateStorage}; SameSite=Lax`;
        setTimeout(() => {
          window.location.reload()
        }, 600)
      }
    } else {
      // Get the start and end dates from the DOM.
      const startDate = $("#spanReportDateRangeBegin").text().trim();
      const endDate = $("#spanReportDateRangeEnd").text().trim();

      // Create an array of months.
      const months = [
        { janvier: "January" },
        { février: "February" },
        { mars: "March" },
        { avril: "April" },
        { mai: "May" },
        { juin: "June" },
        { juillet: "July" },
        { août: "August" },
        { septembre: "September" },
        { octobre: "October" },
        { novembre: "November" },
        { décembre: "December" },
      ];

      // Get the start and end days.
      const startDay = getDateRange(startDate);
      const endDay = getDateRange(endDate);

      // Get the start and end months.
      const startMonth = getMonth(months, startDate);
      const endMonth = getMonth(months, endDate);

      // Get the start and end years.
      const startYear = getFullYear(startDate);
      const endYear = getFullYear(endDate);

      // Create the start and end date cookies.
      const startDateCookie = `${startYear}-${startMonth}-${startDay}`;
      const endDateCookie = `${endYear}-${endMonth}-${endDay}`;

      if (startDateCookie > endDateCookie) {
        $('#reportrangebegin').addClass('border border-danger')
        if ($("#alertDateRangeBegin").length < 1) {
          $(".alert-report-range-begin").append(`
            <span id="alertDateRangeBegin" class="text-sm text-danger mt-1 d-flex align-items-center" style="gap: 5px">
              <i class="fa fa-circle-exclamation"></i>
              La date de début doit être inférieure à la date de fin
            </span>
          `
          )
        }
      } else {
        // Set the date range filter cookie.
        document.cookie = `dateRangeBegin=${startDateCookie}; SameSite=Lax`;
        document.cookie = `dateRangeEnd=${endDateCookie}; SameSite=Lax`;
        document.cookie = `dateRangeFilter=${startDateCookie} * ${endDateCookie}; SameSite=Lax`;

        // Reload the page after 600 milliseconds.
        setTimeout(() => {
          window.location.reload();
        }, 600);
      }

    }
  })

  $("#buttonMenuFilterByCreator").on("click", (e) => {
    e.preventDefault()
    if (selectNormalize[0].value !== "") {
      setTimeout(() => {
        window.location.reload()
      }, 600)
    } else {
      if ($("#alertEmptyCreator").length < 1) {
        $(".creator-group ").append(`
          <span id="alertEmptyCreator" class="text-sm text-danger mt-1 d-flex align-items-center" style="gap: 5px">
            <i class="fa fa-circle-exclamation"></i>
            Veuillez sélectionner le créateur
          </span>
        `
        )
      }
    }
  })
});

//local storage sidebar
var $toggleButton = $("#pushed-sidebar");
var $pushSelectors = $("#pushed-content");
var sidebarIsOpen;
var openSidebarOnLoad = false;
// function toggleSidebar() {
//   sidebarIsOpen = !sidebarIsOpen;
//   if ($pushSelectors.hasClass("sidebar-collapse")) {
//     $pushSelectors.removeClass("sidebar-collapse");
//   }
//   if (sidebarIsOpen) {
//     $pushSelectors.addClass("sidebar-collapse");
//     localStorage.setItem("sidebar", "opened");
//   } else {
//     $pushSelectors.removeClass("sidebar-collapse");
//     localStorage.setItem("sidebar", "closed");
//   }
// }
// if (localStorage.getItem("sidebar") === null) {
//   sidebarIsOpen = openSidebarOnLoad;
// } else {
//   if (localStorage.getItem("sidebar") === "opened") {
//     sidebarIsOpen = true;
//   } else {
//     sidebarIsOpen = false;
//   }
// }
// if (sidebarIsOpen) {
//   $pushSelectors.removeClass("sidebar-collapse");
// }
// $toggleButton.on("click", toggleSidebar);

// //sort table in all-pnr
// $(function () {
//   var $table = $("#all-pnr");
//   $table.tablesorter({
//     widgets: ["zebra", "columns", "stickyHeaders"],
//   });
// });

// $(function () {
//   let $table = $("#tableAnomaly");
//   $table.tablesorter({
//     widgets: ["zebra", "columns", "stickyHeaders"],
//   });
// })

// Utiliser le plugin de tri de Moment.js avec TableSorter
// Ajouter un analyseur de date personnalisé pour le format de date de votre tableau
$.tablesorter.addParser({
  id: "customDateTimeParser",
  is: function (s) {
    // Vérifier si la valeur de la cellule est une date
    return moment(s, "DD/MM/YY HH:mm", true).isValid();
  },
  format: function (s) {
    // Convertir la date en timestamp pour permettre un tri numérique
    return moment(s, "DD/MM/YY HH:mm").unix();
  },
  type: "numeric",
});

$.tablesorter.addParser({
  id: "customDateParser",
  is: function (s) {
    // Vérifier si la valeur de la cellule est une date
    return moment(s, "DD/MM/YY", true).isValid();
  },
  format: function (s) {
    // Convertir la date en timestamp pour permettre un tri numérique
    return moment(s, "DD/MM/YY").unix();
  },
  type: "numeric",
});

// Appliquer la tablesorter à votre tableau avec l'analyseur de date personnalisé
$("#all-pnr").tablesorter({
  headers: {
    // Disable sorting for elements with the class "pnr-creation-date"
    ".pnr-creation-date": {
      sorter: false,
    },
    // Disable sorting for elements with the class "pnr-creator-list"
    ".pnr-creator-list": {
      sorter: false,
    },
    // Use a custom date parser for elements with the class "pnr-issuing-date"
    ".pnr-issuing-date": {
      sorter: "customDateParser",
    },
  },
  // Enable additional tablesorter widgets
  widgets: ["zebra", "columns", "stickyHeaders"],
});

$("#tableAnomaly").tablesorter({
  headers: {
    0: { sorter: "customDateTimeParser" },
  },
  widgets: ["zebra", "columns", "stickyHeaders"],
});

//filter
$(".filter").click(function () {
  // $('.tr-filter').prop('hidden', false);
  $(".filter").prop("hidden", false);
});
// //search function in all pnr
// $(document).ready(function () {
//   /*$("#input-pnr").on("keyup", function () {
//     var value = $(this).val().toLowerCase();
//     $("tr.pnr-class").filter(function () {
//       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
//     });
//   });*/
//   // Modif pnr research via btn
//   $("#pnr-research").on("click", function () {
//     searchFunction();
//   });
// });

//search function in all constat
$(document).ready(function () {
  $("#input-constat").on("keyup", function () {
    var value = $(this).val().toLowerCase();

    $("tr.constat-class").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

// Search function for customers list
$(document).ready(function () {
  $("#input-customer").on("keyup", function () {
    var value = $(this).val().toLowerCase();

    $("tr.client-list").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});

//filter table function
$("select#sort-status").change(function () {
  var filter = $(this).val();
  filterListtable(filter);
});
function filterListtable(value) {
  var list = $(".pnr-class");
  $(list).hide("fadeOut");
  if (value == "All") {
    $(".tbody-pnr")
      .find(".pnr-class")
      .each(function (i) {
        $(this).show("fade");
      });
  } else {
    $(".tbody-pnr")
      .find(".pnr-class[data-status = " + value + "]")
      .each(function (i) {
        $(this).show("fade");
      });
  }
}

// Get all Fee Cost and all Amount Ticket
let allFeeCost = document.querySelectorAll(".fee-cost.inputeditable");
let allAmountTicket = document.querySelectorAll(".montant.fee-total");
const resetFeeCostValue = () => {
  // For each Fee Cost set value to the current cost
  allFeeCost.forEach((feeCost) => {
    feeCost.value = feeCost.getAttribute("data-cost");
  });

  // For eact Amount Ticket set value to the total fee cost
  allAmountTicket.forEach((amountTicket) => {
    amountTicket.textContent = amountTicket.getAttribute("data-fee-total");
  });
};

resetFeeCostValue();

//edit in pnr details
$(document).ready(function () {
  let input__feeCost = document.querySelectorAll("input.fee-cost");
  $("input.fee-cost").prop("disabled", true);
  $(".passagers-check").prop("disabled", true);
  $(".passengers-align-checkboxes").prop("disabled", true);
  $(".select2").attr("style", "display: none !important");
  $(".selection").attr("style", "display: none !important");
  $("#save").prop("hidden", true);

  const buttonDeleteOtherFeeService = document.querySelectorAll("#deleteOtherFeeService")
  const buttonDeleteOtherFeeServiceModalConfirmation = document.querySelector("#deleteOtherFeeServiceModalConfirmation")
  const spanOtherFeeDesignation = document.querySelector("#otherFeeDesignation")
  const textConfirmationDeleteOtherFeeService = document.querySelector("#textConfirmationDeleteOtherFeeService")

  $("#edit").click(function () {
    // Function to handle the click event on the confirmation button
    const handleConfirmationButtonClick = async (otherFee, csrftoken) => {
      try {
        // AJAX request to remove the other fee
        $.ajax({
          type: "POST",
          url: "/home/other-fee/remove/",
          dataType: "json",
          data: {
            other_fee_id: otherFee[0],
            csrfmiddlewaretoken: csrftoken,
          },
          success: (response) => {
            // If the other fee is successfully deleted
            if (response.status === "deleted") {
              const { designation, total } = response;
              const message = `Le service ${designation} avec un montant total de ${parseFloat(
                total
              ).toFixed(2)} a été supprimé...`;

              // Display success message using toastr
              toastr.clear();
              toastr.success(message);

              // Find and remove the corresponding table row
              const trTableOtherFees =
                document.querySelectorAll(".tr-other-fees");
              const trTableOtherFeesFee = document.querySelectorAll(".tr-other-fees-fee")

              const tableToDelete = Array.from(trTableOtherFees).find(
                (table) => parseInt(table.dataset.otherFeeId) === otherFee[0]
              );

              const tableOtherFeesFeeToDelete = Array.from(trTableOtherFeesFee).find(
                (table) => parseInt(table.dataset.otherFeeId) === otherFee[0]
              );

              // Optional chaining to handle the case where the table is already removed
              tableToDelete?.remove();
              tableOtherFeesFeeToDelete?.remove();
            }
          },
          error: (error) => {
            console.log(error);
          },
        });
      } catch (error) {
        console.log(error);
      }
    };

    // Function to handle the click event on the delete button
    const handleDeleteButtonClick = (deleteButton) => {
      const otherFee = [];

      // Add click event listener to the delete button
      deleteButton.addEventListener("click", () => {
        const otherFeeType = deleteButton.dataset.otherFeeType;
        const otherFeeId = parseInt(deleteButton.dataset.otherFeeId);
        const otherFeeDesignation = String(
          deleteButton.dataset.otherFeeDesignation
        );
        const otherFeeTotal = parseFloat(
          deleteButton.dataset.otherFeeTotal
        ).toFixed(2);

        // Store information about the other fee
        otherFee.push(otherFeeId);

        // Update the confirmation message
        if (otherFeeType == 'AVOIR COMPAGNIE') {
          spanOtherFeeDesignation.innerHTML = `<strong>${otherFeeType}</strong> avec un montant total de ${otherFeeTotal} euros`;
          textConfirmationDeleteOtherFeeService.textContent = `Oui, supprimer l'${otherFeeType}`;

        }
        else {
          spanOtherFeeDesignation.innerHTML = `<strong>${otherFeeDesignation}</strong> avec un montant total de ${otherFeeTotal} euros`;
          textConfirmationDeleteOtherFeeService.textContent = `Oui, supprimer ${otherFeeDesignation}`;

        }

      });

      return otherFee;
    };

    // Check if buttonDeleteOtherFeeService is available
    if (buttonDeleteOtherFeeService) {
      try {
        // AJAX request to get product information
        $.ajax({
          type: "GET",
          url: "/home/get-all-products/",
          dataType: "json",
          data: {
            csrfmiddlewaretoken: csrftoken,
          },
          success: (response) => {
            // List of product designations
            const productDesignationList = response.product_designation_list;

            // Loop through delete buttons
            buttonDeleteOtherFeeService.forEach((deleteButton) => {
              // Check if the product designation matches and update visibility

              if (
                productDesignationList.includes(
                  deleteButton.dataset.otherFeeDesignation
                ) || deleteButton.dataset.otherFeeType == 'AVOIR COMPAGNIE'
              ) {
                deleteButton.classList.replace("d-none", "d-block");
              }
              else {
                deleteButton.classList.replace("d-block", "d-none");
              }

              // Attach click event handlers
              const otherFee = handleDeleteButtonClick(deleteButton);

              // Attach click event handler for confirmation button
              buttonDeleteOtherFeeServiceModalConfirmation.addEventListener(
                "click",
                () => {
                  handleConfirmationButtonClick(otherFee, csrftoken);
                }
              );
            });
          },
          error: (error) => {
            console.log(error);
          },
        });
      } catch (error) {
        console.error(error);
      }
    }

    const select2CustomerList = document.getElementById(
      "select2-customer-list-container"
    );

    if (select2CustomerList != null || select2CustomerList != undefined) {
      $(".customer-select").val(null).trigger("change");
    }

    $(".passengers-align-checkboxes").prop("disabled", false);
    $(".ticket-checkbox-passenger").prop("disabled", false);

    if (input__feeCost != null) {
      input__feeCost.forEach((input) => {
        let isFeeInvoiced = input.getAttribute("data-fee-is-invoiced");
        let isOtherFeeInvoiced = input.getAttribute(
          "data-other-fee-is-invoiced"
        );

        if (isOtherFeeInvoiced != null) {
          console.log(isOtherFeeInvoiced);
          if (isOtherFeeInvoiced == "True") {
            input.setAttribute("disabled", true);
            input.classList.add("inputeditable");
          }
          if (isOtherFeeInvoiced == "False") {
            input.removeAttribute("disabled");
            input.classList.remove("inputeditable");
          }
        }

        if (isFeeInvoiced != null) {
          if (isFeeInvoiced == "True") {
            input.setAttribute("disabled", true);
            input.classList.add("inputeditable");
          }
          if (isFeeInvoiced == "False") {
            input.removeAttribute("disabled");
            input.classList.remove("inputeditable");
          }
        }
      });
    }

    if (buttonModifyCustomer != null) {
      buttonModifyCustomer.forEach((button) => {
        button.classList.remove("d-none");
        button.classList.add("d-flex");
        button.addEventListener("click", (e) => {
          oldCustomerId = e.target.getAttribute("data-customer-id");
        });
      });
    }

    // $("input.fee-cost").removeClass("inputeditable");

    if (
      $("#spanRefCode").length > 0 &&
      $("#spanRefCode").text().trim() != "Pas de référence"
    ) {
      $("#spanRefCode").prop("hidden", false);
      $("#ref_cde").prop("hidden", true);
    } else {
      $("#spanRefCode").prop("hidden", true);
      $("#ref_cde").prop("hidden", false);
    }

    // Deactivate the create receipt's button
    $("#buttonCreateReceipt").prop("hidden", true);

    $(".other-fees-check").prop("disabled", false);
    $(this).prop("hidden", true);
    $("#save").prop("hidden", false);
    $("#create-command").prop("hidden", true);
    $(".select2").attr("style", "display: inline-block !important");
    $(".selection").attr("style", "display: block !important");

    $("#cancel").prop("hidden", false);
    $(".tr-add-line").prop("hidden", false);
    $(".customer-select").prop("hidden", false);
    $(".agent-select").prop("hidden", false);
    $(".span-user").prop("hidden", true);
    $(".customer-default").prop("hidden", false);
    $(".agent-assign").prop("hidden", true);
    $(".add-customer").prop("hidden", false);
    $(".add-line").prop("hidden", false);
    $(".tr-add-line").prop("hidden", false);
    $(".prev1").prop("hidden", true);
    $(".prev2").prop("hidden", false);
    $(".next1").prop("hidden", true);
    $(".next2").prop("hidden", false);
    $(".duplicate-deactive").prop("hidden", true);
    $(".duplicate-active").prop("hidden", false);
  });

  $("#cancel").click(function () {
    if (buttonDeleteOtherFeeService) {
      buttonDeleteOtherFeeService.forEach((deleteButton) => {
        deleteButton.classList.replace("d-block", "d-none");
      })
    }

    const SpanAmoutTotalMain = document.getElementById("pnr-amount-total");
    const SpanFeesTotalMain = document.getElementById("total-services-fees");
    SpanAmoutTotalMain.textContent = parseFloat(
      SpanAmoutTotalMain.getAttribute("data-amount-total")
    ).toFixed(2);
    SpanFeesTotalMain.textContent = parseFloat(
      SpanFeesTotalMain.getAttribute("data-amount-fees")
    ).toFixed(2);
    if (
      count__ticketCheckBoxPassenger > 0 ||
      count__otherFeeCheckBox > 0 ||
      count__feeCheckBox == 0
    ) {
      $(".p-checkbox").each(function () {
        var data_id = $(this).data("id");
        $(".check" + data_id).prop("checked", true);
        $(".checkto" + data_id).prop("checked", true);
      });
    }
    const select2CustomerList = document.getElementById(
      "select2-customer-list-container"
    );

    if (select2CustomerList != null || select2CustomerList != undefined) {
      $(".customer-select").val(null).trigger("change");
    }

    // Activate the create receipt's button
    $("#buttonCreateReceipt").prop("hidden", false);
    $(".to-hide-when-cancel").prop("checked", true);
    $(this).prop("hidden", true);
    $(".passengers-align-checkboxes").prop("disabled", true);
    $(".ticket-checkbox-passenger").prop("disabled", true);
    $("input.fee-cost").addClass("inputeditable");
    $("#edit").prop("hidden", false);
    $("#save").prop("hidden", true);
    $("#create-command").prop("hidden", false);
    $(".select2").attr("style", "display: none !important");
    $(".selection").attr("style", "display: none !important");
    $(".add-customer").prop("hidden", true);
    $("#ref_cde").prop("hidden", true);
    $("#spanRefCode").prop("hidden", false);
    $(".tr-add-line").prop("hidden", true);
    $(".other-fees-check").prop("disabled", true);
    $("input.fee-cost").prop("disabled", true);
    $(".customer-select").prop("hidden", true);
    $(".agent-select").prop("hidden", true);
    $(".span-user").prop("hidden", false);
    $(".customer-default").prop("hidden", false);
    $(".agent-assign").prop("hidden", false);
    $(".new-line").prop("hidden", true);
    $(".tr-add-line").prop("hidden", true);
    $(".save-line").prop("hidden", true);
    $(".ignore").prop("hidden", true);
    $(".prev1").prop("hidden", false);
    $(".prev2").prop("hidden", true);
    $(".next1").prop("hidden", false);
    $(".next2").prop("hidden", true);
    $(".duplicate-deactive").prop("hidden", false);
    $(".duplicate-active").prop("hidden", true);
    var amount_total = $("#pnr-amount-total").attr("data-amount-total");
    $("#pnr-amount-total").text(amount_total);

    resetFeeCostValue();

    if (buttonModifyCustomer != null) {
      buttonModifyCustomer.forEach((button) => {
        button.classList.remove("d-flex");
        button.classList.add("d-none");
        button.addEventListener("click", (e) => {
          oldCustomerId = e.target.getAttribute("data-customer-id");
        });
      });
    }
  });
});

//btn add line
$(document).ready(function () {
  $(".add-line").click(function () {
    $(this).prop("hidden", true);
    $(".tr-add-line").prop("hidden", true);
    $(".new-line").prop("hidden", false);
    $(".save-line").prop("hidden", false);
    $(".ignore").prop("hidden", false);
  });
  $(".ignore").click(function () {
    $(".tr-add-line").prop("hidden", false);
    $(".add-line").prop("hidden", false);
    $(".new-line").prop("hidden", true);
    $(".save-line").prop("hidden", true);
    $(".ignore").prop("hidden", true);
  });
});
//block if new cost < current
// $(document).ready(function () {
//   $(".fee-cost").change(function () {
//     var value = $(this).val();
//     var val = parseInt($(this).val());
//     $(this).val(val.toFixed(2));
//     var data_cost = $(this).attr("data-cost");
//     if (val < data_cost) {
//       console.log('error');
//     }
//     else {
//       console.log('success');
//     }
//   });
// });

//block if not number in cost
$(document).ready(function () {
  $(".fee-cost").keypress(function (evt) {
    return /^[0-9]*\.?[0-9]*$/.test($(this).val() + evt.key);
  });
  $(".value_page").keypress(function (evt) {
    return /^[0-9]*\.?[0-9]*$/.test($(this).val() + evt.key);
  });
});

function copyarchivedpnrhistory() {
  var content = document.getElementById("pnrArchivedHistory");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  document.execCommand("copy");
  toastr.info(
    "RPP/TTH a été copié dans presse papier"
  );
}

const npArchivedTicket = document.querySelector("#npArchivedTicket")
if (npArchivedTicket) {
  $('#npArchivedTicket').on('input', function () {
    ticket = $('#npArchivedTicket').val();
    var inputValue = $(this).val();
    var sanitizedValue = inputValue.replace(/[^0-9-]/g, '');
    $(this).val(sanitizedValue);
});
}

function copyarchivedpnrticket() {
  var content = document.getElementById("pnrArchivedTicket");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);

  const npArchivedTicket = $("#npArchivedTicket").val().replace(/[^0-9]/gi, "");

  // console.log(typeof(npArchivedTicket), parseInt(npArchivedTicket));

  if (npArchivedTicket.length > 0 && npArchivedTicket.length <= 2 && parseInt(npArchivedTicket) > 0) {
    navigator.clipboard.writeText(`WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/TST${parseInt(npArchivedTicket)}`)
      .then(() => {
        toastr.info(`WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/TST${parseInt(npArchivedTicket)} a été copié dans presse papier`);
      })
      .catch((error) => {
        console.error('Unable to copy to clipboard', error);
      });
  } else {
    toastr.error("Veuillez saisir le numéro de ligne valide!");
  }

  setTimeout(function () {
    $("#pnrArchivedTicket").text(`WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/TST`);
    $("#npArchivedTicket").val("");
  }, 1000);
}


//copy pnr
function copyarchivedpnr() {
  var content = document.getElementById("pnrArchived");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);

  const pnr_number = $("#npArchived")
    .val()
    .replace(/[^A-Z0-9]/gi, "");
  if (pnr_number.length == 6) {
    document.execCommand("copy");
    toastr.info(
      "WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/RLC a été copié dans presse papier"
    );
  } else {
    // navigator.clipboard.writeText('');
    toastr.error("Veuillez saisir un numero de PNR valide!");
  }

  setTimeout(function () {
    $("#pnrArchived").text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/RLC-");
    $("#npArchived").val("");
  }, 1000);
}

function copypnr() {
  var content = document.getElementById("pnr");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  const pnr_number = $("#np")
    .val()
    .replace(/[^A-Z0-9]/gi, "");
  if (pnr_number.length == 6) {
    document.execCommand("copy");
    toastr.info(
      "WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RT a été copié dans presse papier"
    );
  } else {
    // navigator.clipboard.writeText('');
    toastr.error("Veuillez saisir un numero de PNR valide!");
  }

  setTimeout(function () {
    $("#pnr").text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RT");
    $("#np").val("");
  }, 1000);
}

function copybne() {
  var content = document.getElementById("bne");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  document.execCommand("copy");
  toastr.info(
    "WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TQT/T a été copié dans presse papier"
  );
  // setTimeout(function () {
  //   $('#bne').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TQT/T");
  //   $('#nt').val("");
  // }, 1000)
}
function copybe() {
  var content = document.getElementById("be");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  document.execCommand("copy");
  toastr.info(
    "WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TWD/L a été copié dans presse papier"
  );
  // setTimeout(function () {
  //   $('#be').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TWD/L");
  //   $('#nlbe').val("");
  // }, 1000)
}
function copyse() {
  var content = document.getElementById("se");
  var selection = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  document.execCommand("copy");
  toastr.info(
    "WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/EWD/L a été copié dans presse papier"
  );
  // setTimeout(function () {
  //   $('#se').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/EWD/L");
  //   $('#nlse').val("");
  // }, 1000)
}

//
function copymailuser() {
  var content = document.getElementById("mail-user");
  var range = document.createRange();
  var selection = window.getSelection();
  var data = $("#mail-user").data("mail");
  range.selectNodeContents(content);
  selection.removeAllRanges();
  selection.addRange(range);
  document.execCommand("copy");
  toastr.info(data + " a été copié dans presse papier");
  // setTimeout(function () {
  //   $('#se').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/EWD/L");
  //   $('#nlse').val("");
  // }, 1000)
}

//new num cmd
/* 1 np*/
$('input[type="text"]#np').on("change", function np() {
  var texInputValue = $("#np").val();
  if (texInputValue != "") {
    $("#pnr").append(texInputValue.toUpperCase());
  } else if (texInputValue == "") {
    $("#pnr").text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RT");
  }
});

$('input[type="text"]#npArchived').on("change", function np() {
  var texInputValue = $("#npArchived").val();
  if (texInputValue != "") {
    $("#pnrArchived").append(texInputValue.toUpperCase());
  } else if (texInputValue == "") {
    $("#pnrArchived").text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/RPP/RLC-");
  }
});

//btn signal
$(".pnr-signal-fab").click(function () {
  $(".pnr-signal-fab .wrap").toggleClass("ani");
  $(".pnr-signal").toggleClass("open");
});
$(".hide").click(function () {
  $(".pnr-signal").removeClass("open");
});

//next prev anomalie
var idconstat = $("#anomalie_id").data("id");
//var linkdevanomalie='http://127.0.0.1:8000/comment-detail/';
var linkprodanomalie = "http://5.135.136.201:8000/comment-detail/";
function next() {
  idconstat++;
  location.href = linkprodanomalie + idconstat++;
}
function prev() {
  idconstat--;
  location.href = linkprodanomalie + idconstat--;
}
function eraseCache() {
  window.location.reload();
}

$(".card-header").addClass("fixed-header");
$("#tr-all-pnr").addClass("sticky-tr-table");

// //card-header sticky
// $(window).scroll(function () {
//   // if ($(window).scrollTop() >= 80) {
//     $(".card-header").addClass("fixed-header");
//     $("#tr-all-pnr").addClass("sticky-tr-table");
//   // } else {
//   //   $(".card-header").removeClass("fixed-header");
//   //   $("#tr-all-pnr").removeClass("sticky-tr-table");
//   // }
// });

//limit length comment and response
$("#comment span").text(function (index, currentText) {
  var maxLength = $(this).parent().attr("data-maxlength");
  if (currentText.length >= maxLength) {
    return currentText.substr(0, maxLength) + "...";
  } else {
    return currentText;
  }
});
$("#response span").text(function (index, currentText) {
  var maxLength = $(this).parent().attr("data-maxlength");
  if (currentText.length >= maxLength) {
    return currentText.substr(0, maxLength) + "...";
  } else {
    return currentText;
  }
});

//filter interval two date
function filterRows() {
  var from = $("#datefilterfrom").val();
  var to = $("#datefilterto").val();
  if (!from && !to) {
    // no value for from and to
    return;
  }
  from = from; // default from to a old date if it is not set
  to = to;
  var dateFrom = moment(from);
  var dateTo = moment(to);
  $("tr.pnr-class").each(function (i, tr) {
    var val = $(tr).find("td:nth-child(4)").text();
    var dateVal = moment(val, "DD/MM/YYYY");
    var visible = dateVal.isBetween(dateFrom, dateTo, null, []) ? "" : "none"; // [] for inclusive
    $(tr).css("display", visible);
  });
}

$("#datefilterfrom").on("change", filterRows);
$("#datefilterto").on("change", filterRows);

//check to ckeck passenger
$(".p-checkbox").each(function () {
  var data_id = $(this).data("id");
  $(".checkto" + data_id).prop("checked", true);
  $.each($(this).data(), function () {
    $(".check" + data_id).change(function () {
      if (this.checked) {
        $(".checkto" + data_id).prop("checked", true);
      } else {
        $(".checkto" + data_id).prop("checked", false);
      }
    });
  });
});

/**
 * check and uncheck all checkbox related to the data-customer-id attribute
 */
$(".p-checkbox").each(function () {
  var data_id = $(this).data("id");
  $(".check" + data_id).prop("checked", true);
  $.each($(this).data(), function () {
    $(".checkto" + data_id).change(function () {
      let feeIndex = $(this).index(".checkto" + data_id);
      let feeCheckboxChecking = $(".checkto" + data_id)[feeIndex + 1];

      console.log("Index de la checkbox: " + feeIndex);
      console.log("Type de la checkbox: " + feeCheckboxChecking.getAttribute("data-type"));

      if (this.checked) {
        $(".check" + data_id).prop("checked", true);
        if (feeCheckboxChecking.getAttribute("data-type") == "fee") {
          $(feeCheckboxChecking).prop("checked", true);
        }
      } else {
        $(".check" + data_id).prop("checked", false);
        if (feeCheckboxChecking.getAttribute("data-type") == "fee") {
          $(feeCheckboxChecking).prop("checked", false);
        }
      }
    });
  });
});
//
$(".dropdown-menu a.dropdown-toggle").on("click", function (e) {
  if (!$(this).next().hasClass("show")) {
    $(this).parents(".dropdown-menu").first().find(".show").removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass("show");

  $(this)
    .parents("li.nav-item.dropdown.show")
    .on("hidden.bs.dropdown", function (e) {
      $(".dropdown-submenu .show").removeClass("show");
    });

  return false;
});
//select customer or company
$(document).ready(function () {
  $(".select-type").change(function () {
    var type = $(this).val();
    if (type == "Société") {
      $(".customer-name").prop("hidden", true);
      $(".customer-lastname").prop("hidden", true);
      $(".company").prop("hidden", false);
    } else {
      $(".customer-name").prop("hidden", false);
      $(".customer-lastname").prop("hidden", false);
      $(".company").prop("hidden", true);
    }
  });
});

//blink
function blinker() {
  $(".cde_blink").fadeOut(500);
  $(".cde_blink").fadeIn(500);
}
setInterval(blinker, 1000);

//
$(document).ready(function () {
  // var typed = "";
  if ($(".customer-select").length > 0) {
    // $(".customer-select").select2({
    //   placeholder: "Sélectionner client",
    //   allowClear: true,
    //   language: {
    //     noResults: function (term) {
    //       typed = $(".select2-search__field").val();
    //     },
    //   },
    // });
    // $(".customer-select").on("select2:select", function (e) {
    //   typed = ""; // clear
    // });
    $(".edit-customer").click(function () {
      $("#show-customer").modal("hide");
      $("#edit-customers").modal("show");
    });
  }

  // console.log($(".select2-search__field"));

  // Allow searching customer directly on database
  $('.customer-select').select2({
    placeholder: "Sélectionner client",
    allowClear: true,
    "language": {
      "noResults": function () {
        const noResultsFoundHTML = `
            <div class="d-flex align-items-center" style="gap: 1rem;"> 
              <i class="fa fa-search" aria-hidden="true"></i>
              <span class="text-sm"> 
                <strong class="text-sm">
                  Aucun résultat trouvé. <br> 
                </strong>
                <span style="display: block; width: 100%; height: 1px; background: #fff; margin: 6px 0 6px 0;"></span>
                Veuillez taper 
                <strong class="text-sm"> le nom <span class="text-warning text-sm">exact</span> du client </strong> 
              </span>
            </div>
          `

        return noResultsFoundHTML;
      }
    },
    escapeMarkup: function (markup) {
      return markup;
    },
    ajax: {
      type: 'POST',
      url: '/home/search-customer/',
      dataType: 'json',
      delay: 250,
      data: function (params) {
        const query =
          params.term && params.term.trim() !== ""
            ? { term: params.term, csrfmiddlewaretoken: csrftoken }
            : { csrfmiddlewaretoken: csrftoken };

        return query;
      },
      processResults: function (data) {
        // console.log(data);
        return {
          results: $.map(data, function (item) {
            return {
              text: `${item.intitule} (${item.id})`,
              id: item.id
            }
          })
        };
      },
    }
  });
});

/*************************
 * ALLOW CHANGING CLIENT *
 *************************/
$(document).ready(function () {
  var typed = "";
  if ($(".customer-modification-selection").length > 0) {
    $(".customer-modification-selection").select2({
      placeholder: "Sélectionner client",
      allowClear: true,
      "language": {
        "noResults": function () {
          const noResultsFoundHTML = `
              <div class="d-flex align-items-center" style="gap: 1rem;"> 
                <i class="fa fa-search" aria-hidden="true"></i>
                <span class="text-sm"> 
                  <strong class="text-sm">
                    Aucun résultat trouvé. <br> 
                  </strong>
                  <span style="display: block; width: 100%; height: 1px; background: #fff; margin: 6px 0 6px 0;"></span>
                  Veuillez taper 
                  <strong class="text-sm"> le nom <span class="text-warning text-sm">exact</span> du client </strong> 
                </span>
              </div>
            `

          return noResultsFoundHTML;
        },
      },
      escapeMarkup: function (markup) {
        return markup;
      },
      ajax: {
        type: 'POST',
        url: '/home/search-customer/',
        dataType: 'json',
        delay: 250,
        data: function (params) {
          const query =
            params.term && params.term.trim() !== ""
              ? { term: params.term, csrfmiddlewaretoken: csrftoken }
              : { csrfmiddlewaretoken: csrftoken };

          return query;
        },
        processResults: function (data) {
          // console.log(data);
          return {
            results: $.map(data, function (item) {
              return {
                text: `${item.intitule} (${item.id})`,
                id: item.id
              }
            })
          };
        }
      }
    });

    const selectSelect2Container =
      document.querySelectorAll(".select2-container");
    const spanSelect2Selection = document.querySelectorAll("span.selection");

    if (selectSelect2Container != null) {
      selectSelect2Container.forEach((select, index) => {
        if (selectSelect2Container.length > 1) {
          selectSelect2Container[1].setAttribute(
            "style",
            "display: block !important;"
          );
        } else {
          selectSelect2Container[index].setAttribute(
            "style",
            "display: block !important;"
          );
        }
      });

      spanSelect2Selection.forEach((span, index) => {
        if (spanSelect2Selection.length > 1) {
          spanSelect2Selection[1].setAttribute(
            "style",
            "display: block !important;"
          );
        }
        spanSelect2Selection[index].setAttribute(
          "style",
          "display: block !important;"
        );
      });
    }
  }
});

const customerModificationSelectionList = document.getElementById(
  "customerModificationSelectionList"
);
const buttonModifySelectedClient = document.getElementById(
  "buttonModifySelectedClient"
);
const buttonModifyCustomer = document.querySelectorAll("#buttonModifyCustomer");

let oldCustomerId = 0;

if (buttonModifyCustomer != null) {
  buttonModifyCustomer.forEach((button) => {
    button.classList.remove("d-flex");
    button.classList.add("d-none");
    button.addEventListener("click", (e) => {
      oldCustomerId = e.target.getAttribute("data-customer-id");
    });
  });
}

if (buttonModifySelectedClient != null) {
  buttonModifySelectedClient.addEventListener("click", (e) => {
    e.preventDefault();

    let newCustomerId = customerModificationSelectionList.value;
    let pnrId = buttonModifySelectedClient.getAttribute("data-pnr-id");

    $.ajax({
      type: "POST",
      url: "/home/pnr/modify-customer-in-passenger-invoice/",
      dataType: "json",
      data: {
        OldCustomerId: oldCustomerId,
        NewCustomerId: newCustomerId,
        PnrId: pnrId,
        csrfmiddlewaretoken: csrftoken,
      },
      success: (response) => {
        console.log(response);

        console.log(response.pnrIssuedUpdated, response.pnrNotIssuedUpdated);

        $("#modifySelectedClient").modal("hide");

        if (
          response.pnrIssuedUpdated &&
          response.pnrNotIssuedUpdated == undefined
        ) {
          toastr.info("Le client a été modifié avec succès!");

          setTimeout(() => {
            window.location.reload();
          }, 700);
        } else if (
          !response.pnrIssuedUpdated &&
          response.pnrNotIssuedUpdated == undefined
        ) {
          toastr.error("Le client a déja une commande!");
        }

        if (
          response.pnrNotIssuedUpdated &&
          response.pnrIssuedUpdated == undefined
        ) {
          toastr.info("Le client a été modifié avec succès!");

          setTimeout(() => {
            window.location.reload();
          }, 700);
        } else if (
          !response.pnrNotIssuedUpdated &&
          response.pnrIssuedUpdated == undefined
        ) {
          toastr.error("Le client a déja un devis!");
        }
      },
      error: (response) => {
        console.log(response);
      },
    });
  });
}
/************************************
 * END OF ALLOWING TO CHANGE CLIENT *
 ************************************/

//span to input
/*var switchToInput = function () {
  var $input = $("<input>", {
      val: $(this).text(),
      type: "text",
      class: "form-control form-control-sm p-0",
      rel : $(this).text(),
  });
  $input.addClass("montant");
  $(this).replaceWith($input);
  $input.on("blur", switchToSpan);
  $input.select();
};
var switchToSpan = function () {
  if($(this).val()){
      var $text = $(this).val();
  } else {
      var $text = $(this).attr('rel');
  }
  var $span = $("<span>", {
      text: $text,
  });
  $span.addClass("montant");
  $(this).replaceWith($span);
  $span.on("click", switchToInput);
}
$(".montant").on("click", switchToInput);
*/

// /* 2 nt*/
// $('input[type="text"]#nt').on('change', function () {
//   var texInputValue = $('#nt').val();
//   if (texInputValue != "") {
//     $('#bne').append(texInputValue);
//     //$('#nt').val("");
//   }
//   else if (texInputValue == "") {
//     $('#pnr').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TQT/T");
//   }
// });
// /* 3 nlbe*/
// $('input[type="text"]#nlbe').on('change', function () {
//   var texInputValue = $('#nlbe').val();
//   if (texInputValue != "") {
//     $('#be').append(texInputValue);
//     //$('#nlbe').val("");
//   }
//   else if (texInputValue == "") {
//     $('#be').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/TWD/L");
//   }
// });
// /* 4 nlse*/
// $('input[type="text"]#nlse').on('change', function () {
//   var texInputValue = $('#nlse').val();
//   if (texInputValue != "") {
//     $('#se').append(texInputValue);
//     //$('#nlse').val("");
//   }
//   else if (texInputValue == "") {
//     $('#se').text("WM/FWD/EML ISSOUFALI.PNR@GMAIL.COM/EWD/L");
//   }
// });

//next prev pnr details
// var idpnr = $('#pnr_id').data("id");
// // var linkdev='http://127.0.0.1:8000/home/pnr/';
// var linkprod = 'http://5.135.136.201:8000/home/pnr/';
// function increment() {
//   idpnr++;
//   location.href = linkprod + idpnr++;
// }
// function decrement() {
//   idpnr--;
//   location.href = linkprod + idpnr--;
// }

// $(function () {
//   var $table = $('#all-pnr');
//   $table.tablesorter({
//     widgets: ['zebra', 'columns', 'stickyHeaders'],
//   });
//   $table.on('pagerInitialized pagerComplete', function (e, c) {
//     var i, pages = '', t = [],
//       cur = c.page + 1,
//       start = cur > 1 ? (c.totalPages - cur < 3 ? -3 + (c.totalPages - cur) : -1) : 0,
//       end = cur < 3 ? 5 - cur : 2;
//     for (i = start; i < end; i++) {
//       if (cur + i >= 1 && cur + i < c.totalPages) { t.push(cur + i); }
//     }
//     // make sure first and last page are included in the pagination
//     if ($.inArray(1, t) === -1) { t.push(1); }
//     if ($.inArray(c.totalPages, t) === -1) { t.push(c.totalPages); }
//     // sort the list
//     t = t.sort(function (a, b) { return a - b; });
//     // make links and spacers
//     $.each(t, function (j, v) {
//       pages += '<a  class="' + (v === cur ? 'current' : '') + '">' + v + '</a>';
//       pages += j < t.length - 1 && (t[j + 1] - 1 !== v) ? ' ... ' : (j >= t.length - 1 ? '' : ' | ');
//     });
//     $('.pagecount').html(pages);
//   })
//     .tablesorter({
//       widgets: ['zebra', 'columns', 'stickyHeaders'],
//     })
//     .tablesorterPager({
//       container: $(".pager"),
//       size: 50
//     });
//   // set up pager controls
//   $('.pager .left a').on('click', function () {
//     $(this)
//       .addClass('current')
//       .siblings()
//       .removeClass('current');
//     $table.trigger('pageSize', $(this).html());
//     return false;
//   });
//   $('.pager .right .pagecount').on('click', 'a', function () {
//     $(this)
//       .addClass('current')
//       .siblings()
//       .removeClass('current');
//     $table.trigger('pageSet', $(this).html());
//     $('html, body').animate({scrollTop:0}, '300');
//     return false;
//   });
// });

// function isDate(testDate){
//   var myDate = new Date(testDate);
//   var blMyResult = myDate instanceof Date && !isNaN(myDate.valueOf());
//   return blMyResult;
// }
// var thIndex = 0, curThIndex = null;
// $(document).on('click', '#all-pnr thead tr th', function () {
//   var tblId = '#' + $(this).closest('table').attr('id');
//   sorting = [];
//   thIndex = $(this).index();
//   tbodyHtml = null;
//   $(tblId + ' tbody tr.pnr-class').each(function () {
//     sorting.push([$(this).index(), $(this).children('td').eq(thIndex).html()]);
//   });
//   if (thIndex != curThIndex) {
//     curThIndex = thIndex;
//     sorting = sorting.sort(
//       function (a, b) {
//         if (isNaN(a[1].replace(",", "")) == false && isNaN(b[1].replace(",", "")) == false) {
//           return a[1].replace(",", "") - b[1].replace(",", "");
//         }
//         else if (isDate(a[1]) && isDate(b[1])) {
//           var xDate = new Date(a[1]);
//           var yDate = new Date(b[1]);
//           if (xDate < yDate) {
//             return -1;
//           }
//           if (xDate > yDate) {
//             return 1;
//           }
//           return 0;
//         }
//         else {
//           if (a[1] < b[1]) {
//             return -1;
//           }
//           if (a[1] > b[1]) {
//             return 1;
//           }
//           return 0;
//         }
//       }
//     );
//   }
//   else {
//     sorting = sorting.reverse();
//   }
//   sortIt(sorting, tblId);
// });

// function sortIt(sorting, tblId){
//   //this loop consumes most of the processing/wait time
//   for(var i = 0; i < sorting.length; i++){
//     rowId = sorting[i][0]; //get original row number of record
//     tbodyHtml += $(tblId + ' tbody tr').eq(rowId)[0].outerHTML;
//   }

//   $( tblId + ' tbody').html(tbodyHtml);

//   //var x = new Date();
//   //console.log("finish sort: " + x.toTimeString());
// }

// Fermer le modal quand 'echap' est cliqué
$("body").keyup(function (e) {
  if (e.keyCode == 27) {
    $(".modal").modal("hide");
  }
});

// Activer le button si le champ n'est pas vide
$(document).ready(function () {
  $(".comment-detected-anomaly").on("input change", function () {
    if ($(this).val().trim() != "") {
      $("#send-comment").prop("disabled", false);
    } else {
      $("#send-comment").prop("disabled", true);
    }
  });
});

$("#spinnerLoadingSearch").hide();
$("#buttonShowPnrBySizeOnSearch").hide();
$("#all-pnr-after-search").hide();


$(function () {
  $("#all-pnr-after-search").tablesorter({
    headers: {
      ".dateCreationOrderClass": {
        sorter: false,
      },
      ".pnr-issuing-date": {
        sorter: "customDateParser",
      },
      ".pnr-creator-list-after-search": {
        sorter: false,
      },
    },
    widgets: ["zebra", "columns", "stickyHeaders"],
  });
});

let PAGE_SIZE = $("input[name='paginate_by']").val() || 50;

const dateCreationOrder = document.querySelector("#dateCreationOrder");
let isDateOrderByAsc = false;
let isDateOrderByChecked = false;
let isSortedByCreator = false;

/* A function that is called when the user clicks on the button "Show PNR by size on search". */
$("#buttonShowPnrBySizeOnSearch").on("click", function () {
  let sizeInput = parseInt($("input[name='paginate_by']").val()) || 0;
  let pageSizeByDefault =
    parseInt($("#pnrCounterOnSearch").val().split("/")[1].trim()) || 0;

  if (sizeInput > pageSizeByDefault) {
    $("input[name='paginate_by']").val(pageSizeByDefault);
  }

  PAGE_SIZE = $("input[name='paginate_by']").val();
  searchFunction(PAGE_SIZE, isDateOrderByAsc, isDateOrderByChecked, isSortedByCreator);
});

const icon__pnrDateCreationSearch = document.querySelector("#icon__pnrDateCreationSearch");

$(document).ready(function () {
  $("#dateCreationOrder").on("click", function (e) {
    isDateOrderByAsc === true
      ? (isDateOrderByAsc = false)
      : (isDateOrderByAsc = true);

    isDateOrderByChecked = true;

    isDateOrderByAsc
      ? localStorage.setItem('isOrderedByDateCreatedSearch', "true")
      : localStorage.setItem('isOrderedByDateCreatedSearch', "false")

    localStorage.setItem('isSortedByCreatorSearch', null)

    const isOrderedByDateCreated = localStorage.getItem('isOrderedByDateCreatedSearch')

    if (isOrderedByDateCreated === "false") {
      $("#icon__pnrDateCreationSearch").removeClass("fa-arrows-up-down");
      $("#icon__pnrDateCreationSearch").removeClass("fa-arrow-up");
      $("#icon__pnrDateCreationSearch").addClass("fa-arrow-down");
    } else if (isOrderedByDateCreated === "true") {
      $("#icon__pnrDateCreationSearch").removeClass("fa-arrows-up-down");
      $("#icon__pnrDateCreationSearch").removeClass("fa-arrow-down");
      $("#icon__pnrDateCreationSearch").addClass("fa-arrow-up");
    }

    searchFunction(PAGE_SIZE, isDateOrderByAsc, isDateOrderByChecked, null);
  });
});

$(document).ready(function () {
  $("#creatorSorter").on("click", function (e) {
    isSortedByCreator === true
      ? (isSortedByCreator = false)
      : (isSortedByCreator = true);

    isSortedByCreator
      ? localStorage.setItem('isSortedByCreatorSearch', 'asc')
      : localStorage.setItem('isSortedByCreatorSearch', 'desc')

    localStorage.setItem('isOrderedByDateCreatedSearch', null)

    const isSortedByCreatorStorage = localStorage.getItem('isSortedByCreatorSearch')

    if (isSortedByCreatorStorage === 'asc') {
      $("#icon__pnrCreatorSearch").removeClass("fa-arrows-up-down");
      $("#icon__pnrCreatorSearch").removeClass("fa-arrow-up");
      $("#icon__pnrCreatorSearch").addClass("fa-arrow-down");
    } else if (isSortedByCreatorStorage === 'desc') {
      $("#icon__pnrCreatorSearch").removeClass("fa-arrows-up-down");
      $("#icon__pnrCreatorSearch").removeClass("fa-arrow-down");
      $("#icon__pnrCreatorSearch").addClass("fa-arrow-up");
    }

    searchFunction(PAGE_SIZE, null, false, isSortedByCreator);
  });
})

function searchFunction(pageSize, isDateOrderByAsc, isDateOrderByChecked, isSortByCreator) {
  console.log('====================================');
  console.log({
    isDateOrderByAsc: isDateOrderByAsc,
    isDateOrderByChecked: isDateOrderByChecked,
    isSortByCreator: isSortByCreator
  });
  console.log('====================================');

  var pnr_research = $("#input-pnr").val().toLowerCase();
  if (pnr_research.trim() != "") {
    $("#spinnerLoadingSearch").show();
    $.ajax({
      type: "POST",
      url: "/home/pnr_research",
      dataType: "json",
      data: {
        pnr_research: pnr_research,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (data) {
        let SEARCH_RESULT = data.pnr_result;

        if (SEARCH_RESULT.length > 0) {
          document.querySelector(".tbody-pnr-after-search").innerHTML = "";

          $("#all-pnr-after-search").show();
          $("#buttonShowPnrBySize").hide();
          $("#buttonShowPnrBySizeOnSearch").show();
          $("#initialPagination").hide();
          $("#spinnerLoadingSearch").hide();

          function invalidDateToJsStringDate(dateToParse) {
            const dateString = dateToParse;
            const dateParts = dateString.split(/[\s/:]+/); // Divise la chaîne en une liste de valeurs
            const year = parseInt(dateParts[2]);
            const month = parseInt(dateParts[1]) - 1; // Les mois sont indexés à partir de 0, donc soustraire 1
            const day = parseInt(dateParts[0]);
            const hour = parseInt(dateParts[3]);
            const minute = parseInt(dateParts[4]);
            const date = new Date(year, month, day, hour, minute);
            return date;
          }

          function pnrSortedByCreator(isSortByCreator) {
            if (isSortByCreator) {
              SEARCH_RESULT.sort((a, b) => {
                return a.agent.localeCompare(b.agent);
              });
            } else {
              SEARCH_RESULT.sort((a, b) => {
                return b.agent.localeCompare(a.agent);
              });
            }
          }

          function dateCreationOrderByAsc(isDateOrderByAsc) {
            if (isDateOrderByAsc) {
              SEARCH_RESULT.sort((a, b) => {
                const dateA = invalidDateToJsStringDate(a.system_creation_date);
                const dateB = invalidDateToJsStringDate(b.system_creation_date);
                return dateA - dateB;
              });
            } else {
              SEARCH_RESULT.sort((a, b) => {
                const dateA = invalidDateToJsStringDate(a.system_creation_date);
                const dateB = invalidDateToJsStringDate(b.system_creation_date);
                return dateB - dateA;
              });
            }
          }

          if (isSortByCreator === null) {
            $("#icon__pnrCreatorSearch").addClass("fa-arrows-up-down");
            $("#icon__pnrCreatorSearch").removeClass("fa-arrow-down");
            $("#icon__pnrCreatorSearch").removeClass("fa-arrow-up");
            dateCreationOrderByAsc(isDateOrderByAsc)
          } else if (isDateOrderByAsc === null) {
            $("#icon__pnrDateCreationSearch").addClass("fa-arrows-up-down");
            $("#icon__pnrDateCreationSearch").removeClass("fa-arrow-down");
            $("#icon__pnrDateCreationSearch").removeClass("fa-arrow-up");
            pnrSortedByCreator(isSortByCreator)
          }

          $(".request-pnr-counter").text(SEARCH_RESULT.length);
          $("#pnrCounterOnSearch").val(" / " + SEARCH_RESULT.length);

          let countPnrInvoiced = 0;
          let countPnrNotInvoiced = 0;

          SEARCH_RESULT.forEach((pnr) => {
            if (pnr.is_invoiced) {
              countPnrInvoiced++;
            }
            if (!pnr.is_invoiced) {
              countPnrNotInvoiced++;
            }
          });

          let pnrAfterSearch = SEARCH_RESULT.map((pnr, index) => {
            return { id: pnr.id, position: index, number: pnr.number };
          });

          localStorage.setItem(
            "pnrAfterSearch",
            JSON.stringify(pnrAfterSearch)
          );

          $("tbody.tbody-pnr").remove();
          $("#all-pnr").remove();
          $("#all-pnr-after-search").show();

          var options = {
            dataSource: SEARCH_RESULT, // La source de données pour la pagination (ici, les lignes de la table)
            pageSize: pageSize || 50, // Le nombre de résultats par page
            locator: "items",
            showGoInput: true,
            showGoButton: true,
            showNavigator: true,
            formatNavigator:
              "<%= rangeStart %> - <%= rangeEnd %> sur <%= totalNumber %> résultat(s)",
            callback: function (data, pagination) {
              // La fonction de rappel pour mettre à jour les résultats affichés
              var html = "";
              $.each(data, function (index, pnr) {
                // Boucle pour générer le HTML des résultats
                let invoice_class = pnr.is_invoiced ? "tr-invoiced" : "";

                let isEven = index % 2 === 0 ? "odd" : "even";

                let state_class =
                  pnr.state == 1
                    ? "tr-danger"
                    : pnr.state == 2
                      ? "tr-warning"
                      : "";

                let read_class =
                  pnr.is_read != 1 ? "non-lue" : pnr.is_read == 1 ? "lue" : "";

                let pnr_state =
                  pnr.state == 2
                    ? '<span class="tooltips state_2 float-right" tooltip="" tooltip-position="top" tooltip-type="warning"><i class="fa fa-exclamation-triangle warning"></i></span>'
                    : pnr.state == 1
                      ? '<span class="tooltips state_1 float-right" tooltip="" tooltip-position="top" tooltip-type="danger"><i class="fa fa-exclamation-triangle text-danger"></i></span>'
                      : pnr.state == 0
                        ? "<span></span>"
                        : "";

                let pnrAgencyName =
                  pnr.agency.split(":")[0] == ""
                    ? "Aéroport"
                    : pnr.agency.split(":")[0];

                let pnrAgencyCode =
                  pnr.agency.split(":")[1] == undefined
                    ? ""
                    : pnr.agency.split(":")[1];

                html += `
                  <tr 
                    class="pnr-class ${state_class} ${invoice_class} ${read_class} ${isEven}" 
                    onclick="location.href='/home/pnr/${pnr.id}/'" 
                    style="cursor: pointer;" 
                    data-status="${pnr.status_value}" 
                    id="trAllPnr" 
                    data-pnr-id="${pnr.id}" 
                    data-pnr-invoice="${pnr.is_invoiced}" 
                    role="row"
                  >
                    <td> 
                      ${pnr.number} 
                      ${pnr_state}   
                    </td>             
                    <td>
                      <span class="text-uppercase contact">
                        ${pnr.passenger_name || ""}
                      </span>
                      <span class="text-capitalize contact">
                        ${pnr.passenger_surname || ""}
                      </span>
                    </td>
                    <td> ${pnr.customer || ""} </td>
                    <td> ${pnr.system_creation_date} </td>
                    <td> ${pnr.ticket_issuing_date} </td>
                    <td>
                      <span class="montant">
                        ${pnr.total}
                      </span>
                    </td>
                    <td> ${pnr.status} </td>
                    <td> ${pnr.opc} </td>
                    <td> ${pnr.type} </td>
                    <td> ${pnr.agent} </td>
                    <td> ${pnr.pnr_emitter} </td>
                    <td> ${pnrAgencyName} </td>
                    <td> ${pnrAgencyCode} </td>
                  </tr>
                `;
              });
              $("tbody.tbody-pnr-after-search").html(html); // Mise à jour du contenu de la table
              $("#all-pnr-after-search tbody").html(html).trigger("update");
            },
          };

          $("#pagination").pagination(options); // Initialisation de la pagination avec les options définies

          if (pnrFilteredByOrder != null) {
            for (let i = 0; i < pnrFilteredByOrder.options.length; i++) {
              let option = pnrFilteredByOrder.options[i];
              option.removeAttribute("selected");
              if (countPnrInvoiced > 0 && countPnrNotInvoiced > 0) {
                if (option.getAttribute("value") == "None") {
                  option.setAttribute("selected", true);
                }
              }
              if (countPnrInvoiced > 0 && countPnrNotInvoiced < 1) {
                if (option.getAttribute("value") == "True") {
                  option.setAttribute("selected", true);
                }
              }
              if (countPnrInvoiced < 1 && countPnrNotInvoiced > 0) {
                if (option.getAttribute("value") == "False") {
                  option.setAttribute("selected", true);
                }
              }
            }
          }
          if (!isDateOrderByChecked) {
            toastr.options = {
              closeButton: true,
              timeOut: 6000,
              progressBar: true,
              allowHtml: true,
              positionClass: "toast-bottom-right",
            };
            toastr.info(`
              Résultat(s) de la recherche </br>
              PNR envoyé : ${countPnrInvoiced}</br>
              PNR non envoyé : ${countPnrNotInvoiced}
            `);
          }
        } else {
          $("#spinnerLoadingSearch").hide();
          const input__searchPnrValue = $("#input-pnr").val();
          $("#input-pnr").val("");
          toastr.error(
            `Aucun PNR correspondant à la recherche ~ ${input__searchPnrValue} ~`
          );
        }
      },
    });
  } else {
    $("#spinnerLoadingSearch").hide();
    toastr.warning(`La recherche ne doit pas être vide`);
  }
}

// Permet de rechercher un PNR en pressant le clavier "Entrer" avec le clé du code
// $(document).ready(function () {
//   $("#input-pnr").keyup(function (e) {
//     if (e.keyCode == 13) {
//       searchFunction();
//     }
//   });
// });

//====== PNR SEARCH BY NUMBER IN DETAILS PNR =======//
const inputSearchByPnrNumber = document.getElementById(
  "inputSearchByPnrNumber"
);
const buttonPnrSearchByPnrNumber = document.getElementById(
  "buttonPnrSearchByPnrNumber"
);

if (buttonPnrSearchByPnrNumber != null) {
  let pnrNumber = [];
  buttonPnrSearchByPnrNumber.setAttribute("disabled", true);

  inputSearchByPnrNumber.addEventListener("input", (e) => {
    pnrNumber = e.target.value.toUpperCase();
    inputSearchByPnrNumber.value = pnrNumber;

    if (pnrNumber.length < 6) {
      buttonPnrSearchByPnrNumber.setAttribute("disabled", true);
    } else {
      buttonPnrSearchByPnrNumber.removeAttribute("disabled");
    }
  });

  buttonPnrSearchByPnrNumber.addEventListener("click", () => {
    searchPnrByNumber(pnrNumber);
  });

  $("#inputSearchByPnrNumber").keyup(function (e) {
    if (e.keyCode == 13) {
      searchPnrByNumber(pnrNumber);
    }
  });
}
//======== END OF PNR SEARCH BY NUMBER =========//

//====== PNR SEARCH BY PAGE NUMBER  =======//
const input__setPageNumber = document.getElementById("input__setPageNumber");
const button__navigateToPageNumber = document.getElementById(
  "button__navigateToPageNumber"
);
const lastPageNumber = $("#lastPageNumber").data("page-number");
$("#input__setPageNumber").val("");
$("#input__setPageNumber").keypress(function (evt) {
  return /^[0-9]*\.?[0-9]*$/.test($(this).val() + evt.key);
});
if (button__navigateToPageNumber != null) {
  $("#button__navigateToPageNumber").attr("disabled", true);
  let pageNumber = 0;
  input__setPageNumber.addEventListener("input", (e) => {
    pageNumber = e.target.value;
    if (pageNumber.length > 0 && pageNumber > 0) {
      $("#button__navigateToPageNumber").removeAttr("disabled");
    } else {
      $("#button__navigateToPageNumber").attr("disabled", true);
    }
  });
  $("#button__navigateToPageNumber").click(() => {
    $("#input__setPageNumber").val("");
    var path=window.location.pathname;
    if (pageNumber > 0 && pageNumber <= lastPageNumber) {
      window.location.href = `${path}?page=${pageNumber}`;
    } else {
      toastr.error(`Aucun numéro de page de ${pageNumber}`);
      $("#button__navigateToPageNumber").attr("disabled", true);
    }
  });
  $("#input__setPageNumber").keyup(function (e) {
    if (e.keyCode == 13) {
      $("#input__setPageNumber").val("");
      var path = window.location.pathname;

      if (pageNumber > 0 && pageNumber <= lastPageNumber) {
        window.location.href = `${path}?page=${pageNumber}`;
      } else {
        toastr.error(`Aucun numéro de page de ${pageNumber}`);
        $("#button__navigateToPageNumber").attr("disabled", true);
      }
    }
  });
}
//======== END OF PNR SEARCH BY PAGE NUMBER  =========//

//======= Selected PNR Local Storage ========//

// Récuperer les valeurs de l'url
const currentUrl = window.location.href;

// Récuperer toutes les PNR
const AllPnr = document.querySelectorAll("#trAllPnr"); // retourne un NodeList

// Convertir les données en listes
const convertNodeListToArray = Array.from(AllPnr);

// Récuperer l'id pour chaque pnr
const pnrIds = convertNodeListToArray.map((pnr) => pnr.dataset.pnrId);

// Ajouter les données si pnrIds est un objet et sa taille est supérieure à 0
if (typeof pnrIds === "object" && pnrIds.length > 0) {
  localStorage.setItem("pnrIds", JSON.stringify(pnrIds));
}

// Récuperer l'id du pnr passé dans l'url
if (currentUrl.includes("/home/pnr/")) {
  let id = currentUrl.split("/")[5];
  const localStoragePnrIds = localStorage.getItem("pnrIds");

  if (localStoragePnrIds != null) {
    // Ajouter au local storage l'id du pnr séléctionnée
    if (JSON.parse(localStoragePnrIds).includes(id)) {
      localStorage.setItem("pnrIdSelected", id);
    }
  }
}

// Ajouter une class 'text-primary' au pnr séléctionnée
AllPnr.forEach((pnr) => {
  if (pnr.dataset.pnrId == localStorage.getItem("pnrIdSelected")) {
    const pnrChildTd = pnr.children;

    if (
      pnr.getAttribute("data-passenger-invoiced") == "True" &&
      pnr.getAttribute("data-pnr-invoice") == "True"
    ) {
      for (var i = 0; i < pnrChildTd.length; i++) {
        pnrChildTd[i].classList.add("bg-success");
      }
    } else {
      for (var i = 0; i < pnrChildTd.length; i++) {
        pnrChildTd[i].classList.add("bg-secondary");
      }
    }
  }
});

//======= END Selected PNR Local Storage ========//

// Hide input value on focus #valuePagination
// $(document).ready(function() {
//   $('#placeholderPagination').hide();
//   $('#pnrCountDisabled').hide();

//   $("#valuePagination").focus(function () {
//     $('#valuePagination').hide();
//     $('#placeholderPagination').show();
//     $('#pnrCountDisabled').show();
//   })
// })

// All required inputs
let customerCodePostal = document.querySelector("#customer-code-postal-input");
let selectCustomerCodePostal = document.querySelector(
  "select#customer-code-postal-input"
);
let inputCustomerVille = document.querySelector(
  "input#customer-city-int-input"
);
let selectCustomerVille = document.querySelector(
  "select#customer-city-int-input"
);
let inputCustomerDepartement = document.querySelector(
  "input#customer-departement-input"
);
let selectCustomerDepartement = document.querySelector(
  "select#customer-departement-input"
);
let customerCountry = document.querySelector("#customer-country-int-input");

if (
  selectCustomerVille != null &&
  selectCustomerDepartement != null &&
  selectCustomerCodePostal != null
) {
  selectCustomerVille.hidden = true;
  selectCustomerDepartement.hidden = true;
  selectCustomerCodePostal.hidden = true;
}

// Initialize customers input
const initializeCustomerInput = () => {
  customerCodePostal.classList.remove("is-invalid");
  customerCodePostal.classList.remove("is-valid");
  customerCodePostal.hidden = false;
  customerCodePostal.innerHTML = "";
  selectCustomerCodePostal.hidden = true;
  selectCustomerCodePostal.innerHTML = "";
  selectCustomerVille.hidden = true;
  selectCustomerVille.innerHTML = "";
  inputCustomerVille.hidden = false;
  inputCustomerVille.innerHTML = "";
  selectCustomerDepartement.hidden = true;
  selectCustomerDepartement.innerHTML = "";
  inputCustomerDepartement.hidden = false;
  inputCustomerDepartement.innerHTML = "";
};
//=================== MODAL CUSTOMER CREATION =================//

//====> We loads all country <=====//
if (customerCountry != null) {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/home/get-all-coutries/",
    success: (response) => {
      response.map((country) => {
        // We set France country by default
        // And loads all other country
        customerCountry.innerHTML += `
          <option value="${country.name}" ${country.name == "France" ? 'selected="true"' : ""
          }> ${country.name} </option>
        `;
      });
    },
    error: (response) => {
      console.log(response);
    },
  });
}
//====> End of loads all country <=====//

/*
  ===> We loads all departments
  ===> And set "Mayotte" by default departments
*/
if (selectCustomerDepartement != null) {
  selectCustomerDepartement.hidden = false;
  inputCustomerDepartement.hidden = true;
  customerCountry.classList.add("is-valid");

  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/home/get-all-departments/",
    success: (response) => {
      const sortedData = response.sort((a, b) => (a.nom > b.nom ? 1 : -1));
      for (let departement of sortedData) {
        selectCustomerDepartement.classList.remove("is-invalid");
        selectCustomerDepartement.classList.add("is-valid");
        // We set Mayotte department by default
        selectCustomerDepartement.innerHTML += `
          <option value="${departement.code} - ${departement.nom}"> ${departement.nom} </option>
        `;
        for (var i = 0; i < selectCustomerDepartement.options.length; i++) {
          if (
            selectCustomerDepartement.options[i].getAttribute("value") ==
            "976 - Mayotte"
          ) {
            selectCustomerDepartement.options[i].setAttribute("selected", true);
          } else {
            selectCustomerDepartement.options[i].removeAttribute("selected");
          }
        }
      }
    },
    error: (response) => {
      console.log(response);
    },
  });
}
//====> End of loads all departments <=====//

/*
  ===> We loads all cities
  ===> And set "Mayotte" cities by default cities
*/
if (customerCountry != null) {
  const selectCustomerDepartementDefault = () => {
    const mayotteCodeDepartment = "976"

    $.ajax({
      type: "GET",
      dataType: "json",
      url: "/home/get-all-departments/",
      success: (response) => {
        const sortedData = response.sort((a, b) => (a.nom > b.nom ? 1 : -1));
        for (let departement of sortedData) {
          selectCustomerDepartement.classList.remove("is-invalid");
          selectCustomerDepartement.classList.add("is-valid");

          // We set Mayotte department by default
          selectCustomerDepartement.innerHTML += `
            <option value="${departement.code} - ${departement.nom}" ${departement.code == 976 ? "selected='true'" : ""
            }> ${departement.nom} </option>
          `;
        }
      },
      error: (response) => {
        console.log(response);
      },
    });

    // We set all Mayotte cities by default
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/home/get-all-municipalities/",
      data: {
        csrfmiddlewaretoken: getCookies("csrftoken"),
        code_departement: mayotteCodeDepartment,
      },
      success: (response) => {
        if (response.length > 0) {
          selectCustomerDepartement.hidden = false;
          inputCustomerDepartement.hidden = true;

          selectCustomerVille.hidden = false;
          selectCustomerVille.classList.remove("is-invalid");
          selectCustomerVille.classList.add("is-valid");
          inputCustomerVille.hidden = true;

          selectCustomerVille.innerHTML = "";
          customerCodePostal.innerHTML = "";

          for (let commune of response) {
            selectCustomerVille.innerHTML += `
              <option value=${commune.nom}> ${commune.nom} </option>
            `;
          }
        }
      },
      error: (response) => {
        console.log(response);
      },
    });
  };

  selectCustomerDepartementDefault();

  customerCountry.addEventListener("change", (e) => {
    const selectedCountry = "France";

    if (e.target.value == selectedCountry) {
      selectCustomerDepartementDefault();
    } else {
      initializeCustomerInput();
    }
  });
}
//====> End of loads all cities <=====//

if (selectCustomerDepartement != null) {
  selectCustomerDepartement.addEventListener("change", (e) => {
    const DepartementNumber = e.target.value.split(" - ")[0];
    // const DepartementNumber = e.target.value;
    // let url = `https://geo.api.gouv.fr/departements/${DepartementNumber}/communes`;

    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/home/get-all-municipalities/",
      data: {
        csrfmiddlewaretoken: getCookies("csrftoken"),
        code_departement: DepartementNumber,
      },
      success: (response) => {
        if (response.length > 0) {
          selectCustomerDepartement.hidden = false;
          inputCustomerDepartement.hidden = true;

          selectCustomerVille.hidden = false;
          selectCustomerVille.classList.remove("is-invalid");
          selectCustomerVille.classList.add("is-valid");
          inputCustomerVille.hidden = true;

          selectCustomerVille.innerHTML = "";
          customerCodePostal.innerHTML = "";

          for (let commune of response) {
            var optionInputCustomerVille = document.createElement("option");

            optionInputCustomerVille.value = commune.nom;
            optionInputCustomerVille.innerHTML = commune.nom;

            selectCustomerVille.appendChild(optionInputCustomerVille);
            // selectCustomerDepartement.value = `${ville.departement.code} - ${ville.departement.nom}`;
          }
        }
      },
      error: (response) => {
        console.log(response);
      },
    });
  });
}

if (customerCodePostal != null) {
  // Add event listener to the postal code
  customerCodePostal.addEventListener("input", (e) => {
    if (e.target.value.length == 5) {
      let url = `https://geo.api.gouv.fr/communes?codePostal=${e.target.value}&fields=departement`;
      fetch(url).then((response) =>
        response.json().then((data) => {
          if (data.length > 0) {
            customerCodePostal.classList.remove("is-invalid");
            customerCodePostal.classList.add("is-valid");
            customerCountry.value = "France";
            selectCustomerDepartement.hidden = false;
            inputCustomerDepartement.hidden = true;
            selectCustomerVille.hidden = false;
            selectCustomerVille.classList.remove("is-invalid");
            selectCustomerVille.classList.add("is-valid");
            inputCustomerVille.hidden = true;
            selectCustomerDepartement.innerHTML = "";

            for (let ville of data) {
              var optioninputCustomerVille = document.createElement("option");
              optioninputCustomerVille.value = ville.nom;
              optioninputCustomerVille.innerHTML = ville.nom;
              selectCustomerVille.appendChild(optioninputCustomerVille);

              $.ajax({
                type: "GET",
                dataType: "json",
                url: "/home/get-all-departments/",
                success: (response) => {
                  const sortedData = response.sort((a, b) =>
                    a.nom > b.nom ? 1 : -1
                  );

                  for (let departement of sortedData) {
                    selectCustomerDepartement.classList.remove("is-invalid");
                    selectCustomerDepartement.classList.add("is-valid");

                    // We set Mayotte department by default
                    selectCustomerDepartement.innerHTML += `
                      <option 
                        value="${departement.code} - ${departement.nom}" 
                        ${departement.code == ville.departement.code
                        ? "selected='true'"
                        : ""
                      }
                      > 
                        ${departement.nom} 
                      </option>
                    `;
                  }
                },
                error: (response) => {
                  console.log(response);
                },
              });
            }
          }
        })
      );
    } else {
      selectCustomerVille.hidden = true;
      selectCustomerVille.innerHTML = "";
      inputCustomerVille.hidden = false;
      inputCustomerVille.innerHTML = "";
    }
  });
}

// We get postal code and department by city selected
if (selectCustomerVille != null) {
  selectCustomerVille.addEventListener("change", (e) => {
    const selectedCustomerVille = e.target.value;

    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/home/get-all-municipalities/",
      data: {
        csrfmiddlewaretoken: getCookies("csrftoken"),
        nom_departement: selectedCustomerVille,
      },
      success: (response) => {
        // console.log(response)
        if (response.length > 0) {
          try {
            let postalCodeString = response[0].codes_postaux
            const postalCode = postalCodeString.trim().split(',')

            if (postalCode) {
              if (postalCode.length > 0 && postalCode.length < 2) {
                selectCustomerCodePostal.hidden = true;
                customerCodePostal.hidden = false;

                customerCodePostal.value = postalCode;
                customerCodePostal.classList.remove("is-invalid");
                customerCodePostal.classList.add("is-valid");
              } else {
                selectCustomerCodePostal.hidden = false;
                customerCodePostal.hidden = true;
                selectCustomerCodePostal.innerHTML = "";

                postalCode.forEach((code) => {
                  selectCustomerCodePostal.innerHTML += `
                    <option value=${code}> ${code} </option>
                  `;
                  selectCustomerCodePostal.classList.remove("is-invalid");
                  selectCustomerCodePostal.classList.add("is-valid");
                });
              }
            }
          } catch (error) {
            console.log(error);
          }
        }
      },
      error: (response) => {
        console.log(response);
      },
    });
  });
}
//=================== END OF MODAL CUSTOMER CREATION =================>

const spanCustomerDefault = document.querySelector("span#customerDefault");
const returnButton = document.querySelector("a.nav-link.pl-0.pt-0.return");
const alertModalMissingCustomer = document.querySelector(
  "div#alertModalMissingCustomer"
);
const exitModalMissingCustomer = document.querySelector(
  "button#exitModalMissingCustomer"
);

if (returnButton != null) {
  returnButton.removeAttribute("data-target");

  returnButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (spanCustomerDefault == null || spanCustomerDefault.value == "") {
      returnButton.setAttribute("data-target", "#alertModalMissingCustomer");
      exitModalMissingCustomer.addEventListener("click", () => {
        window.history.replaceState({}, "", "/home/");
        window.location.reload();
      });
    } else {
      window.history.replaceState({}, "", "/home/");
      window.location.reload();
    }
  });
}

// $(document).ready(() => {
//   document.querySelector('#test').style.display = "none";
// })

const backNavigationModal = document.querySelector("div#backNavigationModal");
const confirmBackNavigation = document.querySelector("#confirmBackNavigation");
const cancelBackNavigation = document.querySelector("#cancelBackNavigation");
const closeBackNavigation = document.querySelector("#closeBackNavigation");

const noClientModalProcessing = () => {
  backNavigationModal.classList.remove("d-none");
  backNavigationModal.classList.add("d-block");
  backNavigationModal.style.background = "#00000079";

  confirmBackNavigation.addEventListener("click", () => {
    window.history.replaceState({}, "", "/home/");
    window.location.reload();
  });

  cancelBackNavigation.addEventListener("click", () => {
    backNavigationModal.classList.add("d-none");
    backNavigationModal.classList.remove("d-block");
  });

  closeBackNavigation.addEventListener("click", () => {
    backNavigationModal.classList.add("d-none");
    backNavigationModal.classList.remove("d-block");
  });

  document.addEventListener("keyup", (e) => {
    if (e.keyCode == 27) {
      backNavigationModal.classList.add("d-none");
      backNavigationModal.classList.remove("d-block");
    }
  });
};

if (currentUrl.includes("/home/pnr")) {
  if (spanCustomerDefault == null || spanCustomerDefault.value == "") {
    window.history.pushState(null, null, window.location.href);

    window.onpopstate = function () {
      window.history.go(1);
      noClientModalProcessing();
    };

    if (
      document.querySelector(".nav.nav-pills.nav-sidebar.flex-column") != null
    ) {
      let PnrListMenu = document.querySelector(
        ".nav.nav-pills.nav-sidebar.flex-column"
      ).children;

      for (let i = 0; i < PnrListMenu.length; i++) {
        for (let j = 0; j < PnrListMenu[i].children.length; j++) {
          PnrListMenu[i].children[j].addEventListener("click", (e) => {
            e.preventDefault();

            noClientModalProcessing();
          });
        }
      }
    }
  }
}

//==> Button Show and Edit Customer
const buttonShowCustomer = document.querySelectorAll("#buttonShowCustomer");
const buttonEditCustomer = document.querySelector("button.edit-customer");

//==> Modal Show and Edit Customer
const showCustomerModal = document.getElementById("show-customer");
const editCustomerModal = document.getElementById("edit-customers");

//==> Modal Body Show Customer
const modalBodyCustomerIntitule = document.getElementById(
  "modalBodyCustomerIntitule"
);
const modalBodyCustomerEmail = document.getElementById(
  "modalBodyCustomerEmail"
);
const modalBodyCustomerTelephone = document.getElementById(
  "modalBodyCustomerTelephone"
);
const modalBodyCustomerAddressPrimary = document.getElementById(
  "modalBodyCustomerAddressPrimary"
);
const modalBodyCustomerAddressSecondary = document.getElementById(
  "modalBodyCustomerAddressSecondary"
);
const modalBodyCustomerPostalCode = document.getElementById(
  "modalBodyCustomerPostalCode"
);
const modalBodyCustomerCity = document.getElementById("modalBodyCustomerCity");
const modalBodyCustomerDepartement = document.getElementById(
  "modalBodyCustomerDepartement"
);
const modalBodyCustomerCountry = document.getElementById(
  "modalBodyCustomerCountry"
);

//==> Modal Body Edit Customer
const selectedCostumerID = document.querySelector(".selected-customer-id");
const editModalCustomerIntitule = document.getElementById(
  "editModalCustomerIntitule"
);
const editModalCustomerEmail = document.getElementById(
  "editModalCustomerEmail"
);
const editModalCustomerTelephone = document.getElementById(
  "editModalCustomerTelephone"
);
const editModalCustomerAddressPrimary = document.getElementById(
  "editModalCustomerAddressPrimary"
);
const editModalCustomerAddressSecondary = document.getElementById(
  "editModalCustomerAddressSecondary"
);
const editModalCustomerPostalCode = document.getElementById(
  "editModalCustomerPostalCode"
);
const editModalCustomerCity = document.getElementById("editModalCustomerCity");
const editModalCustomerDepartement = document.getElementById(
  "editModalCustomerDepartement"
);
const editModalCustomerCountry = document.getElementById(
  "editModalCustomerCountry"
);

if (buttonShowCustomer != null) {
  buttonShowCustomer.forEach((button) => {
    button.addEventListener("click", () => {
      let id = button.getAttribute("data-customer-id");
      let intitule = button.getAttribute("data-customer-intitule");
      let email = button.getAttribute("data-customer-email");
      let telephone = button.getAttribute("data-customer-telephone");
      let addressPrimary = button.getAttribute("data-customer-address-1");
      let addressSecondary = button.getAttribute("data-customer-address-2");
      let codePostal = button.getAttribute("data-customer-code-postal");
      let city = button.getAttribute("data-customer-city");
      let departement = button.getAttribute("data-customer-departement");
      let country = button.getAttribute("data-customer-country");

      modalBodyCustomerIntitule.textContent = intitule || "Vide";
      modalBodyCustomerEmail.textContent = email || "Vide";
      modalBodyCustomerTelephone.textContent = telephone || "Vide";
      modalBodyCustomerAddressPrimary.textContent = addressPrimary || "Vide";
      modalBodyCustomerAddressSecondary.textContent =
        addressSecondary || "Vide";
      modalBodyCustomerPostalCode.textContent = codePostal || "Vide";
      modalBodyCustomerCity.textContent = city || "Vide";
      modalBodyCustomerDepartement.textContent = departement || "Vide";
      modalBodyCustomerCountry.textContent = country || "Vide";

      buttonEditCustomer.addEventListener("click", () => {
        selectedCostumerID.value = id;
        editModalCustomerIntitule.textContent = intitule;
        editModalCustomerEmail.value = email;
        editModalCustomerTelephone.value = telephone;
        editModalCustomerAddressPrimary.value = addressPrimary;
        editModalCustomerAddressSecondary.value = addressSecondary;
        editModalCustomerPostalCode.value = codePostal;
        editModalCustomerCity.value = city;
        editModalCustomerDepartement.value = departement;
        editModalCustomerCountry.value = country;
      });
    });
  });
}

const customerDefaultOrderPlace = document.querySelectorAll(
  "#customerDefaultOrderPlace"
);
const customerDefaultAll = document.querySelectorAll("#customerDefault");

const ConfirmationCustomerDefaultOrderPlace = document.querySelectorAll(
  "#ConfirmationCustomerDefaultOrderPlace"
);
const ConfirmationCustomerDefault =
  document.querySelectorAll("#customerDefault");
const ConfirmationPassagersCustomer = document.querySelectorAll(
  "#ConfirmationPassagersCustomer"
);

//==> Show only one no duplicated name of customers
$(document).ready(function () {
  const passagersCustomer = document.querySelectorAll("#passagersCustomer");

  let customers = [];
  let removeDuplicatedIndex = [];
  let allIndexs = [];
  let allPassengersItems = [];

  passagersCustomer.forEach((customer, index) => {
    // Get customer name, and the index (position)
    if (customer.outerText != undefined) {
      const customerName = customer.outerText.split("-");
      const customerIndex = index;
      const customerId = customer.getAttribute("data-customer-id");

      // Get all indexs
      allIndexs.push(customerIndex);

      const PASSENGER_INFORMATION = {
        key: customerName[0],
        value: customerName[1],
        clientId: customerId,
      };

      allPassengersItems.push(PASSENGER_INFORMATION);

      // We verify if customer name is not yet in costumers list
      // We add customer name without duplicated value in costumers list
      // We add customer index without duplicated customer name in costumers list
      if (!customers.includes(customerId)) {
        customers.push(customerId);
        removeDuplicatedIndex.push(customerIndex);
      }
    }
  });

  // We filter all duplicated indexs
  let duplicatedIndexs = allIndexs.filter(
    (index) => !removeDuplicatedIndex.includes(index)
  );

  const indexOf = function (value) {
    return this.findIndex((el) => el.value === value);
  };

  Array.prototype.indexOf = indexOf;

  const groupArray = (arr) => {
    const res = [];
    for (let i = 0; i < arr.length; i++) {
      const ind = res.indexOf(arr[i].clientId);

      if (ind !== -1) {
        res[ind].key += `, ${arr[i].key}`;
      } else {
        res.push(arr[i]);
      }
    }
    return res;
  };

  groupArray(allPassengersItems);

  allPassengersItems.forEach((object, index) => {
    if (index != duplicatedIndexs) {
      customerDefaultOrderPlace[index].textContent = object.key;
      customerDefaultAll[index].textContent = object.value;

      customerDefaultOrderPlace.forEach((customer, customerIndex) => {
        customerDefaultOrderPlace[customerIndex].textContent =
          customer.textContent.replaceAll(" - ", "");
      });
    }
  });

  allPassengersItems.forEach((object, index) => {
    if (index != duplicatedIndexs) {
      if (ConfirmationCustomerDefaultOrderPlace[index] != undefined) {
        ConfirmationCustomerDefaultOrderPlace[index].textContent = object.key;
        ConfirmationCustomerDefault[index].textContent = object.value;

        ConfirmationCustomerDefaultOrderPlace.forEach(
          (customer, customerIndex) => {
            ConfirmationCustomerDefaultOrderPlace[customerIndex].textContent =
              customer.textContent.replaceAll(" - ", "");
          }
        );
      }
    }
  });

  // We remove the passager customer <div> on duplicated index
  duplicatedIndexs.forEach((index) => {
    passagersCustomer[index].remove();
  });

  duplicatedIndexs.forEach((index) => {
    if (ConfirmationPassagersCustomer[index] != undefined) {
      ConfirmationPassagersCustomer[index].remove();
    }
  });

  //==> Button hide and show customers processing
  // We get all button for showing and hiding customers
  // const buttonShowAllClient = document.querySelectorAll("#buttonShowAllClient");
  // const buttonHideAllClient = document.querySelectorAll("#buttonHideAllClient");

  // We add toggle function for hiding or showing customer
  // const toggleButtonAllClient = (showAllClient, hideAllClient) => {
  //   if (showAllClient == "visible" && hideAllClient == "hidden") {
  //     buttonShowAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: flex !important');
  //     })

  //     buttonHideAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: none !important');
  //     })
  //   } else if (showAllClient == "hidden" && hideAllClient == "visible") {
  //     buttonShowAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: none !important');
  //     })

  //     buttonHideAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: flex !important');
  //     })
  //   } else {
  //     buttonShowAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: none !important');
  //     })

  //     buttonHideAllClient.forEach((button) => {
  //       button.setAttribute('style', 'display: none !important');
  //     })
  //   }
  // }

  // We hide all buttons on the first page load
  // toggleButtonAllClient("hidden", "hidden")

  // if (removeDuplicatedIndex.length > 1) {
  //   removeDuplicatedIndex.forEach((index) => {
  //     // We hide all index different of the first position (index)
  //     if (index !== 0) {
  //       passagersCustomer[index].setAttribute('style', 'display: none !important');
  //     }

  //     // We show buttonShowAllClient and hide buttonHideAllClient
  //     toggleButtonAllClient("visible", "hidden")

  //     buttonShowAllClient.forEach((button) => {
  //       button.addEventListener("click", () => {
  //         passagersCustomer[index].setAttribute('style', 'display: flex !important');

  //         toggleButtonAllClient("hidden", "visible")
  //       })
  //     })

  //     buttonHideAllClient.forEach((button) => {
  //       button.addEventListener("click", () => {
  //         if (index !== 0) {
  //           passagersCustomer[index].setAttribute('style', 'display: none !important');
  //         }

  //         toggleButtonAllClient("visible", "hidden")
  //       })
  //     })
  //   })
  // }
});

// Email in PNR Details
const detailsContactEmail = document.querySelectorAll("#detailsContactEmail");
const removeDuplicatedContactEmail = document.querySelectorAll(
  "#removeDuplicatedContactEmail"
);

let removeDuplicatedEmail = [];

detailsContactEmail.forEach((detailsEmail, index) => {
  if (detailsEmail.outerText != undefined) {
    let email = detailsEmail.outerText.trim();

    if (!removeDuplicatedEmail.includes(email)) {
      removeDuplicatedEmail.push(email);
    }

    detailsEmail.remove();
  }
});

removeDuplicatedContactEmail.forEach((email, index) => {
  email.setAttribute("style", "display: block !important");
  email.textContent = removeDuplicatedEmail[index];
});

//========= ADD FILTER TO PNR ============>
const pnrFilteredByOrder = document.getElementById("pnrFilteredByOrder");

if (pnrFilteredByOrder != null) {
  for (let i = 0; i < pnrFilteredByOrder.options.length; i++) {
    if (pnrFilteredByOrder.options[i].value == getCookies("filter_pnr")) {
      pnrFilteredByOrder.options[i].setAttribute("selected", true);
    }
  }
  if (pnrFilteredByOrder != null) {
    pnrFilteredByOrder.addEventListener("change", (e) => {
      document.cookie = `filter_pnr=${e.target.value}; SameSite=Lax`
      location.reload()
    })
  }
}
//========= ENF OF ADDING FILTER TO PNR ============>

/**
 * ADD FILTER BY CREATOR TO PNR LIST
 */

const pnrCreatorFilter = document.getElementById("pnrFilteredByCreator");
if (pnrCreatorFilter != null) {
  for (let i = 0; i < pnrCreatorFilter.options.length; i++) {
    if (pnrCreatorFilter.options[i].getAttribute("selected") == "true") {
      document.cookie = `creator_pnr_filter=${pnrCreatorFilter.options[i].value}`;
    }
    if (pnrCreatorFilter.options[i].value == getCookies("creator_pnr_filter")) {
      pnrCreatorFilter.options[i].setAttribute("selected", true);
    }
  }

  pnrCreatorFilter.addEventListener('change', e => {
    document.cookie = `creator_pnr_filter=${e.target.value}; SameSite=Lax`;
    location.reload();
  });
}

/**
 * END OF ADDING FILTER BY CREATOR TO PNR LIST
 */

// ================ Adds a filter to the list of dates created pnr ======================== //
let isOrderedByDateCreated = localStorage.getItem("isOrderedByDateCreated");
const icon__pnrDateCreation = document.getElementById("icon__pnrDateCreation");

$(".pnr-creation-date").click((e) => {
  e.preventDefault();

  // Remove the 'isSortedByCreator' cookie (obsolete code, can be removed)
  Cookies.remove('isSortedByCreator', { path: '/' })

  // Remove the 'isSortedByCreator' value from localStorage
  localStorage.removeItem('isSortedByCreator')

  // Check if the 'isOrderedByDateCreated' value is null
  if (isOrderedByDateCreated == null) {
    // Set 'isOrderedByDateCreated' to false in localStorage
    localStorage.setItem("isOrderedByDateCreated", "false")
    // Set the 'creation_date_order_by' cookie to "asc" with SameSite=Lax attribute
    document.cookie = `creation_date_order_by="asc"; SameSite=Lax`
  } else {
    // Check if 'isOrderedByDateCreated' is currently false
    if (isOrderedByDateCreated == "false") {
      // Set 'isOrderedByDateCreated' to true in localStorage
      localStorage.setItem("isOrderedByDateCreated", "true")
      // Set the 'creation_date_order_by' cookie to "desc" with SameSite=Lax attribute
      document.cookie = `creation_date_order_by="desc"; SameSite=Lax`
    }
    // Check if 'isOrderedByDateCreated' is currently true
    if (isOrderedByDateCreated == "true") {
      // Set 'isOrderedByDateCreated' to false in localStorage
      localStorage.setItem("isOrderedByDateCreated", "false")
      // Set the 'creation_date_order_by' cookie to "asc" with SameSite=Lax attribute
      document.cookie = `creation_date_order_by="asc"; SameSite=Lax`
    }
  }

  // Reload the page to apply the new sorting order
  window.location.reload();
});

if (isOrderedByDateCreated !== null) {
  if (isOrderedByDateCreated == "true") {
    if (icon__pnrDateCreation != null) {
      icon__pnrDateCreation.classList.remove("fa-arrows-up-down");
      icon__pnrDateCreation.classList.remove("fa-arrow-up");
      icon__pnrDateCreation.classList.add("fa-arrow-down");
    }
  }
  if (isOrderedByDateCreated == "false") {
    if (icon__pnrDateCreation != null) {
      icon__pnrDateCreation.classList.remove("fa-arrows-up-down");
      icon__pnrDateCreation.classList.remove("fa-arrow-down");
      icon__pnrDateCreation.classList.add("fa-arrow-up");
    }
  }
} else {
  if (icon__pnrDateCreation != null) {
    icon__pnrDateCreation.classList.add("fa-arrows-up-down");
  }
}
// ================ End of Adding a filter to the list of dates created pnr ======================== //

//========= ADD BUTTON TO SEND PNR NOT UPDATED IN ODOO ============>
const buttonSendPnrNotUpdated = document.getElementById(
  "buttonSendPnrNotUpdated"
);
const messagePnrNotUpdated = document.getElementById("messagePnrNotUpdated");

if (buttonSendPnrNotUpdated != null) {
  buttonSendPnrNotUpdated.setAttribute("disabled", true);

  if (messagePnrNotUpdated != null) {
    messagePnrNotUpdated.addEventListener("input", (e) => {
      if (e.target.value.trim() != "") {
        buttonSendPnrNotUpdated.removeAttribute("disabled");
      } else {
        buttonSendPnrNotUpdated.setAttribute("disabled", true);
      }
    });
  }
}
//========= END ADDING BUTTON TO SEND PNR NOT UPDATED IN ODOO ============>

// =======================HANDLING PNR NOT FETCHED FROM MAIL =======================
if (buttonSendPnrNotUpdated != null) {
  buttonSendPnrNotUpdated.addEventListener("click", (e) => {
    e.preventDefault();
    $("#modalPnrNotUpdated").modal("hide");
    const PnrNumber = document.querySelector("#messagePnrNotUpdated");
    $.ajax({
      type: "POST",
      dataType: "json",
      url: `get-not-fetched-pnr/`,
      data: {
        csrfmiddlewaretoken: csrftoken,
        pnrNumber: PnrNumber.value,
      },
      success: (response) => {
        toastr.info("PNR non remonté signalé.");
      },
      error: (response) => {
        console.log(response);
      },
    });
  });
}

//========================== HANDLING RECEIPT PRINT ==================================>
const buttonPrintReceipt = document.getElementById("buttonPrintReceipt");
const modalCreateReceipt = document.getElementById("modalCreateReceipt");
const buttonModalCheckReceipt = document.getElementById(
  "buttonModalCheckReceipt"
);
const modalCheckReceipt = document.getElementById("modalCheckReceipt");
const pageToPrint = document.getElementById("pageToPrint");
const buttonCreateReceiptDirectly = document.getElementById(
  "buttonCreateReceiptDirectly"
);
let select__modalCreateReceiptOrderNumber = document.getElementById(
  "select__modalCreateReceiptOrderNumber"
);
let div__modalCreateReceiptOrderNumber = document.getElementById(
  "div__modalCreateReceiptOrderNumber"
);

let select__modalCreateReceipt = document.getElementById(
  "select__modalCreateReceipt"
);
let span__customer__modalCheckReceipt = document.getElementById(
  "span__customer__modalCheckReceipt"
);
let span__pnrNumber__modalCheckReceipt = document.getElementById(
  "span__pnrNumber__modalCheckReceipt"
);
let span__issuedDate__modalCheckReceipt = document.getElementById(
  "span__issuedDate__modalCheckReceipt"
);
let span__streetAndCity__modalCheckReceipt = document.getElementById(
  "span__streetAndCity__modalCheckReceipt"
);
let span__stateAndCountry__modalCheckReceipt = document.getElementById(
  "span__stateAndCountry__modalCheckReceipt"
);
let span__phone__modalCheckReceipt = document.getElementById(
  "span__phone__modalCheckReceipt"
);
let span__email__modalCheckReceipt = document.getElementById(
  "span__email__modalCheckReceipt"
);
let span__totalAmountOrder__modalCheckReceipt = document.getElementById(
  "span__totalAmountOrder__modalCheckReceipt"
);
// let span__total__modalCheckReceipt = document.getElementById("span__total__modalCheckReceipt");
let itemsContainer = document.getElementById("itemsContainer");

// const modalCheckReceipt__customer = document.getElementById("modalCheckReceipt__customer");

let dateToday = new Date();
let dateOptions = { month: "long", day: "numeric", year: "numeric" };
let hours =
  dateToday.getHours() < 10 ? `0${dateToday.getHours()}` : dateToday.getHours();
let minutes =
  dateToday.getMinutes() < 10
    ? `0${dateToday.getMinutes()}`
    : dateToday.getMinutes();
let dateHoursForToday = `${dateToday.toLocaleString(
  "fr-FR",
  dateOptions
)}, à ${hours}:${minutes}`;

let convertCanvasToImage = (canvas) => {
  let image = new Image();
  image.src = canvas.toDataURL("image/jpeg", 1.0);
  return image;
};

const convertHtmlToCanvasAndPrintIt = (html, buttonPrint, documentTitle) => {
  window.html2canvas = html2canvas;

  buttonPrint.setAttribute("hidden", "true");

  html2canvas(html).then((canvas) => {
    let img = convertCanvasToImage(canvas);
    img.setAttribute("style", "width: 100% !important");

    var newWindow = window.open("", "_blank");

    if (newWindow) {
      var newBody = newWindow.document.body;
      newBody.style.background = "#fff";
      newBody.appendChild(img);
      newWindow.document.title = `Reçu de paiement du PNR N°${documentTitle}`;

      setTimeout(() => {
        newWindow.print();
        buttonPrint.removeAttribute("hidden");
        newWindow.close();
        $("#modalCheckReceipt").modal("hide");
      }, 100);
    }
  });
};

if (select__modalCreateReceipt != null) {
  const dataAboutCustomers = JSON.parse(
    select__modalCreateReceipt.getAttribute("data-about-customers")
  );
  const dataTotalAmountOrder = JSON.parse(
    select__modalCreateReceipt.getAttribute("data-total-amount-order")
  );
  const pnrNumber = select__modalCreateReceipt.getAttribute("data-pnr-number");

  select__modalCreateReceipt.addEventListener("change", (e) => {
    e.preventDefault();
    let customerId = e.target.value;
    let dataFilteredByCustomerId = dataTotalAmountOrder.filter(
      (customer) => customer.customer_id == customerId
    );
    let dataPnrInvoiceNumbers = [];
    dataFilteredByCustomerId.forEach((data) => {
      let invoiceNumbers = data.pnr_invoice_numbers;
      if (!dataPnrInvoiceNumbers.includes(invoiceNumbers)) {
        dataPnrInvoiceNumbers.push(invoiceNumbers);
      }
    });
    if (
      dataPnrInvoiceNumbers.flat().length < 1 ||
      dataPnrInvoiceNumbers.flat()[0] == ""
    ) {
      div__modalCreateReceiptOrderNumber.classList.add("d-none");
      let dataFilteredByInvoiceNumber = dataTotalAmountOrder.filter(
        (data) => data.customer_id == customerId
      );
      console.log(dataFilteredByInvoiceNumber);
      receiptProcess(
        customerId,
        dataAboutCustomers,
        dataFilteredByInvoiceNumber,
        pnrNumber
      );
    }
    if (
      dataPnrInvoiceNumbers.flat().length > 0 &&
      dataPnrInvoiceNumbers.flat()[0] != ""
    ) {
      div__modalCreateReceiptOrderNumber.classList.remove("d-none");
      buttonModalCheckReceipt.setAttribute("disabled", true);
      select__modalCreateReceiptOrderNumber.innerHTML = "";
      select__modalCreateReceiptOrderNumber.innerHTML = `
        <option selected="true" disabled="true" value="default">Sélectionner le numéro de commande</option>
      `;
      dataPnrInvoiceNumbers.flat().forEach((invoiceNumber) => {
        if (dataPnrInvoiceNumbers.flat().length == 1) {
          select__modalCreateReceiptOrderNumber.innerHTML += `
            <option value="${invoiceNumber}" selected="true">${invoiceNumber}</option>
          `;
        } else {
          select__modalCreateReceiptOrderNumber.innerHTML += `
            <option value="${invoiceNumber}">${invoiceNumber}</option>
          `;
        }
      });
      let optionValue = [];
      if (select__modalCreateReceiptOrderNumber.children.length == 2) {
        let option = select__modalCreateReceiptOrderNumber.children[1];
        let optionTextContent = option.text.trim();
        // On efface tous le éléments dans la liste
        optionValue.splice(0, optionValue.length);
        // On ajoute le nouveau élément dans la liste
        optionValue.push(optionTextContent);
        buttonModalCheckReceipt.removeAttribute("disabled");
        const dataFilteredByInvoiceNumber = dataTotalAmountOrder.filter(
          (data) =>
            data.customer_id == customerId &&
            data.pnr_invoice_numbers[0] == optionValue[0]
        );
        receiptProcess(
          customerId,
          dataAboutCustomers,
          dataFilteredByInvoiceNumber,
          pnrNumber
        );
      } else if (select__modalCreateReceiptOrderNumber.children.length > 2) {
        select__modalCreateReceiptOrderNumber.addEventListener(
          "change",
          (e) => {
            buttonModalCheckReceipt.setAttribute("disabled", true);
            for (
              let i = 0;
              i < select__modalCreateReceiptOrderNumber.children.length;
              i++
            ) {
              let option = select__modalCreateReceiptOrderNumber.children[i];
              let optionTextContent = option.text.trim();
              if (optionTextContent == e.target.value) {
                option.setAttribute("selected", true);
                // On efface tous le éléments dans la liste
                optionValue.splice(0, optionValue.length);
                // On ajoute le nouveau élément dans la liste
                optionValue.push(optionTextContent);
              } else {
                option.removeAttribute("selected");
              }
            }
            const dataFilteredByInvoiceNumber = dataTotalAmountOrder.filter(
              (data) =>
                data.customer_id == customerId &&
                data.pnr_invoice_numbers[0] == optionValue[0]
            );
            receiptProcess(
              customerId,
              dataAboutCustomers,
              dataFilteredByInvoiceNumber,
              pnrNumber
            );
          }
        );
      }
    }
  });

  buttonModalCheckReceipt.setAttribute("disabled", "true");

  if (select__modalCreateReceipt.children.length == 1) {
    buttonModalCheckReceipt.removeAttribute("disabled");
    let customerId =
      select__modalCreateReceipt.children[0].getAttribute("data-customer-id");

    if (buttonCreateReceiptDirectly != null) {
      buttonCreateReceiptDirectly.addEventListener("click", (e) => {
        e.preventDefault();
        receiptProcess(
          customerId,
          dataAboutCustomers,
          dataTotalAmountOrder,
          pnrNumber
        );
        $("#modalCheckReceipt").modal("show");
      });
    }
  }

  select__modalCreateReceipt.addEventListener("change", (e) => {
    e.preventDefault();
    let customerId = e.target.value;
    receiptProcess(
      customerId,
      dataAboutCustomers,
      dataTotalAmountOrder,
      pnrNumber
    );
  });

  if (buttonPrintReceipt != null) {
    buttonPrintReceipt.addEventListener("click", (e) => {
      convertHtmlToCanvasAndPrintIt(pageToPrint, buttonPrintReceipt, pnrNumber);
    });
  }
}

function searchPnrByNumber(value) {
  let currentUrl = document.location.href;
  let splitCurrentUrl = currentUrl.split("/");

  if (value.length >= 6) {
    $.ajax({
      type: "POST",
      url: "/home/pnr_search_by_pnr_number",
      dataType: "json",
      data: {
        PnrNumber: value,
        csrfmiddlewaretoken: csrftoken,
      },
      success: (data) => {
        let newPnrId = data.pnr_id;
        if (newPnrId.length == 0) {
          toastr.error(`Aucun résultat pour ${value}`);
        } else {
          splitCurrentUrl[5] = newPnrId;
          let newUrl = splitCurrentUrl.join("/");
          window.location.href = newUrl;
        }
      },
      error: (data) => {
        console.log(data);
      },
    });
  }
}

function receiptProcess(
  customerId,
  dataAboutCustomers,
  dataTotalAmountOrder,
  pnrNumber
) {
  if (customerId != 0) {
    buttonModalCheckReceipt.removeAttribute("disabled");
  }

  // console.log('====================================');
  // console.log(dataTotalAmountOrder);
  // console.log('====================================');

  const customerData = dataAboutCustomers.filter(
    (customer) => customer.id == customerId
  )[0];
  const valueOfEachFiled = dataTotalAmountOrder.filter(
    (customer) => customer.customer_id == customerId
  )[0];
  const totalAmountOrder = valueOfEachFiled.total;

  const ticket = valueOfEachFiled.ticket;
  const fee = valueOfEachFiled.fee;
  const otherFee = valueOfEachFiled.other_fee;

  span__customer__modalCheckReceipt.textContent = `${customerData.intitule}`;
  span__pnrNumber__modalCheckReceipt.textContent = `#${pnrNumber}`;
  span__issuedDate__modalCheckReceipt.textContent = dateHoursForToday;
  span__streetAndCity__modalCheckReceipt.textContent = `${customerData.address}, ${customerData.city}`;
  span__stateAndCountry__modalCheckReceipt.textContent = `${customerData.country
    }, ${customerData.departement || ""}`;
  span__phone__modalCheckReceipt.textContent = `${customerData.telephone}`;
  span__email__modalCheckReceipt.textContent = `${customerData.email.toLowerCase()}`;
  span__totalAmountOrder__modalCheckReceipt.textContent = `${totalAmountOrder.toFixed(
    2
  )}`;

  itemsContainer.innerHTML = "";

  let ticketCounter = 0;
  let feeCounter = 0;
  let otherFeeCounter = 0;

  const convertToFrenchDate = (dateString) => {
    try {
      // Convert the date string to a JavaScript Date object.
      const date = new Date(dateString);

      // Get the day of the month.
      const day = date.getDate();

      // Get the month name in French.
      const monthNameInFrench = [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre"
      ];

      const monthName = monthNameInFrench[date.getMonth()];

      // Get the year.
      const year = date.getFullYear();

      // Format the date in French.
      const frenchDate = `${day} ${monthName} ${year}`;

      return frenchDate;
    } catch (error) {
      console.log("Erreur dans la conversion de la date " + error);
      return "";
    }
  };

  let ticketDivData = () => {
    if (ticketCounter < ticket.length) {
      itemsContainer.innerHTML += `
        <div class="row item">
          <div class="col-sm-1">${ticket.type[ticketCounter]}</div>
          <div class="col-sm-3">#${ticket.number[ticketCounter]}</div>
          <div class="col-sm-3">${ticket.passenger[ticketCounter]}</div>
          <div class="col-sm-2">${convertToFrenchDate(ticket.issuing_date[ticketCounter])}</div>
          <div class="col-sm-1 text-right">${ticket.transport_cost[
          ticketCounter
        ].toFixed(2)}</div>
          <div class="col-sm-1 text-right">${ticket.tax[ticketCounter].toFixed(
          2
        )}</div>
          <div class="col-sm-1 text-right">${ticket.total[
          ticketCounter
        ].toFixed(2)}</div>
        </div>
      `;
      ticketCounter++;
    }
  };

  let feeDivData = () => {
    if (feeCounter < fee.length) {
      itemsContainer.innerHTML += `
        <div class="row item">
          <div class="col-sm-1">FEE</div>
          <div class="col-sm-3">${fee.type[feeCounter]}</div>
          <div class="col-sm-3"></div>
          <div class="col-sm-2">${convertToFrenchDate(fee.issuing_date[feeCounter])}</div>
          <div class="col-sm-1 text-right">${fee.cost[feeCounter].toFixed(
        2
      )}</div>
          <div class="col-sm-1 text-right">${fee.tax[feeCounter].toFixed(
        2
      )}</div>
          <div class="col-sm-1 text-right">${fee.total[feeCounter].toFixed(
        2
      )}</div>
        </div>
      `;
      feeCounter++;
    }
  };

  let otherFeeDivData = () => {
    if (otherFeeCounter < otherFee.length) {
      itemsContainer.innerHTML += `     
        <div class="row item">
          <div class="col-sm-1">${otherFee.type[otherFeeCounter]}</div>
          <div class="col-sm-3">${otherFee.designation[otherFeeCounter]}</div>
          <div class="col-sm-3">${otherFee.passenger[otherFeeCounter]}</div>
          <div class="col-sm-2">${convertToFrenchDate(otherFee.issuing_date[otherFeeCounter])}</div>
          <div class="col-sm-1 text-right">${otherFee.cost[
          otherFeeCounter
        ].toFixed(2)}</div>
          <div class="col-sm-1 text-right">${otherFee.tax[
          otherFeeCounter
        ].toFixed(2)}</div>
          <div class="col-sm-1 text-right">${otherFee.total[
          otherFeeCounter
        ].toFixed(2)}</div>
        </div>
      `;
      otherFeeCounter++;
    }
  };

  /****************************************************************
   *  TICKET (not empty) + FEE (not empty) + OTHERFEE (not empty) *
   ****************************************************************
   */
  if (ticket.length > 0 && fee.length > 0 && otherFee.length > 0) {
    for (let i = 0; i < ticket.length + fee.length + otherFee.length; i++) {
      ticketDivData();
      feeDivData();
      otherFeeDivData();
    }
  }

  /*****************************************
   *  TICKET (not empty) + FEE (not empty) *
   *****************************************
   */
  if (ticket.length > 0 && fee.length > 0 && otherFee.length < 1) {
    for (let i = 0; i < ticket.length + fee.length; i++) {
      ticketDivData();
      feeDivData();
    }
  }

  /*******************************************
   *  FEE (not empty) + OTHERFEE (not empty) *
   *******************************************
   */
  if (ticket.length < 1 && fee.length > 0 && otherFee.length > 0) {
    for (let i = 0; i < fee.length + otherFee.length; i++) {
      otherFeeDivData();
      feeDivData();
    }
  }

  /*******************************************
   *  TICKET(not empty) + OTHERFEE (not empty) *
   *******************************************
   */
  if (ticket.length > 0 && fee.length < 1 && otherFee.length > 0) {
    for (let i = 0; i < ticket.length + otherFee.length; i++) {
      ticketDivData();
      otherFeeDivData();
    }
  }

  /*************************
   *  TICKET (not empty) *
   *************************
   */
  if (ticket.length > 0 && fee.length < 1 && otherFee.length < 1) {
    for (let i = 0; i < ticket.length; i++) {
      ticketDivData();
    }
  }

  /*************************
   *  FEE (not empty) *
   *************************
   */
  if (ticket.length < 1 && fee.length > 0 && otherFee.length < 1) {
    for (let i = 0; i < fee.length; i++) {
      feeDivData();
    }
  }

  /*************************
   *  OTHERFEE (not empty) *
   *************************
   */
  if (ticket.length < 1 && fee.length < 1 && otherFee.length > 0) {
    for (let i = 0; i < otherFee.length; i++) {
      otherFeeDivData();
    }
  }
}
//=========================== END OF HANDLING RECEIPT PRINT ======================>

const span__customerIntitule = document.querySelectorAll(
  "#span__customerIntitule"
);
const span__passengerName = document.querySelectorAll("#span__passengerName");
if (span__customerIntitule.length > 0) {
  span__customerIntitule.forEach((span) => {
    let spanTextContent = span.textContent.trim();
    let spanLength = spanTextContent.length;
    if (spanLength >= 25) {
      span.textContent = `${spanTextContent.substring(0, 25)} (...)`;
    } else {
      span.textContent = `${spanTextContent}`;
    }
  });
}
if (span__passengerName.length > 0) {
  span__passengerName.forEach((span) => {
    let spanTextContent = span.textContent.trim();
    let spanLength = spanTextContent.length;
    if (spanLength >= 25) {
      span.textContent = `${spanTextContent.substring(0, 25)} (...)`;
    } else {
      span.textContent = `${spanTextContent}`;
    }
  });
}

/**
 * BOUTON PRECEDENT ET SUIVANT DANS LA PAGE D'AFFICHAGE DETAIL PNR
 */

// Récupérer les éléments HTML nécessaires
const managePnrToSwitch = document.getElementById("managePnrToSwitch");
const buttonPreviousPNR = document.getElementById("previousPNR");
const buttonNextPNR = document.getElementById("nextPNR");

// Supprimer le l'objet pnrAfterSearch du localStorage si la page a été rechargé
if (!window.location.href.includes("/home/pnr/")) {
  window.addEventListener("load", () => {
    localStorage.removeItem("pnrAfterSearch");
  });
}

// Vérifier si l'élément "managePnrToSwitch" existe et possède un attribut "data-pnr-to-switch"
if (managePnrToSwitch && managePnrToSwitch.getAttribute("data-pnr-to-switch")) {
  try {
    // Récupérer les informations des PNR depuis l'attribut "data-pnr-to-switch" et les stocker dans "pnrData"
    let pnrData = JSON.parse(
      managePnrToSwitch.getAttribute("data-pnr-to-switch")
    );

    // Récupérer les données du localStorage s'il y en existe
    const pnrDataFromLocalStorage = JSON.parse(
      localStorage.getItem("pnrAfterSearch")
    );
    if (pnrDataFromLocalStorage) {
      pnrData = pnrDataFromLocalStorage;
    } else {
      pnrData = pnrData;
    }

    // console.table(pnrData);

    // Récupérer l'URL actuelle et la stocker dans "currentUrl"
    const currentUrl = window.location.href;

    // Séparer l'URL en un tableau de chaînes de caractères en utilisant "/" comme séparateur
    const splitUrl = currentUrl.split("/");

    // Récupérer l'ID du PNR à partir de l'URL et le convertir en entier
    const pnrId = parseInt(splitUrl[splitUrl.length - 2]);

    // Vérifier si "pnrData" contient des PNR
    if (pnrData.length > 0) {
      // Récupérer les informations du PNR actuel en utilisant son ID
      const currentPnr = pnrData.find((pnr) => pnr.id === pnrId);

      // Récupérer le premier PNR
      const firstPnr = pnrData.find((pnr) => pnr.position === 0);

      // Récupérer le dernier PNR
      const lastPnr = pnrData.find(
        (pnr) => pnr.position === pnrData.length - 1
      );

      // Désactiver le bouton "Précédent" s'il n'y a pas de PNR précédent et ajouter un titre à la place
      if (currentPnr.position === firstPnr.position) {
        buttonPreviousPNR.setAttribute("disabled", "true");
        buttonPreviousPNR.title = `Le PNR ${currentPnr.number} est le premier PNR dans la liste`;
      }

      // Désactiver le bouton "Suivant" s'il n'y a pas de PNR suivant et ajouter un titre à la place
      if (currentPnr.position === lastPnr.position) {
        buttonNextPNR.setAttribute("disabled", "true");
        buttonNextPNR.title = `Le PNR ${currentPnr.number} est le dernier PNR dans la liste`;
      }

      // Désactiver le bouton "Suivant" et "Précédent" s'il y a qu'un seul PNR
      // Vérifie si le premier PNR et le dernier PNR ont la même position
      if (firstPnr.position === lastPnr.position) {
        // Désactive les boutons "précédent" et "suivant"
        buttonPreviousPNR.setAttribute("disabled", "true");
        buttonNextPNR.setAttribute("disabled", "true");

        // Définit le titre des boutons comme "Il n'y a que le pnr {numéro de PNR courant}"
        buttonPreviousPNR.title = `Il n'y a que le pnr ${currentPnr.number}`;
        buttonNextPNR.title = `Il n'y a que le pnr ${currentPnr.number}`;
      } else {
        // Récupère le PNR précédent et le PNR suivant dans la liste par rapport à la position du PNR en cours
        let prevPnr = pnrData.find(
          (pnr) => pnr.position === currentPnr.position - 1
        );
        let nextPnr = pnrData.find(
          (pnr) => pnr.position === currentPnr.position + 1
        );

        // Si un PNR précédent existe, définit le titre du bouton "précédent" avec son numéro de PNR
        if (prevPnr) {
          buttonPreviousPNR.title = `PNR précédent : ${prevPnr.number}`;
        }

        // Si un PNR suivant existe, définit le titre du bouton "suivant" avec son numéro de PNR
        if (nextPnr) {
          buttonNextPNR.title = `PNR suivant : ${nextPnr.number}`;
        }
      }

      // Ajouter des gestionnaires d'événements pour les clics sur les boutons "Précédent" et "Suivant"
      // Ajoute un écouteur d'événements "click" au bouton "Précédent"
      buttonPreviousPNR.addEventListener("click", (e) => {
        // Empêche le comportement par défaut du clic sur un lien
        e.preventDefault();

        // Vérifie si le PNR en cours n'est pas déjà le premier PNR de la liste
        if (currentPnr.position > firstPnr.position) {
          // Trouve le PNR précédent dans la liste
          const pnr = pnrData.find(
            (pnr) => pnr.position === currentPnr.position - 1
          );

          // Met à jour l'ID du PNR précédent dans l'URL de la page
          splitUrl[5] = pnr.id;

          // Rejoint les éléments de l'URL mis à jour pour former une nouvelle URL
          let newUrl = splitUrl.join("/");

          // Redirige vers la nouvelle URL
          window.location.href = newUrl;
        }
      });

      // Ajoute un écouteur d'événements "click" au bouton "Suivant"
      buttonNextPNR.addEventListener("click", (e) => {
        // Empêche le comportement par défaut du clic sur un lien
        e.preventDefault();

        // Vérifie si le PNR en cours n'est pas déjà le dernier PNR de la liste
        if (currentPnr.position < lastPnr.position) {
          // Trouve le PNR suivant dans la liste
          const pnr = pnrData.find(
            (pnr) => pnr.position === currentPnr.position + 1
          );

          // Met à jour l'ID du PNR suivant dans l'URL de la page
          splitUrl[5] = pnr.id;

          // Rejoint les éléments de l'URL mis à jour pour former une nouvelle URL
          let newUrl = splitUrl.join("/");

          // Redirige vers la nouvelle URL
          window.location.href = newUrl;
        }
      });

      // Afficher la position du PNR actuel dans la liste
      $("#pnrPosition").text(
        `${currentPnr.position + 1} sur ${lastPnr.position + 1}`
      );
    } else {
      console.log("Aucune donnée n'a été récupérée");
      $("#pnrPosition").text("1 sur 1");
    }
  } catch (error) {
    console.log(`Une erreur lors de la récupération des données : ${error}`);
    console.log(error);

    // Remove loading effect
    $("#pnrPosition").text("1 sur 1");

    // // Get the span element with the id "pnrPosition"
    // const pnrPosition = document.getElementById("pnrPosition");

    // // Create a new div element
    // const newDiv = document.createElement("div");

    // // Add a button to the new div
    // newDiv.innerHTML += `
    //   <button id="goBackHome" class="btn btn-sm btn-secondary" title="Revenir dans le menu principal"> Cliquer ici </button>
    // `;

    // // Append the new div element to the span element
    // pnrPosition.appendChild(newDiv);

    // Disabled buttons
    buttonNextPNR.setAttribute("disabled", true);
    buttonPreviousPNR.setAttribute("disabled", true);

    // // Redirect to home page on click button
    // $("#goBackHome").click(function (e) {
    //   e.preventDefault();
    //   goBackHome();
    // });

    // function goBackHome() {
    //   const url = window.location.href;
    //   const baseUrl = url.split("/").slice(0, 4).join("/");
    //   // Redirect to home page
    //   window.location.href = baseUrl;
    // }
  }
} else {
  console.log(
    "L'élément 'managePnrToSwitch' n'existe pas ou ne contient pas d'attribut 'data-pnr-to-switch'"
  );
}

$.ajax({
  type: "GET",
  url: '/home/customer/import_customer/',
  dataType: 'json',
  success: (response) => {
    console.log(response.return);
  },
  error: (response) => {
    console.log(response.return);
  }
});

$.ajax({
  type: "GET",
  url: '/home/product/import_product_odoo/',
  dataType: 'json',
  success: (response) => {
    console.log(response.return);
  },
  error: (response) => {
    console.log(response.return);
  }
});

$(document).ready(function() {
  ExcelUploadPnrList.addEventListener("click", async () => {
    // Récupérer les données depuis le stockage local avec la clé "pnrIds"
    const data = localStorage.getItem("pnrIds");

    // Convertir les données JSON en objet JavaScript
    const pnr_list = JSON.parse(data);

    // Envoyer les données au serveur via une requête AJAX
    $.ajax({
      type: 'POST',
      url: '/pnr/list/to/excel',
      dataType: 'json',
      data: {
        pnr_list: JSON.stringify(pnr_list),
        csrfmiddlewaretoken: csrftoken
      },
      success: async function(data) {
        const XLSX = await import("https://cdn.sheetjs.com/xlsx-0.19.2/package/xlsx.mjs");

        const workbook = XLSX.utils.book_new();

        // Créer une feuille de calcul vide
        const worksheet = XLSX.utils.aoa_to_sheet([]);

        // Ajouter les en-têtes de colonne
        const header = ["Numéro", "Passagerd", "Client","Date de création","Date d'émission","Montant","Statut","OPC","Type","Créateur","Emetteur","Agence","Code"];
        XLSX.utils.sheet_add_aoa(worksheet, [header]);

        // Ajouter les données
        data.results.forEach((pnr, index) => {
          const rowIndex = index + 1; // Décalage pour inclure les en-têtes
          Object.keys(pnr).forEach((key, columnIndex) => {
            XLSX.utils.sheet_add_aoa(worksheet, [[pnr[key]]], { origin: { r: rowIndex, c: columnIndex } });
          });
        });

        // Ajouter la feuille au classeur
        XLSX.utils.book_append_sheet(workbook, worksheet, "PNR List");

        // Écrire le classeur dans un fichier
        XLSX.writeFile(workbook, "PNR_List.xlsx", { compression: true });
      }
    });
  });
});









