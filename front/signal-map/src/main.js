import { createApp } from 'vue'
import App from './App.vue'
import store from './store.js'
import router from './router.js'

createApp(App).use(store,router).mount('#app')
