import axios from 'axios';

const API_URL = 'http://127.0.0.1:8001';

export default {
  async getProperties() {
    try {
      const response = await axios.get(`${API_URL}/signal/properties`);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  },

  async sendMarkerData(lat, lng, text, selectedProperties) {
    try {
      const token = localStorage.getItem("token");
      const headers = {
        Authorization: `Bearer ${token}`
      };
      const data = {
        latitude: lat,
        longitude: lng,
        text,
        properties: selectedProperties,
        city_id: 1,
        time_of_incident: new Date().toISOString()
      };
      const response = await axios.post(`${API_URL}/signal/send`, data, { headers });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  },

  async anonymousLogin() {
    try {
      const response = await axios.post(`${API_URL}/auth/anonymous/login`);
      localStorage.setItem("token", response.data.token);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  },

  async getGeoData() {
    try {
      const response = await axios.get(`${API_URL}/geo`);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
};
