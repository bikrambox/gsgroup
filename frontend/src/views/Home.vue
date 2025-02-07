<template>
  <div class="home">
    <header>
      <div id="account">
        <div v-if="isAuthenticated">
          <div id="auth">
            Authenticated as "{{ user.username }}" &lt;{{ user.email }}&gt;
          </div>
        </div>
        <div v-else>
          <form id="logio" action="/login" method="get">
            <input type="hidden" name="continue" v-model="currentPath">
            <a class="login" href="#" @click.prevent="handleLogin">Login</a>
          </form>
        </div>
      </div>
      <h1>Care4all API</h1>
    </header>

    <main>
      <nav>
        <ul>
          <li><a href="documentation">Documentation</a></li>
          <li><a class="login" href="#" @click.prevent="handleLogin">Login</a></li>
        </ul>
      </nav>
      <article>
        <section>
          <p v-if="isAuthenticated">Hello, {{ user.username }}!</p>
          <p v-else>Welcome!</p>
          <p v-if="!isAuthenticated">Please <a class="login" href="#" @click.prevent="handleLogin">Login</a>!</p>
        </section>
      </article>
    </main>

    <footer>© {{ currentYear }} Flextrack ApS</footer>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)
const user = computed(() => auth.user)
const currentYear = new Date().getFullYear()
const currentPath = ref(window.location.href)

function handleLogin(event) {
  event.preventDefault()
  router.push('/login')
}
</script>

<style>
.home {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', system-ui;
}

header {
  margin-bottom: 30px;
}

#account {
  text-align: right;
  margin-bottom: 20px;
}

#logio {
  display: inline;
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

nav li {
  display: inline;
  margin-right: 15px;
}

a.login {
  color: #0066cc;
  text-decoration: none;
}

a.login:hover {
  text-decoration: underline;
}

footer {
  margin-top: 40px;
  text-align: center;
  color: #666;
}

article section {
  margin: 20px 0;
}
</style>
