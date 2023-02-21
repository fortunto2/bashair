const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap 2</a> contributors'
var url = "https://api.bashair.ru";
// var url = "http://127.0.0.1:8001";


const map = L.map('map');

map.on('moveend', function () {
    const latlng = map.getCenter();
    const zoom = map.getZoom();
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('location', latlng.lat.toFixed(4) + ',' + latlng.lng.toFixed(4));
    urlParams.set('zoom', zoom);
    window.history.replaceState({}, '', '?' + urlParams.toString());
});


const geocoder = L.Control.geocoder({
    position: 'topright',
    collapsed: false,
    placeholder: 'Поиск по адресу',
    errorMessage: 'Адрес не найден',
    showResultIcons: true,
    defaultMarkGeocode: true,
    geocoder: L.Control.Geocoder.nominatim()
});

const urlParams = new URLSearchParams(window.location.search);
const cityParam = urlParams.get('city');
const locationParam = urlParams.get('location');
const zoomParam = urlParams.get('zoom');
console.log(locationParam, zoomParam, cityParam)


if (locationParam && zoomParam) {
    const locationArray = locationParam.split(',');
    const lat = Number(locationArray[0]);
    const lng = Number(locationArray[1]);
    map.setView([lat, lng], zoomParam);
} else if (cityParam) {
    const geocoder = L.Control.Geocoder.nominatim();
    geocoder.geocode(cityParam, function (results) {
        if (results.length > 0) {
            map.setView(results[0].center, zoomParam || 11, {setHistory: true});
        }
    });
} else {
    map.setView([53.62, 55.91], 11);
}

map.addControl(geocoder);
L.control.locate({
    position: 'topright',
    flyTo: false,
    keepCurrentZoomLevel: true,
    cacheLocation: true,
    setView: 'untilPan',
    strings: {
        title: "Show me where I am"
    },
}).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);
// const markers = JSON.parse(document.getElementById('markers-data').textContent);
// let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);

var sidebar = L.control.sidebar('sidebar', {
    position: 'left'
});

map.addControl(sidebar);

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?

    // if (feature.properties && feature.properties.name) {
    //     layer.bindPopup(feature.properties.name);
    // }
    if (feature.geometry && feature.geometry.type === "MultiPolygon") {
        // console.log('factory')
    }
    if (feature.geometry && feature.geometry.type === "Point") {
        // console.log(feature)
    }
    // if (feature.properties && feature.properties.pm25) {
    //     layer.bindPopup(`PM: ${feature.properties.pm25} [${feature.properties.aqi_category}]`);
    //
    // } else {
    //     layer.bindPopup(`Датчик отключен`);
    // }

}

