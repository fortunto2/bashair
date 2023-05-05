import { createStore } from 'vuex';
import axios from "axios";

//API_URL
const API_URL = 'http://localhost:8001';

const store = createStore({
  state() {
    return {
      properties: [],
      geoData: [],
      markers: [],
      selectedProperties: [],
      selectedMarker: null,
      token: null,
    };
  },
  mutations: {
    setProperties(state, properties) {
      state.properties = properties;
    },
    setGeoData(state, geoData) {
      state.geoData = geoData;
    },
    setMarkers(state, markers) {
      state.markers = markers;
    },
    setSelectedProperties(state, selectedProperties) {
      state.selectedProperties = selectedProperties;
    },
    setSelectedMarker(state, selectedMarker) {
      state.selectedMarker = selectedMarker;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    async getProperties({ commit }) {
      try {
        const response = await axios.get(`${API_URL}/signal/properties`);
        commit('setProperties', response.data);
      } catch (error) {
        console.error(error);
      }
    },
    async getGeoData({ commit }) {
      try {
        const response = await axios.get(`${API_URL}/geo`);
        commit('setGeoData', response.data);
      } catch (error) {
        console.error(error);
      }
    },
    async anonymousLogin({ commit }) {
      try {
          const response = await axios.post(`${API_URL}/auth/anonymous/login`);
        commit('setToken', response.data.token);
      } catch (error) {
        console.error(error);
      }
    },
    // async sendMarkerData({ state }, { lat, lng, text }) {
    //   // Your implementation here
    // },
  },
});

export default store;
