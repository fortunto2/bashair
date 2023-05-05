<template>
  <div id="sidebar">
    <div v-if="showSidebar">
      <h2>Create Signal</h2>
      <form id="create-signal-form">
        <label for="text">Message:</label>
        <input type="text" v-model="message" id="text">
        <br>
        <br>

        <label for="properties">What do you feel:</label>
        <div id="properties-checkboxes">
          <div class="properties" v-for="property in properties" :key="property.id">
            <input type="checkbox" v-model="selectedProperties" :value="property.id">
            <label>{{ property.name }}</label>
          </div>
        </div>
        <br>

        <button type="submit" @click.prevent="submitSignal">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: '',
      properties: [],
      selectedProperties: []
    }
  },
  props: {
    showSidebar: Boolean,
    marker: Object
  },
  methods: {
    async fetchProperties() {
      try {
        const response = await axios.get('http://127.0.0.1:8001/signal/properties')
        this.properties = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async submitSignal() {
      const lat = this.marker.getLatLng().lat
      const lng = this.marker.getLatLng().lng
      const text = this.message
      const selectedProperties = this.selectedProperties

      try {
        const response = await axios.post('http://127.0.0.1:8001/signal/send', {
          latitude: lat,
          longitude: lng,
          text,
          properties: selectedProperties,
          city_id: 1,
          time_of_incident: new Date().toISOString()
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        console.log(response)
      } catch (error) {
        console.error(error)
      }
    }
  },
  created() {
    this.fetchProperties()
  }
}
</script>

<style scoped>
  #sidebar {
    background-color: white;
    padding: 20px;
  }
</style>
