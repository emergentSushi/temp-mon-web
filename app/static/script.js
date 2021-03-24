Math.randomRange = function(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

HTMLElement.prototype.empty = function() {
    this.innerHTML = '';
}

HTMLElement.prototype.find = function(query) {
    return find(this, query);
}

HTMLElement.prototype.on = function(event, cb) {
    this.addEventListener(event, cb);
}

if (!HTMLElement.prototype.remove) {
    HTMLElement.prototype.remove = function () {
        this.parentNode.removeChild(this);
    }
}

$ = function(query) {
    return find(document, query);
}

function find(root, query) {
    var nodes = root.querySelectorAll(query);
    if (nodes.length === 1) {
        return nodes[0];
    }
    else return nodes;
}

let devices = {
    "A4:C1:38:3B:86:DE": "Loose",
    "A4:C1:38:73:28:DC": "Office",
    "A4:C1:38:A4:86:79": "Roof",
    "A4:C1:38:56:5C:07": "Kitchen",
}

let chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

document.addEventListener( "DOMContentLoaded", function() { 
    var ctx = document.getElementById('chart');

    fetch('/data')
        .then(response => response.json())
        .then(data => {

        const temperature = data.filter(x => x.mac == "A4:C1:38:A4:86:79")
                                .map(p => { return { t: new Date(p.timestamp), y: p.temp }; });
        
        const humidity = data.filter(x => x.mac == "A4:C1:38:A4:86:79")
                             .map(p => { return { t: new Date(p.timestamp), y: p.humidity }; });

        new Chart(ctx, {
            type: 'line',
            data: {
              datasets: [{
                label: 'Celcius',
                data: temperature,
                borderColor: chartColors.red,
                fill: false
              },
              {
                label: 'Humidity',
                data: humidity,
                borderColor: chartColors.blue,
                fill: false
              }]
            },
            options: {
              scales: {
                xAxes: [{
                  type: 'time',
                  distribution: 'linear',
                  time: {
                      units: 'hour'
                  }
                }]
              }
            }
          });
    });
});


