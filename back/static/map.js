const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

var map = L.map('map').setView([53.62, 55.91], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);
// const markers = JSON.parse(document.getElementById('markers-data').textContent);
// let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);



function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    console.log(feature)
    console.log(layer)
    if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name);
    }
    if (feature.geometry && feature.geometry.type === "MultiPolygon" ) {
        console.log('factory')
    }
    if (feature.geometry && feature.geometry.type === "Point" ) {
        console.log('point')
    }
    if (feature.properties && feature.properties.pm25) {
        layer.bindPopup(`PM: ${feature.properties.pm25} [${feature.properties.aqi_category}]`);
    }

}

var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};


function callback(response) {

    console.log(response);

    // L.geoJSON(response, {
    //     onEachFeature: onEachFeature
    // }).addTo(map);

    L.geoJSON(response, {
        onEachFeature: onEachFeature,
        style: function(feature) {
            console.log(feature)
            if (feature.geometry && feature.geometry.type === "Point" ) {
                switch (feature.properties.aqi_category) {

                    case "Good": return {color: "#82ff53"};
                    case 'Moderate':   return {color: "#ffd500"};
                    case 'Unhealthy for Sensitive Groups':   return {color: "#ff6f6f"};
                    case 'Unhealthy':   return {color: "#c7005a"};
                    case 'Very Unhealthy':   return {color: "#5e0029"};
                    case 'Hazardous':   return {color: "#340000"};
                }
            }
        },
        pointToLayer: function (feature, latlng) {
            // console.log(feature)
            return L.marker
            .arrowCircle(latlng, {
              iconOptions: { rotation: feature.properties.wind.deg},
            })
        }
    }).addTo(map);

};

$.ajax({
    // url: "https://api-dev.bashair.ru/geo",
    url: "http://localhost:8001/geo",
    dataType: "json",
    success: function (response) {
        callback(response)
    }
})
