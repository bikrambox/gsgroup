<!-- FileName: frontend\src\views\Home.vue -->

<template>
  <div class="min-h-screen dark:bg-gray-800 dark:text-slate-50">
    <Intro />
  </div>
</template>

<script>
import Intro from './Intro.vue'

export default {
  name: 'Home',
  components: {
    Intro
  }
}
</script>