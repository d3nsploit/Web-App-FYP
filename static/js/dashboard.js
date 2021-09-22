// Scanned URL for dashboard
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


// API usage charts
var api = {
  chart: {
    height: 280,
    type: "area",
    toolbar: {
      show: false
    }
  },
  dataLabels: {
    enabled: false
  },
  series: [{
    name: "Series 1",
    data: [45, 52, 38, 45, 19, 23, 2]
  }],
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.9,
      stops: [0, 90, 100]
    }
  },
  xaxis: {
    categories: [
      "01 Jan",
      "02 Jan",
      "03 Jan",
      "04 Jan",
      "05 Jan",
      "06 Jan",
      "07 Jan",
      "08 Jan"
    ]
  }
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



const currentLocation = location.href;
const menuItem = document.querySelectorAll('div.sidebar__link');
const menuItem2 = document.querySelectorAll('div.sidebar__link a');

const menuLength = menuItem.length;

for (let i=0; i < menuLength; i++){
  if(menuItem2[i].href === currentLocation){
    menuItem[i].classList.add("active_menu_link");
  }
}
// Utk active navbar
// $(document).ready(function () {
//   $(".sidebar__link").click(function () {
//     $(".sidebar__link").removeClass("active_menu_link");
//     $(this).addClass('active_menu_link');
//   });
// });





//Pie chart
$(function () {
  $('.chart').easyPieChart({
    size: 200,
    lineWidth: 12,
    barColor: '#000000'
  });
});