<!-- FileName: frontend\src\App.vue -->

<template>
  <div>
    <!-- Add Navbar globally -->
    <Navbar />
    
    <!-- Main content area for routed views -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import Navbar from './views/Navbar.vue' // Import the Navbar component

// Existing script logic for dark mode
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
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
</style>