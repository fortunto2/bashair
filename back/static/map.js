const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap 2</a> contributors'
// var url = "https://api.bashair.ru";
var url = "http://127.0.0.1:8001";

var newMarker, markerLocation;
var map = L.map('map').setView([53.62, 55.91], 11);

L.control.locate().addTo(map);

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
            const token = data.token;
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
        $.ajax({
            url: url + "/auth/anonymous/login",
            method: "POST",
            success: function (data) {
                token = data.access_token;
                localStorage.setItem("token", token);
                console.log('success anonymous login', token)
            },
            error: function (error) {
                console.error("An error occurred while logging in anonymously: ", error);
            }
        });
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
        }
    });
}


function callback(response) {

    var markersLayer = L.geoJSON(response, {
        onEachFeature: onEachFeature,
        pointToLayer: function (feature, latlng) {

            let arrow_deg = 0

            const node_color = getColor(feature.properties.aqi_category);

            var marker_item;

            if (feature.properties && feature.properties.pm25) {

                marker_item = L.marker.arrowCircle(latlng, {
                    iconOptions: {rotation: arrow_deg, color: node_color, size: 60},
                }).bindPopup(`PM: ${feature.properties.pm25} [${feature.properties.aqi_category}]`);

            } else if (feature.id.startsWith('signal')) {
                marker_item = L.marker(latlng, geojsonSignalOptions).bindPopup(`${feature.properties.text}`);

            } else {
                marker_item = L.circleMarker(latlng, geojsonNodeOptions).bindPopup(`[${feature.id}] отключен`);
            }

            return marker_item


        }
    }).addTo(map);

    newMarkerGroup = new L.LayerGroup();
    // map.on('click', addMarker);

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

$.ajax({
    url: url + "/geo",
    dataType: "json",
    success: function (response) {
        callback(response)
    }
})

