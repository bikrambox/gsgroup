<!-- FileName: frontend\src\views\Home.vue -->

<template>
  <div class="min-h-screen dark:bg-gray-800 dark:text-slate-50">
    <Login />
  </div>
</template>

<script>
import Login from './Login.vue'

export default {
  name: 'Home',
  components: {
    Login
  }
}
</script>