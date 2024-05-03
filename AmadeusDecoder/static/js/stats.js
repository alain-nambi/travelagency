var selectMonth = document.getElementById("selectMonth");

// Obtenir les noms des mois
var months = new Array(12);
for (var i = 0; i < months.length; i++) {
    var date = new Date(2022, i, 1); // Créer une date pour chaque mois
    var monthName = date.toLocaleString('default', { month: 'long' }); // Obtenir le nom du mois
    var option = document.createElement("option");
    option.text = monthName;
    option.value = i + 1; // Les valeurs commencent souvent à 1 pour janvier
    selectMonth.add(option);

}

selectMonth.addEventListener('change', function() {
    var selectedValue = this.value; // Récupérer la valeur sélectionnée
    console.log(selectedValue);
});