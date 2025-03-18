<template>
  <nav ref="navRef" class="bg-gray-200 dark:bg-gray-900 text-gray-900 dark:text-gray-400 sticky top-0 left-0 right-0 z-50">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <!-- Mobile menu button -->
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <button @click.stop="isMobileMenuOpen = !isMobileMenuOpen" class="relative inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-50 hover:text-white focus:outline-none cursor-pointer">
            <span class="sr-only">Open main menu</span>
            <svg v-if="!isMobileMenuOpen" class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Desktop Navigation -->
        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <!-- Desktop Menu Items -->
          <div class="hidden sm:ml-6 sm:block">
            <div class="flex space-x-4">
              <template v-for="item in navigation" :key="item.name">
                <!-- Regular menu items -->
                <button v-if="!item.hasDropdown" @click="handleItemClick(item.name)" :class="[item.current ? 'bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700', 'rounded-md px-3 py-2 text-sm font-medium cursor-pointer']">
                  {{ item.name }}
                </button>

                <!-- Dropdown menu -->
                <div v-else class="relative inline-block text-left" @mouseenter="hoveredDropdown = item.name" @mouseleave="hoveredDropdown = null">
                  <button class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700 cursor-pointer">
                    {{ item.name }}
                    <svg class="ml-2 -mr-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>

                  <div v-show="hoveredDropdown === item.name" class="absolute left-0 z-10 w-48 origin-top-right bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-md shadow-lg">
                    <div>
                      <button v-for="subItem in item.subItems" :key="subItem.name" @click="handleItemClick(subItem.name)" class="block w-full text-left px-4 py-2 text-sm font-medium hover:bg-gray-300 dark:hover:bg-gray-700 cursor-pointer">
                        {{ subItem.name }}
                      </button>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- User menu -->
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <button v-if="route.path !== '/' && route.path !== '/fileupload'" type="button" @click="handleItemClick('Log In')" class="relative rounded-md text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700 px-3 mr-1 py-2 text-sm font-medium cursor-pointer">
            Login
          </button>
          <button v-if="route.path !== '/register' && route.path !== '/fileupload'" type="button" @click="handleItemClick('Register')" class="relative rounded-md text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700 px-3 ml-1 py-2 text-sm font-medium cursor-pointer">
            Register
          </button>
          <!-- Profile dropdown -->
          <div v-if="route.path === '/fileupload' || authStore.isAuthenticated" class="relative ml-3" @mouseenter="hoveredDropdown = 'profile'" @mouseleave="hoveredDropdown = null">
            <button class="relative flex rounded-full bg-gray-50 dark:bg-gray-800 text-sm cursor-pointer">
              <img class="h-8 w-8 rounded-full" src="https://w7.pngwing.com/pngs/859/761/png-transparent-user-heroicons-solid-icon.png" alt="Profile" />
            </button>

            <div v-show="hoveredDropdown === 'profile'" class="absolute right-0 z-10 w-48 origin-top-right py-2 bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-lg shadow-lg">
              <button v-for="item in profileDropdownItems" :key="item.name" @click="item.action" class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-300 dark:hover:bg-gray-700 cursor-pointer">
                {{ item.name }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-show="isMobileMenuOpen" class="sm:hidden absolute top-16 inset-x-0 z-50 bg-gray-50 dark:bg-gray-800 shadow-md">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <template v-for="item in navigation" :key="item.name">
          <!-- Regular menu items -->
          <button v-if="!item.hasDropdown" @click="handleItemClick(item.name)" class="block w-full text-left rounded-md px-3 py-2 text-base font-medium" :class="[item.current ? 'bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer']">
            {{ item.name }}
          </button>

          <!-- Dropdown items -->
          <div v-else class="space-y-1">
            <button @click="item.isOpen = !item.isOpen" class="flex w-full items-center justify-between rounded-md px-3 py-2 text-base font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer">
              <span>{{ item.name }}</span>
              <svg class="ml-2 h-5 w-5" :class="{ 'rotate-180': item.isOpen }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <div v-show="item.isOpen" class="ml-3">
              <button v-for="subItem in item.subItems" :key="subItem.name" @click="handleItemClick(subItem.name)" class="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer">
                {{ subItem.name }}
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const hoveredDropdown = ref(null)
const isMobileMenuOpen = ref(false)
const navRef = ref(null)
const tooltipPosition = ref('left')
const isDarkMode = ref(true)
const router = useRouter()
const route = useRoute() // Added to track current route
const authStore = useAuthStore()

const updateTooltipPosition = () => {
  if (window.innerWidth < 640) {
    tooltipPosition.value = 'bottom'
  } else {
    tooltipPosition.value = 'left'
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
  window.addEventListener('resize', updateTooltipPosition)
  updateTooltipPosition()
  const savedDarkMode = localStorage.getItem('darkMode')
  isDarkMode.value = savedDarkMode !== null ? savedDarkMode === 'true' : true
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
  window.removeEventListener('resize', updateTooltipPosition)
})

const handleItemClick = (itemName) => {
  console.log(`${itemName} item clicked`)
  if (itemName === 'Sign out') {
    handleLogout()
  } else if (itemName === 'Log In') {
    router.push('/')
  } else if (itemName === 'Register') {
    router.push('/register')
  } else if (itemName === 'Home') {
    router.push('/') // Redirect to root path (/)
  } else {
    console.log(`Navigating to ${itemName}`)
  }
  isMobileMenuOpen.value = false // Close mobile menu after click
}

const resetDropdowns = () => {
  navigation.value.forEach(item => {
    if (item.hasDropdown) {
      item.isOpen = false
    }
  })
}

const handleClickOutside = (event) => {
  if (navRef.value && !navRef.value.contains(event.target)) {
    isMobileMenuOpen.value = false
    resetDropdowns()
  }
}

watch(isMobileMenuOpen, (newValue) => {
  if (!newValue) {
    resetDropdowns()
  }
})

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('darkMode', isDarkMode.value)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

// Dynamically compute the navigation items based on auth status and current route
const navigation = computed(() => {
  const navItems = [
    { name: 'Home', href: '/', current: route.path === '/' },
  ]

  return navItems
})

const profileDropdownItems = computed(() => [
  {
    name: authStore.isAuthenticated ? 'Sign out' : 'Log In',
    action: () => handleItemClick(authStore.isAuthenticated ? 'Sign out' : 'Log In')
  },
])
</script>