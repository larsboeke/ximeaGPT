
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
      minDate: "29.06.2023",
      maxDate: new Date(),
      onSelect: (dateText, inst) => {
        console.log("From:", dateText);
        var selectedDate = new Date(inst.selectedYear, inst.selectedMonth, inst.selectedDay);
        console.log(selectedDate);
        selectedDate.setDate(selectedDate.getDate()); 
        endDate.datepicker("option", "minDate", selectedDate);
      }    
    });
  
    var endDate = $("#enddate").datepicker({
      defaultDate: "+0",
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      numberOfMonths: 1,
      firstDay: 1,
      maxDate: new Date(),
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

      // Apex Charts initialization here
      const loadChart = (graphData)=>{
        var options = {
          series: [{
          name: "API calls",
          data: graphData.count
        }],
          chart: {
          type: 'bar',
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
    console.log("Socket: updated_stats emited");
    console.log("Socket: updated_stats: graphdata",stats['graph_data']);
    activityCosts.textContent = stats['activity_cost']+ " $";
    costsPerMessage.textContent = stats['cost_per_message']+ " $";
    activityCount.textContent = stats['activity_count'];
    avgResponseTime.textContent = stats['avg_response_time']+ " sec";
    chart.destroy();
    loadChart(stats['graph_data']);
    console.log('UPDATED GRAPH.....', stats['graph_data']);
  });

  socket.emit('load_chart');

  socket.on('loaded_chart', (graphData) =>{
    loadChart(graphData);
    console.log('LOADED A GRAPH FOR TODAY.....', graphData);
});


});
