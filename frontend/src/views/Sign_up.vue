<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight">Sign up for your account</h2>
    </div>
    <div class="pt-12 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" @submit="handleSubmit" action="#" method="POST">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <label for="firstname" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">First name</label>
            <div class="mt-1">
              <input type="text" placeholder="First name" name="firstname" id="firstname" autocomplete="firstname"
                required=""
                class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" />
            </div>
          </div>
          <div class="flex-1 ml-4">
            <label for="lastname" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Last name</label>
            <div class="mt-1">
              <input type="text" placeholder="Last name" name="lastname" id="lastname" autocomplete="lastname"
                required=""
                class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" />
            </div>
          </div>
        </div>
        <div>
          <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email address</label>
          <div class="mt-2">
            <input type="email" placeholder="John@doe.com" name="email" id="email" autocomplete="email" required=""
              class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" />
          </div>
        </div>
        <div>
          <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Company Name</label>
          <div class="mt-2">
            <input type="text" placeholder="Company Name" name="username" id="username" autocomplete="username" required=""
              class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-xs-light" />
          </div>
        </div>

        <!-- Password field -->
        <div class="mb-5">
          <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
          <div class="relative">
            <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password"
              @input="checkPasswordStrength" placeholder="**** ****"
              class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              required />
            <button type="button" @click="togglePassword"
              class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 dark:text-gray-400">
              <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>

          <!-- Password Strength Indicator -->
          <div class="flex mt-2 space-x-1">
            <div v-for="(level, index) in 5" :key="index" :class="[
              'h-1.5 flex-1 rounded-full transition-all duration-300',
              index < passwordStrength ? 'bg-blue-500' : 'bg-gray-200 dark:bg-gray-700'
            ]"></div>
          </div>

          <!-- Password Requirements -->
          <div class="mt-3">
            <p class="text-sm text-gray-700 dark:text-gray-300 mb-1">
              Level: <span class="font-semibold">{{ strengthLevel }}</span>
            </p>
            <ul class="space-y-1">
              <li v-for="(requirement, index) in requirements" :key="index" class="flex items-center text-sm"
                :class="requirement.met ? 'text-green-500' : 'text-gray-500'">
                <span class="mr-2">
                  <svg v-if="requirement.met" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                    </path>
                  </svg>
                </span>
                {{ requirement.text }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Confirm Password field -->
        <div class="mb-5">
          <label for="confirmPassword" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Confirm
            Password</label>
          <div class="relative">
            <input :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword" v-model="confirmPassword"
              @input="checkPasswordMatch" placeholder="**** ****"
              class="shadow-xs bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              required />
            <button type="button" @click="toggleConfirmPassword"
              class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 dark:text-gray-400">
              <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
          <!-- Password Match Indicator -->
          <p v-if="confirmPassword" class="mt-2 text-sm" :class="passwordsMatch ? 'text-green-500' : 'text-red-500'">
            {{ passwordsMatch ? 'Passwords match' : 'Passwords do not match' }}
          </p>
        </div>

        <div class="flex items-start mb-5">
          <div class="flex items-center h-5">
            <input id="terms" type="checkbox" value=""
              class="w-4 h-4 border border-gray-300 rounded-sm bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
              required />
          </div>
          <label for="terms" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree with the <a
              href="#" class="text-blue-600 hover:underline dark:text-blue-500">terms and conditions</a></label>
        </div>

        <button type="submit"
          class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Register new account
        </button>
      </form>

      <p class="mt-10 text-center text-sm/6 text-gray-500">
        Already a member?
        {{ ' ' }}
        <a href="/" class="font-semibold text-indigo-600 hover:text-indigo-500">Login</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api' // Adjust the import path based on your project structure

const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const passwordStrength = ref(0)
const strengthLevel = ref('Empty')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// Compute if passwords match
const passwordsMatch = computed(() => {
  return password.value && confirmPassword.value && password.value === confirmPassword.value
})

// Compute if all password requirements are met
const allRequirementsMet = computed(() => {
  return requirements.every(req => req.met)
})

const requirements = reactive([
  { text: 'Minimum number of characters is 8', met: false },
  { text: 'Should contain lowercase', met: false },
  { text: 'Should contain uppercase', met: false },
  { text: 'Should contain numbers', met: false },
  { text: 'Should contain special characters', met: false }
])

const checkPasswordStrength = () => {
  const pwd = password.value
  let strength = 0

  // Reset all requirements
  requirements.forEach(req => (req.met = false))

  // Check length
  if (pwd.length >= 8) {
    strength++
    requirements[0].met = true
  }

  // Check lowercase
  if (/[a-z]/.test(pwd)) {
    strength++
    requirements[1].met = true
  }

  // Check uppercase
  if (/[A-Z]/.test(pwd)) {
    strength++
    requirements[2].met = true
  }

  // Check numbers
  if (/\d/.test(pwd)) {
    strength++
    requirements[3].met = true
  }

  // Check special characters
  if (/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) {
    strength++
    requirements[4].met = true
  }

  passwordStrength.value = strength
  strengthLevel.value = [
    'Empty',
    'Very Weak',
    'Weak',
    'Medium',
    'Strong',
    'Very Strong'
  ][strength]
}

// Toggle functions for password visibility
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

const checkPasswordMatch = () => {
  // This function triggers the computed property `passwordsMatch`
}

const handleSubmit = async (event) => {
  event.preventDefault()

  if (!allRequirementsMet.value) {
    alert('Please fulfill all password requirements before submitting')
    return
  }

  if (!passwordsMatch.value) {
    alert('Passwords do not match')
    return
  }

  try {
    const response = await api.post('/api/auth/register/', {
      username: document.getElementById('username').value,
      email: document.getElementById('email').value,
      password: password.value,
      first_name: document.getElementById('firstname').value,
      last_name: document.getElementById('lastname').value
    })
    console.log('Registration successful:', response.data)
    router.push('/') // Redirect to login after signup
  } catch (error) {
    console.error('Registration failed:', error.response?.data || error.message)
    alert('Registration failed: ' + (error.response?.data?.message || 'Server error'))
  }
}
</script>