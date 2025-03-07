<!-- FileName: frontend\src\App.vue -->

<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  mounted() {
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    this.handleDarkMode(darkModeMediaQuery)
    darkModeMediaQuery.addListener(this.handleDarkMode)
  },
  methods: {
    handleDarkMode(e) {
      console.log('System dark mode is:', e.matches ? 'on' : 'off')
    }
  }
}
</script>

<style>
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>