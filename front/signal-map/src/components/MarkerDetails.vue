<template>
  <div class="person">
    <h2>AQI Air Index: {{ properties.aqi }}</h2>
    <h3>{{ properties.name }}, {{ properties.city }}</h3>
    <hr/>
    <h5>Category: {{ properties.aqi_category }}</h5>
    <li class="pm25">pm2.5: <b>{{ properties.pm25 }}</b></li>
    <li class="pm10">pm10: <b>{{ properties.pm10 }}</b></li>
    <li class="humidity">temperature: <b>{{ properties.temperature }}</b></li>
    <li class="humidity">humidity: <b>{{ properties.humidity }}</b></li>
    <li class="pressure">pressure: <b>{{ properties.pressure }}</b></li>
    <br/>
    <h4>Wind:</h4>
    <li class="wind_deg">angle: <b>{{ properties.wind.deg }}</b></li>
    <li class="wind_gust">gust: <b>{{ properties.wind.gust }}</b></li>
    <li class="wind_speed">speed: <b>{{ properties.wind.speed }}</b></li>

    <br/>
    <br/>
    <button type="button" class="button_alarm">
      <a :href="complaintLink">Where to complain?</a>
    </button>
  </div>
</template>
<script>
export default {
  name: 'MarkerDetails',
  props: ['properties', 'complaintLink'],
};
</script>
