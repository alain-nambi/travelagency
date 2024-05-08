var destination;
var passenger_data; 
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          destination = response.all_data;
          passenger_data = response.passenger_by_age;
          
          
        } else {
            // Il y a eu une erreur lors de la récupération des données
            console.error('Une erreur est survenue lors de la récupération des données : ' + xhr.status);
        }
    }
};
xhr.open('GET', '/stat/details', true);
xhr.send();

function filterDestinationsByMonth(destinations, month) {
  destinations.filter((element) => element['month'] == month);
}

destination = filterDestinationsByMonth(destination, 12);
var destination_categories = [];
destination.forEach(element => {
  console.log(element);
});

Highcharts.chart('container', {
  chart: {
      type: 'bar'
  },
  title: {
      text: 'Historic World Population by Region',
      align: 'left'
  },

  xAxis: {
      categories: ['Africa', 'America', 'Asia', 'Europe'],
      title: {
          text: null
      },
      gridLineWidth: 1,
      lineWidth: 0
  },
  yAxis: {
      min: 0,
      title: {
          text: 'Population (millions)',
          align: 'high'
      },
      labels: {
          overflow: 'justify'
      },
      gridLineWidth: 0
  },
  tooltip: {
      valueSuffix: ' millions'
  },
  plotOptions: {
      bar: {
          dataLabels: {
              enabled: true
          },
          groupPadding: 0.1
      }
  },
  credits: {
      enabled: false
  },
  series: [{
      name: 'Year 1990',
      data: [631, 727, 3202, 721]
  }, {
      name: 'Year 2000',
      data: [814, 841, 3714, 726]
  }, {
      name: 'Year 2018',
      data: [1276, 1007, 4561, 746]
  }]
});
