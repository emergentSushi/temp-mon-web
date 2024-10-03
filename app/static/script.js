const options = {
    scales: {
        x: {
            display: true,
            type: 'time',
            time: {
                unit: 'hour'
            }
        }
    }
};

const createDataSet = (prop, titleSuffix, sensorData, device) => {
    // cull data if we're pulling large numbers of points, bandwidth is cheap, but chartjs starts lagging a 
    // bit when there's thousands of points
    if (sensorData.length > 10000) {
        sensorData = sensorData.filter(function(_, index) {
            return index % 10 == 0;
        })
    }

    return {
        label: `${device.name} ${titleSuffix}`,
        data: sensorData.map(p => { return { t: new Date(p.timestamp), y: p[prop] }; }),
        borderColor: device.graph_colour,
        backgroundColor: device.graph_colour,
        fill: false
    };
}

document.addEventListener( "DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const start = params.get('start') ?? Math.floor(Date.now() / 1000);
    const lookBackHours = params.get('hours') ?? 12;

    Promise.all([
        fetch(`/data?start=${start}&hours=${lookBackHours}`).then(v => v.json()), 
        fetch('/devices').then(v => v.json())
    ])
    .then((values) => {
        const data = values[0];
        const devices = values[1];

        const sensorGrouped = data.groupBy('mac');
        const deviceKeys = Object.keys(sensorGrouped);

        var batteryData = deviceKeys.map(k => sensorGrouped[k])
            .map(s => s[0]) // recorded battery levels fluctuate with temperature, take the most recent value
            .map(z => { return { mac: z.mac, name: devices[z.mac].name, battery: z.battery }; });

        $('#devices').appendHtml(render({ devices: batteryData }, 'devices-view'));

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
    })
    .catch(err => $('body').appendHtml(render({ errorText: JSON.stringify(err) }, 'error')));
});
