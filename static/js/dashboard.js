
document.addEventListener("DOMContentLoaded", () => {

  const socket = io.connect();
  const activityCosts = document.querySelector("#activity_cost");
  const costsPerMessage = document.querySelector('#cost_per_message');
  const activityCount = document.querySelector('#activity_count');
  const avgResponseTime = document.querySelector('#avg_response_time');


  $(() => {
    var currentDate = $.datepicker.formatDate("dd.mm.yy", new Date());
    var startDate = $("#startdate").datepicker({
      defaultDate: "+0",
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      numberOfMonths: 1,
      firstDay: 1,
      onSelect: (dateText, inst) => {
        console.log("From:", dateText);
      }
    });
  
    var endDate = $("#enddate").datepicker({
      defaultDate: "+0",
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      numberOfMonths: 1,
      firstDay: 1,
      onSelect: (dateText, inst) => {
        console.log("To:", dateText);
      }
    });
    $("#startdate").attr("placeholder", currentDate);
    $("#enddate").attr("placeholder", currentDate);
    $("#set-daterange-btn").click(() => {
         console.log("FROM",  startDate.datepicker("getDate"), "TO",endDate.datepicker("getDate"));
         socket.emit('update_stats', startDate.datepicker("getDate"), endDate.datepicker("getDate"));
    });
  });

  socket.on('updated_stats', (stats) =>{
    activityCosts.textContent = stats['activity_cost'];
    costsPerMessage.textContent = stats['cost_per_message'];
    activityCount.textContent = stats['activity_count'];
    avgResponseTime.textContent = stats['avg_response_time'];
    //loadChart();
  });


    // Apex Charts initialization code here
    const loadChart = ()=>{
      
      var options = {
        series: [{
        name: "API calls",
        data: [31, 40, 28, 51, 42, 109, 100]
      }],
        chart: {
        type: 'area',
        height: 350,
        background:'transparent',
        zoom: { enabled: false },
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      xaxis: {
        type: 'datetime',
        categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
      },
      tooltip: {
        x: {
          format: 'dd/MM/yy HH:mm'
        },
      },
      theme: {
        mode: 'dark',
        palette: 'palette1',
        monochrome: {
          enabled: true,
          color: '#f18701',
          shadeTo: 'light',
          shadeIntensity: 0.65
         }}
      };

      var chart = new ApexCharts(document.querySelector("#chart"), options);
      chart.render();

    };
    loadChart();
    // var options = {
    //     series: [{
    //     name: 'Total Costs',
    //     data: [0, 0, 0, 1.05, 5.07, 12.56, 7.24, 32.76, 48.53]
    //   }],
    //     chart: {
    //     type: 'bar',
    //     height: 350,
    //     background:'transparent',
    //     // Apply dark theme
    //     toolbar: {
    //     show: false
    //   }
    //   },
    //   plotOptions: {
    //     bar: {
    //       horizontal: false,
    //       columnWidth: '55%',
    //       endingShape: 'rounded'
    //     },
    //   },
    //   dataLabels: {
    //     enabled: false
    //   },
    //   stroke: {
    //     show: true,
    //     width: 2,
    //     colors: ['transparent']
    //   },
    //   xaxis: {
    //     categories: ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
    //     labels: {
    //         style: {
    //           colors: '#fff'
    //         }}
    //   },
    //   yaxis: {
    //     title: {
    //       text: 'dollars',
    //       style: {
    //         color: '#fff'
    //       }
    //     }
    //   },
    //   labels: {
    //     style: {
    //       colors: '#fff'
    //     }
    //   },
    //   fill: {
    //     opacity: 1
    //   },
    //   tooltip: {
    //     y: {
    //       formatter: function (val) {
    //         return  val  + " $ "
    //       }
    //     }
    //   },
    //         // Apply dark theme
    //         theme: {
    //             mode: 'dark',
    //             palette: 'palette1',
    //             monochrome: {
    //               enabled: true,
    //               color: '#f18701',
    //               shadeTo: 'light',
    //               shadeIntensity: 0.65
    //             }
    //           }

    //   };

    //   var chart = new ApexCharts(document.querySelector("#chart"), options);
    //   chart.render();


      
  });
