<template>
  <div style="height:600px; width:800px">
    <p>Signal Map</p>
    <l-map ref="map" v-model:zoom="zoom" :center="[47.41322, -1.219482]">
      <l-geo-json :geojson="geojsonData" :options="geojsonOptions"/>
    </l-map>
  </div>
</template>
<script>
import "leaflet/dist/leaflet.css";
import {LMap, LGeoJson} from "@vue-leaflet/vue-leaflet";
import {mapGetters} from "vuex";

export default {
  components: {
    LMap,
    LGeoJson,
  },
  data() {
    return {
      zoom: 2,
    };
  },
  computed: {
    ...mapGetters({
      geoData: "geoData",
    }),
    geojsonData() {
      return this.geoData;
    },
    geojsonOptions() {
      return {};
    },
  },
  async beforeMount() {
    const {circleMarker} = await import("leaflet/dist/leaflet-src.esm");

    this.geojsonOptions.pointToLayer = (feature, latLng) =>
        circleMarker(latLng, {radius: 8});
  },
};
</script>
