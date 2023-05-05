// Set up the map
var map = L.map('map').setView([51.505, -0.09], 13);

// Add a tile layer to the map (for example, OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

const pollutionSource = [51.505, -0.09]; // coordinates of the pollution source
const windSpeed = 1; // wind speed in m/s
const markers = L.markerClusterGroup();

// Function that calculates the coordinates of a point based on wind speed and time
function calculatePoint(latitude, longitude, windSpeed, angle, time) {
  if (!latitude || !longitude) {
    return null;
  }
  const distance = windSpeed * time;
  const radius = 6371000; // Earth's radius in meters
  const lat1 = latitude * Math.PI / 180;
  const lon1 = longitude * Math.PI / 180;
  const bearing = angle * Math.PI / 180;

  const lat2 = Math.asin(Math.sin(lat1) * Math.cos(distance / radius) +
    Math.cos(lat1) * Math.sin(distance / radius) * Math.cos(bearing));

  const lon2 = lon1 + Math.atan2(Math.sin(bearing) * Math.sin(distance / radius) * Math.cos(lat1),
    Math.cos(distance / radius) - Math.sin(lat1) * Math.sin(lat2));

  return L.latLng([lat2 * 180 / Math.PI, lon2 * 180 / Math.PI]);
}

// Function that calculates the air pollution based on the distance to the source and wind speed
function calculatePollution(distance, windSpeed) {
  return Math.exp(-0.05 * distance / windSpeed);
}

// Function that calculates the color of the point on the heat map based on the air pollution
function calculateColor(pollution) {
  const r = 255 - Math.floor(255 * pollution);
  const g = Math.floor(255 * pollution);
  const b = 0;
  return `rgb(${r}, ${g}, ${b})`;
}
// Function that creates a heat map around the pollution source
function createHeatMap(pollutionSource, windSpeed) {
  const heatMapData = [];
  const maxPollution = 1000;
  for (let i = 0; i < 360; i++) {
    const point = calculatePoint(pollutionSource[0], pollutionSource[1], windSpeed, i, 3600); // Calculate the coordinates of the point after 1 hour
    const distance = point ? L.latLng(point).distanceTo(L.latLng(pollutionSource)) : 0; // Calculate the distance to the pollution source
    const pollution = calculatePollution(distance, windSpeed); // Calculate the air pollution based on the distance and wind speed
    const intensity = pollution / maxPollution;
    const color = intensity > 1 ? "#FF0000" : `rgb(255, ${Math.floor(intensity*255)}, 0)`;
    if (point) {
      heatMapData.push([point.lat, point.lng, intensity]); // Add the point to the heat map data
    }
  }
  console.log(heatMapData);
  const heatMapLayer = L.heatLayer(heatMapData, {
    radius: 30,
    blur: 10,
    minOpacity: 0.5
  }).addTo(map); // Create the heat map layer with the heat map data
  return heatMapLayer;
}


// Create the heat map layer
const heatMapLayer = createHeatMap(pollutionSource, windSpeed);

// Add the heat map layer to the map
heatMapLayer.addTo(map);

// Create a marker for the pollution source
const sourceMarker = L.circleMarker(pollutionSource, {
  radius: 10,
  color: 'red'
}).bindPopup('Pollution Source');

// Add the pollution source marker to the map
sourceMarker.addTo(map);

// Add the marker cluster group to the map
markers.addTo(map);
