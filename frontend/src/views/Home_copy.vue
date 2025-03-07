<template>
  <div class="min-h-screen dark:bg-gray-800 dark:text-slate-50">
  <!-- <div class="min-h-screen "> -->
    <!-- <Navbar /> -->
    <!-- <Navbar_ /> -->
     <!-- <Navbar_clone /> -->
    <Login />
    <!-- <Sign_up /> -->
    <!-- <Intro /> -->
    <!-- <Profile /> -->
    <!-- <Footer /> -->
     <!-- <Dashboard /> -->
  </div>
</template>


<script>
import Navbar from './Navbar.vue'
import Login from './Login.vue'
import Sign_up from './Sign_up.vue'
import Intro from './Intro.vue'
import Profile from './Profile.vue'
import Footer from './Footer.vue'
import Dashboard from './Dashboard.vue'
import Navbar_clone from './Navbar_clone.vue'
import Navbar_ from './Navbar_.vue'

export default {
  name: 'app',
  components: {
    Navbar,
    Navbar_,
    Navbar_clone,
    Login,
    Sign_up,
    Intro,
    Profile,
    Footer,
    Dashboard
  }
}
</script>