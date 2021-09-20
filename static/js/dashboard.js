// This is for able to see chart. We are using Apex Chart. U can check the documentation of Apex Charts too..
var dashboard = {
  series: [{
      name: "Benign",
      data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
    },
    {
      name: "Malicious",
      data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
    },
  ],
  chart: {
    type: "bar",
    height: 250, // make this 250
    sparkline: {
      enabled: true, // make this true
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "55%",
      endingShape: "rounded",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: ["transparent"],
  },
  xaxis: {
    categories: ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
  },
  yaxis: {
    title: {
      text: " (urls)",
    },
  },

  tooltip: {
    y: {
      formatter: function (val) {
        return val + " urls";
      },
    },
  },
};


var api = {
  series: [{
    name: 'series2',
    data: [11, 32, 45, 32, 34, 52, 41]
  }],
    chart: {
    height: 350,
    type: 'area'
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
  };



  var ml_accuracy = {
    series: [98],
    chart: {
    height: 250,
    type: 'radialBar',
  },
  plotOptions: {
    radialBar: {
      hollow: {
        size: '70%',
      }
    },
  },
  labels: ['ML Accuracy'],
  };



  var ml_predict = {
    series: [90],
    chart: {
    height: 250,
    type: 'radialBar',
  },
  plotOptions: {
    radialBar: {
      hollow: {
        size: '70%',
      }
    },
  },
  labels: ['ML Predicted'],
  };






var chart = new ApexCharts(document.querySelector("#apex1"), dashboard);
chart.render();

var chart = new ApexCharts(document.querySelector("#apex2"), api);
chart.render();

var chart = new ApexCharts(document.querySelector("#apex3"), ml_accuracy);
chart.render();

var chart = new ApexCharts(document.querySelector("#apex4"), ml_predict);
chart.render();

// Sidebar Toggle Codes;

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");
var sidebarCloseIcon = document.getElementById("sidebarIcon");

function toggleSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add("sidebar_responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove("sidebar_responsive");
    sidebarOpen = false;
  }
}

// Utk active navbar
$(document).ready(function () {
  $('.sidebar__link').on('click', function () {
    $('div.sidebar__link.active_menu_link ').removeClass('active_menu_link');
    $(this).addClass('active_menu_link');
  })
})

//Pie chart
$(function () {
  $('.chart').easyPieChart({
    size: 200,
    lineWidth: 12,
    barColor: '#000000'
  });
});