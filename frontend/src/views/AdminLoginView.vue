<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- <AdminHeader :show-logout="false" /> -->

    <div class="flex-1 flex items-center justify-center">
      <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <div class="text-center">
          <h2 class="text-3xl font-bold text-gray-900">Admin Login</h2>
          <p class="mt-2 text-gray-600">Please sign in to continue</p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                v-model="email"
                id="email"
                type="email"
                required
                autofocus
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input
                v-model="password"
                id="password"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
            </div>
            <div class="flex items-center">
              <input
                v-model="rememberMe"
                id="remember-me"
                type="checkbox"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              >
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>
          </div>

          <div v-if="errorMessage" class="text-center text-sm text-red-600">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            class="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Signing In...' : 'Sign In' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

onMounted(() => {
  // Check if credentials are stored in localStorage
  const storedEmail = localStorage.getItem('rememberedEmail')
  const storedPassword = localStorage.getItem('rememberedPassword')

  if (storedEmail && storedPassword) {
    email.value = storedEmail
    password.value = storedPassword
    rememberMe.value = true
  }
})

// const handleLogin = async () => {
//   errorMessage.value = ''
//   isLoading.value = true

//   try {
//     const success = await authStore.login(email.value, password.value)
//     if (success) {
//       // Handle "Remember Me" functionality
//       if (rememberMe.value) {
//         localStorage.setItem('rememberedEmail', email.value)
//         localStorage.setItem('rememberedPassword', password.value)
//       } else {
//         localStorage.removeItem('rememberedEmail')
//         localStorage.removeItem('rememberedPassword')
//       }

//       // Check if the user is a superuser
//       if (authStore.user?.is_staff) {
//         router.push('/admin-dashboard')
//       } else {
//         errorMessage.value = 'You do not have admin access.'
//         authStore.logout('Not a superuser')
//       }
//     } else {
//       errorMessage.value = 'Login failed: Invalid email or password.'
//     }
//   } catch (error) {
//     errorMessage.value = 'Login failed: Server error.'
//     console.error('Login error:', error)
//   } finally {
//     isLoading.value = false
//   }
// }


const handleLogin = async () => {
  errorMessage.value = '';
  isLoading.value = true;

  try {
    const success = await authStore.login(email.value, password.value);
    if (success) {
      if (rememberMe.value) {
        localStorage.setItem('rememberedEmail', email.value);
        localStorage.setItem('rememberedPassword', password.value);
      } else {
        localStorage.removeItem('rememberedEmail');
        localStorage.removeItem('rememberedPassword');
      }

      console.log('Checking is_staff:', authStore.user?.profile_summary?.is_staff);
      if (authStore.user?.profile_summary?.is_staff) { // Check is_staff instead of is_superuser
        router.push('/admindashboard');
      } else {
        errorMessage.value = 'You do not have admin access.';
        authStore.logout('Not a superuser');
      }
    } else {
      errorMessage.value = 'Login failed: Invalid email or password.';
    }
  } catch (error) {
    errorMessage.value = 'Login failed: Server error.';
    console.error('Login error:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>