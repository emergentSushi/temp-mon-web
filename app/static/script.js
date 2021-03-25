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

function groupBy(arr, criteria) {
	return arr.reduce(function (obj, item) {
		var key = item[criteria];
		if (!obj.hasOwnProperty(key)) {
			obj[key] = [];
		}

		obj[key].push(item);

		return obj;
	}, {});
};

let devices = {
    "A4:C1:38:3B:86:DE": "Loose",
    "A4:C1:38:73:28:DC": "Office",
    "A4:C1:38:A4:86:79": "Roof",
    "A4:C1:38:56:5C:07": "Kitchen",
}

let chartColors = [
	'rgb(255, 99, 132)',
	'rgb(255, 159, 64)',
	'rgb(75, 192, 192)',
	'rgb(54, 162, 235)',
];

document.addEventListener( "DOMContentLoaded", function() { 
    var ctxTemp = document.getElementById('chart-temp');
    var ctxHumidity = document.getElementById('chart-humidity');

    fetch('/data')
        .then(response => response.json())
        .then(data => {

        
        const sensorGrouped = groupBy(data, 'mac');

        var temperatureDatasets = [];
        var humidityDatasets = [];
        let i = 0;
        for (let s in sensorGrouped) {
            temperatureDatasets.push(
                {
                label: `${devices[s]} Celcius`,
                data: sensorGrouped[s].map(p => { return { t: new Date(p.timestamp), y: p.temp }; }),
                borderColor: chartColors[i],
                fill: false
                }
            );
            
            humidityDatasets.push(
                {
                    label: `${devices[s]} Humidity`,
                    data: sensorGrouped[s].map(p => { return { t: new Date(p.timestamp), y: p.humidity }; }),
                    borderColor: chartColors[i],
                    fill: false
                }
            );

            i++;
        }

        new Chart(ctxTemp, {
            type: 'line',
            data: {
              datasets: temperatureDatasets
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

        new Chart(ctxHumidity, {
            type: 'line',
            data: {
              datasets: humidityDatasets
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


