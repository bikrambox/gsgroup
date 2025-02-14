<template>
  <Navbar />
  <Intro />
</template>


<script>
import Navbar from './Navbar.vue'
import Intro from './Intro.vue'

export default {
  name: 'app',
  components: {
    Navbar,
    Intro
  }
}
</script>