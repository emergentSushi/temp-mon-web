const devices = {
    "A4:C1:38:3B:86:DE": { title: "Loose", colour: 'rgb(255, 99, 132)' },
    "A4:C1:38:73:28:DC": { title: "Office", colour: 'rgb(255, 159, 64)' },
    "A4:C1:38:A4:86:79": { title: "Roof", colour: 'rgb(75, 192, 192)' },
    "A4:C1:38:56:5C:07": { title: "Kitchen", colour: 'rgb(54, 162, 235)' }
}

const options = {
    scales: {
        xAxes: [{
            type: 'time',
            distribution: 'linear',
            time: {
                units: 'hour'
            }
        }]
    }
};

const createDataSet = (prop, titleSuffix, sensorData, device) => { 
    return {
        label: `${device.title} ${titleSuffix}`,
        data: sensorData.map(p => { return { t: new Date(p.timestamp), y: p[prop] }; }),
        borderColor: device.colour,
        backgroundColor: device.colour,
        fill: false
    };
}

document.addEventListener( "DOMContentLoaded", () => { 
    var ctxTemp = document.getElementById('chart-temp');
    var ctxHumidity = document.getElementById('chart-humidity');

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const sensorGrouped = data.groupBy('mac');
            const deviceKeys = Object.keys(sensorGrouped);

            new Chart(ctxTemp, {
                type: 'line',
                data: {
                    datasets: deviceKeys.map(s => createDataSet('temp', 'celsius', sensorGrouped[s], devices[s]))
                },
                options
            });

            new Chart(ctxHumidity, {
                type: 'line',
                data: {
                    datasets: deviceKeys.map(s => createDataSet('humidity', 'humidity', sensorGrouped[s], devices[s]))
                },
                options
            });
        });
});
