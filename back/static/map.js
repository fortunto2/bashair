const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

var map = L.map('map').setView([53.62,55.91], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);
const markers = JSON.parse(document.getElementById('markers-data').textContent);
let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
