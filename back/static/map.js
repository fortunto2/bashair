const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

var map = L.map('map').setView([53.62, 55.91], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);
// const markers = JSON.parse(document.getElementById('markers-data').textContent);
// let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);


function callback(response) {

    console.log(response);
    L.geoJSON(response).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
};

$.ajax({
    url: "http://127.0.0.1:8001/geo",
    dataType: "json",
    success: function (response) {
        callback(response)
    }
})