var geojsonNodeOptions = {
    radius: 6,
    fillColor: "#a6a6a6",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

var geojsonSignalOptions = {
    radius: 10,
    fillColor: "#de4f4f",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

// Add marker on map click
map.on('click', function (event) {
    var lat = event.latlng.lat;
    var lng = event.latlng.lng;
    addMarker(lat, lng);
});


// Add marker function
function addMarker(lat, lng) {
    var marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup("");

    sidebar.show();
    const _sidebar_html = `
        
        <form id="create-signal-form">
          <label for="text">Сообщение:</label>
          <input type="text" name="text" id="text">
          <br>
          <br>
    
          <label for="properties">Что вы чувствуете:</label>
          <div id="properties-checkboxes"></div>
          <br>
    
          <button type="submit">Отправить</button>
        </form>
      `;
    sidebar.setContent(_sidebar_html);

    // Populate properties dropdown list
    $.ajax({
        type: "GET",
        url: url + "/signal/properties",
        success: function (response) {
            var properties = response;
            var checkboxes = '';
            for (var i = 0; i < properties.length; i++) {
                checkboxes += '<div class="properties"><input type="checkbox" name="properties" value="' + properties[i].id + '"><label>' + properties[i].name + '</label></div>';
            }
            $('#properties-checkboxes').html(checkboxes);

        },
        error: function (response) {
            console.error(response);
        }
    });

    // Add custom note to marker when form is submitted
    $("#create-signal-form").submit(function (event) {
        event.preventDefault();
        var text = $("#text").val();
        var selectedProperties = $("#properties-checkboxes input:checked").map(function () {
            return $(this).val();
        }).get();
        marker.setPopupContent(text);
        marker.openPopup();
        sendMarkerData(lat, lng, text, selectedProperties);
        $("#text").val("");
        $("#properties input:checked").prop("checked", false);
        sidebar.hide()
    });
}


function anonymousLogin() {
    $.ajax({
        url: url + "/auth/anonymous/login",
        method: "POST",
        success: function (data) {
            const token = data.access_token;
            localStorage.setItem("token", token);
            console.info('success anonymous login')
        },
        error: function (error) {
            console.error("An error occurred while logging in anonymously: ", error);
        }
    });
}

let token = localStorage.getItem("token");

$(document).ready(function () {
    if (!token) {
        anonymousLogin();
    }
});

function sendMarkerData(lat, lng, text, selectedProperties) {
    if (!token) {
        console.error("No token found in local storage after anonymousLogin");
        return;
    }

    console.log(token)

    $.ajax({
        type: "POST",
        url: url + "/signal/send",
        headers: {
            "Authorization": "Bearer " + token,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": "https://api.bashair.ru,https://map.bashair.ru",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        data: JSON.stringify({
            "latitude": lat,
            "longitude": lng,
            "text": text,
            "properties": selectedProperties,
            "city_id": 1,
            "time_of_incident": new Date().toISOString()
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log(response);
        },
        error: function (response) {
            console.error(response);
            if (response.status === 422) {
                console.error("Invalid data sent to server");
               $.ajax({
                    url: url + "/auth/anonymous/login",
                    method: "POST",
                    success: function (data) {
                        token = data.access_token;
                        localStorage.setItem("token", token);
                        console.log('success anonymous login', token)
                        // Retry sending signal with new access token
                        sendMarkerData(lat, lng, text, selectedProperties);
                    },
                    error: function (error) {
                        console.error("An error occurred while logging in anonymously: ", error);
                    }
                });
            }
        }
    });
}


function callback(response) {

    var dataMarker = [];

    var markersLayer = L.geoJSON(response, {
        onEachFeature: onEachFeature,
        pointToLayer: function (feature, latlng) {

            let arrow_deg = 0

            const node_color = getColor(feature.properties.aqi_category);

            var marker_item;

            if (feature.properties && feature.properties.pm25) {

                arrow_deg = feature.properties.wind.deg - 180;

                marker_item = L.marker.arrowCircle(latlng, {
                    iconOptions: {rotation: arrow_deg, color: node_color, size: 60},
                }).bindPopup(`AQI: ${feature.properties.aqi} [${feature.properties.aqi_category}]`);

                // / Add the lat/lng point to the dataMarker array
                dataMarker.push([
                    latlng.lat,
                    latlng.lng,
                    getHeatIntensity(feature.properties.aqi_category, feature.properties.aqi)
                ]);


            } else if (feature.id.startsWith('signal')) {
                marker_item = L.marker(latlng, geojsonSignalOptions).bindPopup(`${feature.properties.text}`);

            } else {
                marker_item = L.circleMarker(latlng, geojsonNodeOptions).bindPopup(`[${feature.id}] отключен`);
            }

            return marker_item


        }
    }).addTo(map);

    map.on('zoomend', function () {
        if (map.getZoom() < 8) {
            markersLayer.remove();
        } else {
            markersLayer.addTo(map);
        }
    });

    newMarkerGroup = new L.LayerGroup();
    // map.on('click', addMarker);

    console.log(dataMarker)

    let gradientColors = {
        0.1: 'green',
        0.2: 'lime',
        0.4: 'yellow',
        0.6: 'orange',
        0.8: 'red'
    };

    console.log(dataMarker)

    // Create the heatmap layer
    const heat = L.heatLayer(dataMarker, {
        radius: 70,
        blur: 50,
        maxZoom: 11,
        gradient: gradientColors
    });

    heat.addTo(map);


    markersLayer.on("click", function (event) {
        sidebar.show();

        var clickedMarker = event.layer;
        var feature = clickedMarker.feature;
        var properties = feature.properties;

        var _sidebar_html;

        const date = new Date(properties.created);
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric'
        };
        const humanDateTime = date.toLocaleString('ru-RU', options); // Returns 'February 15, 2023, 9:29:45 PM' in en-US locale


        if (feature.id.startsWith('signal')) {
            _sidebar_html = `
            <div class="person">
                <h2>${properties.text}</h2>
                <h4>${humanDateTime}</h4>
                <div>${properties.properties}</div>
                <br />
                <button type="button" class="button_alarm"><a href="https://bashair.ru/help/">Куда жаловаться?</a></button>
             </div>
            `;
        } else if (feature.properties && feature.properties.pm25) {

            _sidebar_html = `
            <div class="person">
                <h2>Индекс воздуха AQI: ${properties.aqi}</h2>
                <h3>${properties.name}, ${properties.city}</h3>
                <hr />
                <h5>Категория: ${properties.aqi_category}</h5>
                <li class="pm25">pm2.5: <b>${properties.pm25}</b></li>
                <li class="pm10">pm10: <b>${properties.pm10}</b></li>
                <li class="humidity">температура: <b>${properties.temperature}</b></li>
                <li class="humidity">влажность: <b>${properties.humidity}</b></li>
                <li class="pressure">давление: <b>${properties.pressure}</b></li>
                <br />
                <h4>Ветер:</h4>
                <li class="wind_deg">угол: <b>${properties.wind.deg}</b></li>
                <li class="wind_gust">порыв: <b>${properties.wind.gust}</b></li>
                <li class="wind_speed">скорость: <b>${properties.wind.speed}</b></li>
                <br />
                <div class="chart-container" >
                    <canvas id="sensorChart"></canvas>
                </div>
                <br />
                <a href="https://panel.bashair.ru/d/g5CKOmB7k/sterlitamak">Подробный график</a>
                <br />
                <br />
                <button type="button" class="button_alarm"><a href="https://bashair.ru/help/">Куда жаловаться?</a></button>
             </div>
            `;

            getChartData(url, properties.id, function (chartConfig) {
                const sensorChart = new Chart($('#sensorChart'), chartConfig);
            });

        } else {
            _sidebar_html = `
            <div class="person">
                <h2>Датчик отключен</h2>
             </div>
            `;
        }

        sidebar.setContent(_sidebar_html);
        console.log('click', feature)

        // const chartContainer = document.querySelector('.chart-container');
        // chartContainer.style.height = '400px';
        // chartContainer.style.width = '600px';


    });


};

function getHeatIntensity(aqi_category, aqi) {
    let intensity = 0;
    switch (aqi_category) {
        case 'Good':
            intensity = aqi / 200;
            break;
        case 'Moderate':
            intensity = aqi / 200;
            break;
        case 'Unhealthy for Sensitive Groups':
            intensity = aqi / 200;
            break;
        case 'Unhealthy':
            intensity = aqi / 300;
            break;
        case 'Very Unhealthy':
            intensity = aqi / 300;
            break;
        case 'Hazardous':
            intensity = aqi / 400;
            break;
        default:
            intensity = 0;
    }
    return intensity;
}


$.ajax({
    url: url + "/geo",
    dataType: "json",
    success: function (response) {
        callback(response)
    }
})


