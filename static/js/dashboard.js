
document.addEventListener("DOMContentLoaded", () => {

  const socket = io.connect();
  const activityCosts = document.querySelector("#activity_cost");
  const costsPerMessage = document.querySelector('#cost_per_message');
  const activityCount = document.querySelector('#activity_count');
  const avgResponseTime = document.querySelector('#avg_response_time');
  let chart;



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
        console.log("Emitting update_stats: FROM",  startDate.datepicker("getDate"), "TO",endDate.datepicker("getDate"));
        socket.emit('update_stats', startDate.datepicker("getDate"), endDate.datepicker("getDate"));
      })
    });


  
  const updateChart = (graphData) => {
    console.log("UPDATING GRAPH....", graphData);
      chart.updateOptions([{ data: graphData.count }]); //updateSeries
      chart.updateOptions({ xaxis: { categories: graphData.timestamp } });
  };

      // Apex Charts initialization code here
      const loadChart = (graphData)=>{
        var options = {
          series: [{
          name: "API calls",
          data: graphData.count
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
          categories: graphData.timestamp
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
        chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();
      };


  socket.on('updated_stats', (stats) =>{
    console.log("Socket: updated_stats emmited");
    console.log("WHY IS LAST VALUE MISSING???", stats['graph_data']);
    activityCosts.textContent = stats['activity_cost'];
    costsPerMessage.textContent = stats['cost_per_message'];
    activityCount.textContent = stats['activity_count'];
    avgResponseTime.textContent = stats['avg_response_time'];
    updateChart(stats['graph_data']);
  });

  socket.emit('load_chart');
  socket.on('loaded_chart', (graphData) =>{
    loadChart(graphData);
    console.log('LOADED A GRAPH FOR TODAY.....');
});


  


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
