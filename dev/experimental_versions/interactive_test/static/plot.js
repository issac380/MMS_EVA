document.addEventListener('DOMContentLoaded', function() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            var traces = [];
            for (var key in data) {
                traces.push({
                    x: data[key].time,
                    y: data[key].values,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: key.split('_')[1]  // Adjust the name splitting as needed
                });
            }
            var layout = {
                title: 'MMS Data Plot',
                xaxis: {title: 'Time'},
                yaxis: {title: 'Density'},
                autosize: true
            };
            Plotly.newPlot('plot', traces, layout);
        });
});
