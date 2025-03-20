<!-- FileName: frontend\src\App.vue

<template>
  <div>
    <Navbar />
    <router-view></router-view>
  </div>
</template>

<script setup>
import Navbar from './views/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { onMounted, onUnmounted } from 'vue'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.checkAuth() // Check authentication status on app load

  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  handleDarkMode(darkModeMediaQuery)
  darkModeMediaQuery.addEventListener('change', handleDarkMode)
})

onUnmounted(() => {
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  darkModeMediaQuery.removeEventListener('change', handleDarkMode)
})

const handleDarkMode = (e) => {
  console.log('System dark mode is:', e.matches ? 'on' : 'off')
}
</script>

<style>
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style> -->




<!-- 
// frontend/src/App.vue
<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth';
import Navbar from './views/Navbar.vue'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    // Listen for the token-expired event
    window.addEventListener('token-expired', () => {
      console.log('Token expired event received - redirecting to login');
      router.push('/');
    });

    return {
      authStore,
    };
  },
};
</script>

<style>
/* Your styles */
</style> -->



<!-- frontend/src/App.vue -->
<template>
  <div class=" min-h-screen">
    <Navbar />
    <router-view></router-view>
  </div>
</template>

<script setup>
import Navbar from './views/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import { onMounted, onUnmounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

// Function to handle token expiration and redirect
const handleTokenExpired = () => {
  console.log('Token expired event received - redirecting to login')
  router.push('/')
}

onMounted(async () => {
  // Check authentication status on app load
  await authStore.checkAuth()

  // Set up dark mode handling
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  handleDarkMode(darkModeMediaQuery)
  darkModeMediaQuery.addEventListener('change', handleDarkMode)

  // Listen for the token-expired event
  window.addEventListener('token-expired', handleTokenExpired)
})

onUnmounted(() => {
  // Clean up dark mode event listener
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  darkModeMediaQuery.removeEventListener('change', handleDarkMode)

  // Clean up token-expired event listener
  window.removeEventListener('token-expired', handleTokenExpired)
})

const handleDarkMode = (e) => {
  console.log('System dark mode is:', e.matches ? 'on' : 'off')
}
</script>