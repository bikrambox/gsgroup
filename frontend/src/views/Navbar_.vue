<template>
  <nav ref="navRef"
    class="bg-gray-200 dark:bg-gray-900 text-gray-900 dark:text-gray-400 sticky top-0 left-0 right-0 z-50">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <!-- Mobile menu button -->
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <button @click.stop="isMobileMenuOpen = !isMobileMenuOpen"
            class="relative inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-50 hover:text-white focus:outline-none">
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
          <!-- Logo -->
          <!-- <div class="flex shrink-0 items-center">
            <img class="h-8 w-auto" src="https://tailwindui.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
              alt="BHS logistics" />
          </div> -->

          <!-- Desktop Menu Items -->
          <div class="hidden sm:ml-6 sm:block">
            <div class="flex space-x-4">
              <template v-for="item in navigation" :key="item.name">
                <!-- Regular menu items -->
                <button v-if="!item.hasDropdown" @click="handleItemClick(item.name)"
                  :class="[item.current ? 'bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700', 'rounded-md px-3 py-2 text-sm font-medium']">
                  {{ item.name }}
                </button>

                <!-- Dropdown menu -->
                <div v-else class="relative inline-block text-left" @mouseenter="hoveredDropdown = item.name"
                  @mouseleave="hoveredDropdown = null">
                  <button
                    class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700">
                    {{ item.name }}
                    <svg class="ml-2 -mr-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>

                  <div v-show="hoveredDropdown === item.name"
                    class="absolute left-0 z-10 w-48 origin-top-right bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-md shadow-lg">
                    <div class="">
                      <button v-for="subItem in item.subItems" :key="subItem.name"
                        @click="handleItemClick(subItem.name)"
                        class="block w-full text-left px-4 py-2 text-sm font-medium hover:bg-gray-300 dark:hover:bg-gray-700">
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
          <!-- Dark Mode Toggle -->
          <button @click="toggleDarkMode"
            class="group relative rounded-full p-1 text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700 mr-2">
            <!-- Sun icon for dark mode -->
            <svg v-if="isDarkMode" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <!-- Moon icon for light mode -->
            <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <!-- Bell Icon -->
          <div class="relative">
            <button type="button"
              class="group relative rounded-full  dark:bg-gray-800 p-1 text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700"
              @mouseenter="hoveredDropdown = 'bell'" @mouseleave="hoveredDropdown = null">
              <span class="sr-only">View notifications</span>
              <svg
                class="h-6 w-6 stroke-gray-900 dark:stroke-gray-50 group-hover:stroke-gray-700 dark:group-hover:stroke-gray-300"
                fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>

            <div v-show="hoveredDropdown === 'bell'" role="tooltip" :class="[
              'absolute z-10 inline-block px-3 py-2 text-sm font-medium bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-lg shadow-lg',
              tooltipPosition === 'bottom' ? 'top-full mt-2 left-1/2 -translate-x-1/2' : 'top-1/2 -translate-y-1/2 right-full mr-2'
            ]">
              Notifications
              <div :class="[
                'absolute w-2 h-2 bg-gray-200 dark:bg-gray-900 rotate-45',
                tooltipPosition === 'bottom' ? '-top-1 left-1/2 -translate-x-1/2' : 'right-[-4px] top-1/2 -translate-y-1/2'
              ]"></div>
            </div>
          </div>

          <!-- Profile dropdown -->
          <div class="relative ml-3" @mouseenter="hoveredDropdown = 'profile'" @mouseleave="hoveredDropdown = null">
            <button class="relative flex rounded-full bg-gray-50 dark:bg-gray-800 text-sm">
              <img class="h-8 w-8 rounded-full"
                
                src="https://w7.pngwing.com/pngs/859/761/png-transparent-user-heroicons-solid-icon.png"
                alt="" />
            </button>

            <div v-show="hoveredDropdown === 'profile'"
              class="absolute right-0 z-10 w-48 origin-top-right py-2 bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-lg shadow-lg">
              <div class="">
                <!-- <button @click="handleItemClick('Profile')"
                  class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-300 dark:hover:bg-gray-700">
                  Your Profile
                </button>
                <button @click="handleItemClick('Settings')"
                  class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-300 dark:hover:bg-gray-700">
                  Settings
                </button> -->
                <!-- <button @click="handleItemClick('Sign out')"
                  class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-300 dark:hover:bg-gray-700">
                  Sign out
                </button> -->

                <div v-show="hoveredDropdown === 'profile'"
                  class="absolute right-0 z-10 w-48 origin-top-right py-2 bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50 rounded-lg shadow-lg">
                  <div class="">
                    <button v-for="item in profileDropdownItems" :key="item.name" @click="item.action"
                      class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-300 dark:hover:bg-gray-700">
                      {{ item.name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-show="isMobileMenuOpen"
      class="sm:hidden absolute top-16 inset-x-0 z-50 bg-gray-50 dark:bg-gray-800 shadow-md">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <template v-for="item in navigation" :key="item.name">
          <!-- Regular menu items -->
          <button v-if="!item.hasDropdown" @click="handleItemClick(item.name)"
            class="block w-full text-left rounded-md px-3 py-2 text-base font-medium"
            :class="[item.current ? 'bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700']">
            {{ item.name }}
          </button>

          <!-- Dropdown items -->
          <div v-else class="space-y-1">
            <button @click="item.isOpen = !item.isOpen"
              class="flex w-full items-center justify-between rounded-md px-3 py-2 text-base font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700">
              <span>{{ item.name }}</span>
              <svg class="ml-2 h-5 w-5" :class="{ 'rotate-180': item.isOpen }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>

            <div v-show="item.isOpen" class="ml-3">
              <button v-for="subItem in item.subItems" :key="subItem.name" @click="handleItemClick(subItem.name)"
                class="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700">
                {{ subItem.name }}
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<!-- <script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const hoveredDropdown = ref(null)
const isMobileMenuOpen = ref(false)
const isProfileOpen = ref(false)
const navRef = ref(null)
const tooltipPosition = ref('left') // changed default position to left
const isDarkMode = ref(true) // Set default to dark mode

const updateTooltipPosition = () => {
  if (window.innerWidth < 640) { // sm breakpoint
    tooltipPosition.value = 'bottom'
  } else {
    tooltipPosition.value = 'left'
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
  window.addEventListener('resize', updateTooltipPosition)
  updateTooltipPosition() // Initial position
  
  // Set initial dark mode from localStorage or default to true
  const savedDarkMode = localStorage.getItem('darkMode')
  isDarkMode.value = savedDarkMode !== null ? savedDarkMode === 'true' : true
  
  // Apply initial dark mode
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
}

// Reset all dropdown states
const resetDropdowns = () => {
  navigation.value.forEach(item => {
    if (item.hasDropdown) {
      item.isOpen = false
    }
  })
}

const handleClickOutside = (event) => {
  // Check if the click is outside the nav element and not on the menu button
  if (navRef.value && !navRef.value.contains(event.target)) {
    isMobileMenuOpen.value = false
    resetDropdowns() // Reset dropdowns when mobile menu closes
  }
}

// Watch for mobile menu state changes
watch(isMobileMenuOpen, (newValue) => {
  if (!newValue) {
    resetDropdowns() // Reset dropdowns when mobile menu is closed
  }
})

// Toggle dark mode
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  // Update document class for dark mode
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  // Save preference to localStorage
  localStorage.setItem('darkMode', isDarkMode.value)
}

const navigation = ref([
  { name: 'Dashboard', href: '#', current: true },
  { name: 'Team', href: '#', current: false },
  {
    name: 'Projects',
    href: '#',
    current: false,
    hasDropdown: true,
    isOpen: false,
    subItems: [
      { name: 'Nomeco', href: '#' },
      { name: 'Novonordis', href: '#' }
    ]
  },
  {
    name: 'Jester',
    href: '#',
    current: false,
    hasDropdown: true,
    isOpen: false,
    subItems: [
      { name: 'TT', href: '#' },
      { name: 'TXT', href: '#' }
    ]
  },
  { name: 'Calendar', href: '#', current: false }
])
</script> -->


<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth' // Import auth store

const hoveredDropdown = ref(null)
const isMobileMenuOpen = ref(false)
const navRef = ref(null)
const tooltipPosition = ref('left')
const isDarkMode = ref(true)
const router = useRouter()
const authStore = useAuthStore() // Access auth store

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
  } else {
    // Handle other clicks (e.g., Profile, Settings)
    console.log(`Navigating to ${itemName}`)
  }
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
  authStore.logout() // Clear auth state
  router.push('/login') // Redirect to login after logout
}

// Dynamically compute the navigation items based on auth status
const navigation = ref([
  { name: 'Home', href: '/', current: true },
  // { name: 'Team', href: '#', current: false },
  {
    name: 'Projects',
    href: '#',
    current: false,
    hasDropdown: true,
    isOpen: false,
    subItems: [
      { name: 'Nomeco', href: '#' },
      { name: 'Novonordis', href: '#' }
    ]
  },
  {
    name: 'Jester',
    href: '#',
    current: false,
    hasDropdown: true,
    isOpen: false,
    subItems: [
      { name: 'TT', href: '#' },
      { name: 'TXT', href: '#' }
    ]
  },
  { name: 'Calendar', href: '#', current: false }
])

// Computed property to dynamically adjust the profile dropdown
const profileDropdownItems = computed(() => [
  // { name: 'Your Profile', action: () => handleItemClick('Profile') },
  // { name: 'Settings', action: () => handleItemClick('Settings') },
  {
    name: authStore.isAuthenticated ? 'Sign out' : 'Log In',
    action: () => handleItemClick(authStore.isAuthenticated ? 'Sign out' : 'Log In')
  },
])
</script>