//magnitude color
function chooseColor(magnitude) {
    if (magnitude < 1) {
        return "#32CD32";
    } else if (magnitude >= 1 && magnitude < 2) {
        return "#ADFF2F";
    } else if (magnitude >= 2 && magnitude < 3) {
        return "#FFD700";
    } else if (magnitude >= 3 && magnitude < 4) {
        return "#FFA500";
    } else if (magnitude >= 4 && magnitude < 5) {
        return "#FF5C00";
    } else {
        return "#8B0000";
    }
}

//magnitude size
function chooseRadius(magnitude) {
    if (magnitude < 1) {
        return 3;
    } else if (magnitude >= 1 && magnitude < 2) {
        return 6;
    } else if (magnitude >= 2 && magnitude < 3) {
        return 8;
    } else if (magnitude >= 3 && magnitude < 4) {
        return 10;
    } else if (magnitude >= 4 && magnitude < 5) {
        return 12;
    } else {
        return 15;
    }
}

check = 0;

// Define the different tile layers
var light = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
});

var satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
    maxZoom: 18,
});

// Add the different tile layers to the baseMaps object
var baseMaps = {
    "Light Map": light,
    "Satellite Map": satellite,
};

// Define the URLs for the earthquake data
var urls = [
    {
        name: "Hour",
        url: "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
    },
    {
        name: "Day",
        url: "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
    },
    {
        name: "Week",
        url: "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson",
    },
];

// Define a function to add earthquake data to the map
function addEarthquakeData(url, name, overlayMaps, layerGroups) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            // Define the geojson layer for the earthquake data
            var geojson = L.geoJson(data, {
                pointToLayer: function (feature, latlng) {
                    var radius = chooseRadius(feature.properties.mag);
                    var marker_color = chooseColor(feature.properties.mag);
                    return L.circleMarker(latlng, {
                        radius: radius,
                        color: marker_color,
                    });
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup("<strong>" + feature.properties.place + "</strong><br>" +
                        new Date(feature.properties.time).toLocaleString() + "<br>" +
                        "Magnitude: " + feature.properties.mag);
                },
            });

            // Add the earthquake data layer to the overlayMaps and layerGroups objects
            overlayMaps[name] = geojson;
            layerGroups[name].addLayer(geojson);

            return geojson; // Return the geoJSON layer
        })
        .catch(error => console.log(error));
}

// Create layer groups for the earthquake data layers
var hourLayer = L.layerGroup();
var dayLayer = L.layerGroup();
var weekLayer = L.layerGroup();
var faultLayer = L.layerGroup();

// Add the default layers to the map
light.addTo(map);
hourLayer.addTo(map);

// Create a layer switch control and add it to the map
var overlayMaps = {
    "Earthquake Hour": hourLayer,
    "Earthquake Day": dayLayer,
    "Earthquake Week": weekLayer,
    "Fault lines": faultLayer,
};
var layerGroups = {
    "Hour": hourLayer,
    "Day": dayLayer,
    "Week": weekLayer,
    "Fault lines": faultLayer,
};
// L.control.layers(baseMaps, overlayMaps).addTo(map);

// Load the second earthquake data when the user clicks on the layer switch control
map.on('overlayadd', function (eventLayer) {
    if (eventLayer.name === 'Earthquake Week') {
        addEarthquakeData(urls[2].url, "Week", overlayMaps, layerGroups)
            .then(layer => {
                weekLayer.clearLayers();
                weekLayer.addLayer(layer);
            });
    } else if (eventLayer.name === 'Earthquake Day') {
        addEarthquakeData(urls[1].url, "Day", overlayMaps, layerGroups)
            .then(layer => {
                dayLayer.clearLayers();
                dayLayer.addLayer(layer);
            });
    }
});

// Load the first earthquake data on page load
addEarthquakeData(urls[0].url, "Hour", overlayMaps, layerGroups)
    .then(layer => {
        hourLayer.addLayer(layer);
    });


map.on('overlayadd', function (eventLayer) {
    if (eventLayer.name === 'Fault lines') {
        fetch('/static/PB2002_steps.json')
            .then(response => response.json())
            .then(data => {
                var geojson = L.geoJson(data, {
                    style: {
                        color: '#ff7800',
                        weight: 2,
                        opacity: 0.65
                    }
                });

                overlayMaps['Fault lines'] = geojson;
                layerGroups['Fault lines'].addLayer(geojson);

            })
            .catch(error => console.log(error));
    }
});


L.control.layers(baseMaps, overlayMaps, {position: 'topleft'}).addTo(map);


// // Add the tectonic plates layer to the overlayMaps and layerGroups objects
// overlayMaps["Fault Lines"] = geojsonFault;
// layerGroups["Fault Lines"].addLayer(geojsonFault);
//
// // Add the layer control to the map
// L.control.layers(baseMaps, overlayMaps, {position: 'topleft'}).addTo(map);
