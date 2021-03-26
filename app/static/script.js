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
    Promise.all([
        fetch('/data').then(response => response.json()), 
        fetch('/devices').then(response => response.json())
    ]).then((values) => {
        const data = values[0];
        const devices = values[1];

        const sensorGrouped = data.groupBy('mac');
        const deviceKeys = Object.keys(sensorGrouped);

        var model = deviceKeys.map(k => sensorGrouped[k])
            .map(s => s[0])
            .map(z => { return { mac: z.mac, name: devices[z.mac].title, battery: z.battery }; });

        $('#devices')
	        .insertAdjacentHTML('beforeend', render({ devices: model }, 'devices-view'));

        new Chart($('#chart-temp'), {
            type: 'line',
            data: {
                datasets: deviceKeys.map(s => createDataSet('temp', 'celsius', sensorGrouped[s], devices[s]))
            },
            options
        });

        new Chart($('#chart-humidity'), {
            type: 'line',
            data: {
                datasets: deviceKeys.map(s => createDataSet('humidity', 'humidity', sensorGrouped[s], devices[s]))
            },
            options
        });
    });
});
