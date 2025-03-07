// FileName: frontend\src\main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'

// Import the router instance
import router from './router'

// Create Pinia instance
const pinia = createPinia()

// Create and mount the Vue application
const app = createApp(App)
app.use(pinia)
app.use(router) // Use the imported router instance
app.mount('#app')