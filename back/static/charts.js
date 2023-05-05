function getColor(aqi_category) {
  switch (aqi_category) {
    case "Good":
      return "#6fc94c";
    case 'Moderate':
      return "#eccf43";
    case 'Unhealthy for Sensitive Groups':
      return "#d27533";
    case 'Unhealthy':
      return "#bb402f";
    case 'Very Unhealthy':
      return "#a61b0a";
    case 'Hazardous':
      return "#7c1208";
    default:
      return "gray";
  }
}

function getChartData(url, nodeId, callback) {
    // Construct the URL for the AJAX request using the nodeId parameter
    url_history = url + `/node/${nodeId}/history`;

    // Make the AJAX request using jQuery's $.getJSON() method
    $.getJSON(url_history, function (data) {

        // Extract the labels and data values from the response data
        // const labels = data.map(entry => entry.time);
        const labels = data.map(data => new Date(data.time));

        // Convert the dates to a shorter format with only the hours
        const formattedLabels = labels.map(date => date.toLocaleTimeString([], {hour: '2-digit'}));

        const pm25Values = data.map(entry => entry.pm25);
        const aqiValues = data.map(entry => entry.aqi);
        const aqiCategory = data.map(entry => entry.aqi_category);


// Set up the chart data and configuration options using the extracted data
        const chartData = {
            labels: formattedLabels,
            datasets: [{
                label: 'AQI',
                data: aqiValues,
                backgroundColor: aqiCategory.map(getColor),
                borderWidth: 1
            }]
        };

        const chartConfig = {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                height: 400,
            }
        };

        // Call the callback function with the chart configuration options
        callback(chartConfig);
    });
}
