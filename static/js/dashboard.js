document.addEventListener("DOMContentLoaded", function() {
    // Apex Charts initialization code here
      
    var options = {
        series: [{
        name: 'Total Costs',
        data: [0, 0, 0, 1.05, 5.07, 12.56, 7.24, 32.76, 48.53]
      }],
        chart: {
        type: 'bar',
        height: 350,
        background:'transparent',
        // Apply dark theme
        toolbar: {
        show: false
      }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          endingShape: 'rounded'
        },
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
        labels: {
            style: {
              colors: '#fff'
            }}
      },
      yaxis: {
        title: {
          text: 'dollars',
          style: {
            color: '#fff'
          }
        }
      },
      labels: {
        style: {
          colors: '#fff'
        }
      },
      fill: {
        opacity: 1
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return  val  + " $ "
          }
        }
      },
            // Apply dark theme
            theme: {
                mode: 'dark',
                palette: 'palette1',
                monochrome: {
                  enabled: true,
                  color: '#f18701',
                  shadeTo: 'light',
                  shadeIntensity: 0.65
                }
              }

      };

      var chart = new ApexCharts(document.querySelector("#chart"), options);
      chart.render();
  });
