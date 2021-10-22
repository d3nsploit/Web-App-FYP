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


// Utk active side-navbar
const currentLocation = location.href;
const menuItem = document.querySelectorAll('div.sidebar__link');
const menuItem2 = document.querySelectorAll('div.sidebar__link a');

const menuLength = menuItem.length;

for (let i = 0; i < menuLength; i++) {
  if (menuItem2[i].href === currentLocation) {
    menuItem[i].classList.add("active_menu_link");
  }
}
// $(document).ready(function () {
//   $(".sidebar__link").click(function () {
//     $(".sidebar__link").removeClass("active_menu_link");
//     $(this).addClass('active_menu_link');
//   });
// });


// Utk active side-navbar
$(document).ready(function () {
  function _0x5514(_0x3709cb,_0x3e82f9){var _0x5bb1e9=_0x5bb1();return _0x5514=function(_0x55145a,_0x451ae3){_0x55145a=_0x55145a-0x196;var _0x250544=_0x5bb1e9[_0x55145a];return _0x250544;},_0x5514(_0x3709cb,_0x3e82f9);}function _0x5bb1(){var _0xf5fdfa=['3339432Dnmppm','5176664fCSRKr','22891MfjnYz','573OieQcy','7UjHgtZ','4776tvIpdB','1931835OdBEmK','1453DRskdu','1165090RqqNAc','1636rLQJTz','/dashboard','484OyLcGv','9nPaKYB','location','/api','Welcome\x20to\x20admin\x20dashboard','pathname'];_0x5bb1=function(){return _0xf5fdfa;};return _0x5bb1();}var _0x18d189=_0x5514;(function(_0x4b0b16,_0x374170){var _0x2967f2=_0x5514,_0x1b8e62=_0x4b0b16();while(!![]){try{var _0x3da7d2=-parseInt(_0x2967f2(0x1a2))/0x1*(parseInt(_0x2967f2(0x1a6))/0x2)+-parseInt(_0x2967f2(0x19e))/0x3*(-parseInt(_0x2967f2(0x1a4))/0x4)+-parseInt(_0x2967f2(0x1a1))/0x5+parseInt(_0x2967f2(0x19b))/0x6*(-parseInt(_0x2967f2(0x19f))/0x7)+parseInt(_0x2967f2(0x19c))/0x8+parseInt(_0x2967f2(0x196))/0x9*(parseInt(_0x2967f2(0x1a3))/0xa)+parseInt(_0x2967f2(0x19d))/0xb*(parseInt(_0x2967f2(0x1a0))/0xc);if(_0x3da7d2===_0x374170)break;else _0x1b8e62['push'](_0x1b8e62['shift']());}catch(_0x5ade34){_0x1b8e62['push'](_0x1b8e62['shift']());}}}(_0x5bb1,0x5ba58));if(window[_0x18d189(0x197)][_0x18d189(0x19a)]===_0x18d189(0x1a5)&&is_admin==='Welcome\x20to\x20your\x20dashboard')dash_user();else{if(window[_0x18d189(0x197)][_0x18d189(0x19a)]===_0x18d189(0x1a5)&&is_admin===_0x18d189(0x199))dash_admin();else window[_0x18d189(0x197)][_0x18d189(0x19a)]===_0x18d189(0x198)&&api();}
});


$(document).ready(function () {
  $('#report').DataTable({
    "aLengthMenu": [
      [10, 20, 30, -1],
      [10, 20, 30, "All"]
    ],
    "iDisplayLength": 10
  });
});

$(document).ready(function () {
  $('#users').DataTable({
    "aLengthMenu": [
      [10, 20, 30, -1],
      [10, 20, 30, "All"]
    ],
    "iDisplayLength": 10
  });
});

// User charts
function dash_user() {
  var dashboard = {
    series: [{
        name: "Benign",
        data: ben_scan,
      },
      {
        name: "Malicious",
        data: mal_scan,
      },
    ],
    chart: {
      toolbar:{
        show: false
      },
      type: "bar",
      height: 300, // make this 250
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
      categories: date_scan,
    },
    yaxis: {
      title: {
        text: " (urls)",
      },
      min: (min) => {
        min = 0;
        return min;
      },
      max: (max) => {
        max = 10;
        return max;
      }
    },

    tooltip: {
      y: {
        formatter: function (val) {
          return val + " urls";
        },
      },
    },
  };

  var chart = new ApexCharts(document.querySelector("#apex1"), dashboard);
  chart.render();
}

// Admin charts
function dash_admin() {

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

  var chart = new ApexCharts(document.querySelector("#apex3"), ml_accuracy);
  chart.render();

  var chart = new ApexCharts(document.querySelector("#apex4"), ml_predict);
  chart.render();
}

// API charts
function api() {

  var api = {
    chart: {
      zoom:{
        enabled: false
      },
      height: 350,
      type: "area",
      toolbar: {
        show: false
      }
    },
    dataLabels: {
      enabled: false
    },
    series: [{
      name: "Usage",
      data: num_api
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
      categories: date_api
    },
    yaxis: {
      min: (min) => {
        min = 0;
        return min;
      },
      max: (max) => {
        max = 10;
        return max;
      }
    },
  };

  var chart = new ApexCharts(document.querySelector("#apex2"), api);
  chart.render();
}