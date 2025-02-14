<!-- <template>
  <router-view></router-view>
</template> -->



<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  mounted() {
    // Optional: Add a method to detect and respond to system theme changes
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Initial check
    this.handleDarkMode(darkModeMediaQuery);
    
    // Listen for changes
    darkModeMediaQuery.addListener(this.handleDarkMode);
  },
  methods: {
    handleDarkMode(e) {
      // You can add custom logic here if needed
      console.log('System dark mode is:', e.matches ? 'on' : 'off')
    }
  }
}
</script>

<style>
/* Optional: Smooth transition for dark mode */
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>