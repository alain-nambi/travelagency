$("#all-unordered-pnr-after-search").hide();



$(document).ready(function () {

  $("#unordered_pnr-research").on("click", function () {
    searchFunction();
  });
});

function searchFunction() {
  console.log('====================================');
  
  var pnr_research = $("#input-unordered-pnr").val().toLowerCase();
  if (pnr_research.trim() != "") {
    $("#spinnerLoadingSearch").show();
    $.ajax({
      type: "POST",
      url: "/home/unordered-pnr-research",
      dataType: "json",
      data: {
        pnr_research: pnr_research,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (data) {
        let SEARCH_RESULT = data.results;

        if (SEARCH_RESULT.length > 0) {
          document.querySelector("#all-unordered-pnr-after-search").innerHTML = "";

          $("#all-unordered-pnr-after-search").show();
          $("#initialPagination").hide();
          $("#spinnerLoadingSearch").hide();



          $(".request-pnr-counter").text(SEARCH_RESULT.length);
          $("#unorderedpnrCounterOnSearch").val(" / " + SEARCH_RESULT.length);

          let pnrAfterSearch = SEARCH_RESULT.map((invoice, index) => {
            return { id: invoice.pnr_id, position: index, number: invoice.pnr_number };
          });
          

          localStorage.setItem(
            "pnrAfterSearch",
            JSON.stringify(pnrAfterSearch)
          );

          // $("tbody.tbody-unordered-pnr").remove();
          $("#all-unordered-pnr").remove();
          $("#all-unordered-pnr-after-search").show();

          var options = {
            dataSource: SEARCH_RESULT, // La source de données pour la pagination (ici, les lignes de la table)
            locator: "items",
            showGoInput: true,
            showGoButton: true,
            showNavigator: true,
            formatNavigator:
              "<%= rangeStart %> - <%= rangeEnd %> sur <%= totalNumber %> résultat(s)",
            callback: function (data, pagination) {
              // La fonction de rappel pour mettre à jour les résultats affichés
              var html = "";
              $.each(data, function (index,invoice) {

                html += `
                    <thead id="thead-all-pnr">
                    <tr id="tr-all-pnr">
                      <th>Numéro</th>
                      <th>Numéro de commande</th> 

                      <th class="pnr-creation-date" style="cursor: pointer;">
                        <div class="d-flex align-items-center justify-content-between text-sm" style="gap: 5px">
                          Date du décommande
                          <i class="fa fa-sm fa-solid" id="icon__pnrDateCreation"></i>
                        </div>
                      </th>

                      <th>Motif</th>
                      
                      
                      <th class="pnr-creator-list">
                        <div class="d-flex align-items-center justify-content-between text-sm" style="gap: 5px">
                          Créateur
                          <i class="fa fa-sm fa-solid" id="icon__pnrCreator"></i>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="tbody-unordered-pnr-after-search">
                    <tr 
                      
                      onclick="location.href='/home/pnr/${invoice.id}/'" 
                      style="cursor: pointer;" 
                      role="row"
                    >
                      <td> 
                        ${invoice.pnr_number}  
                      </td>             
                      <td> ${invoice.invoice_number} </td>
                      <td> ${invoice.date} </td>

                      <td> ${invoice.motif} </td>
                      <td> ${invoice.user} </td>
                      
                    </tr>
                  </tbody>
                `;
              });
              $("all-unordered-pnr-after-search").html(html); // Mise à jour du contenu de la table
              $("#all-unordered-pnr-after-search").html(html).trigger("update");
            },
          };

          $("#pagination").pagination(options); // Initialisation de la pagination avec les options définies

        } else {
          $("#spinnerLoadingSearch").hide();
          const input__searchPnrValue = $("#input-unordered-pnr").val();
          $("#input-unordered-pnr").val("");
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
