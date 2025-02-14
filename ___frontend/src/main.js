import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

// Import routes
import routes from './router'

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create Pinia instance
const pinia = createPinia()

// Create and mount the Vue application
const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
