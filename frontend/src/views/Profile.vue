<template>
  <div class="w-full max-w-10/10 max-[500px]:max-w-10/10 mx-auto flex-row items-center" :class="{ 'dark': isDarkMode }">
  <!-- <div class=" flex-row items-center" :class="{ 'dark': isDarkMode }"> -->
    <div class="w-full max-[500px]:flex-col flex justify-between items-center ">
      <div class="w-full max-[500px]:mb-3 max-[500px]:mt-3 max-[500px]:pl-3">
        <h1 class="text-lg font-semibold">Nomeco</h1>
      </div>

      
      <!-- <div class="max-[500px]:w-full w-2/4 max-[500px]:block mx-auto max-[500px]:px-1"> -->
      <div class="max-[500px]:w-full w-3/4 max-[500px]:block mx-auto max-[500px]:px-1">
        <form class="w-full mx-auto p-2" @submit="handleSearch">
          <div class="relative">
            <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400 dark:text-gray-500" aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
              </svg>
            </div>
            <input 
              type="search" 
              id="search"
              v-model="searchQuery"
              @input="handleSearchInput"
              class="block w-full p-3 ps-10 rounded-xl text-sm bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-800 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 outline-none transition duration-300 ease-in-out"
              placeholder="Search in all columns..." 
            />
            <button type="submit"
              class="absolute end-1.5 bottom-1.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm px-4 py-1.5 transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500">
              Search
            </button>
          </div>
        </form>
      </div>




    </div>
  </div>
  <div class="w-full max-w-10/10 max-[500px]:max-w-10/10 mx-auto h-auto shadow-md ">
    <div class="overflow-x-auto max-h-[calc(100vh-300px)] sm:rounded-lg rounded">
      <!-- Adjust the subtraction value as needed -->

      <div v-if="isLoading" class="flex justify-center items-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="error" class="text-red-500 text-center py-4">
        {{ error }}
        <button @click="fetchTableData" class="ml-2 text-blue-600 hover:text-blue-700">Try again</button>
      </div>

      <table v-else class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 whitespace-normal relative">
        <thead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400 sticky top-0 z-10">
          <tr>
            <th v-for="header in tableHeaders" :key="header.key" scope="col" class="p-4 whitespace-nowrap bg-gray-100 dark:bg-gray-700">
              {{ header.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in paginatedData" :key="row.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
            <td v-for="header in tableHeaders" 
                :key="header.key" 
                class="p-4 align-top"
                :class="header.class"
            >
              <div :class="{
                'font-semibold': header.key === 'id',
                'whitespace-pre-line break-words max-w-[300px]': header.key !== 'createdAt',
                'whitespace-nowrap': header.key === 'createdAt',
                'line-clamp-4 hover:line-clamp-none': header.key === 'description'
              }">
                {{ formatCellContent(row[header.key], header.key) }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div
        class="flex justify-between w-full max-w-9/10 max-[425px]:max-w-10/10 mx-auto items-center px-4 py-3 fixed bottom-0 left-0 right-0 ">
        <div class="flex items-center justify-between w-full">
          <div class="flex items-center gap-4">
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
              Showing
              <span class="font-semibold text-gray-900 dark:text-white">{{ ((currentPage - 1) * itemsPerPage) + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredData.length) }}</span>
              of
              <span class="font-semibold text-gray-900 dark:text-white">{{ filteredData.length }}</span>
            </span>
            <div class="flex items-center gap-2">
              <label for="itemsPerPage" class="text-sm text-gray-500 dark:text-gray-400">Show:</label>
              <select
                id="itemsPerPage"
                v-model="itemsPerPage"
                @change="handleItemsPerPageChange($event.target.value)"
                class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm rounded-lg border border-gray-300 dark:border-gray-700 focus:ring-blue-500 focus:border-blue-500 p-1"
              >
                <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>
          <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8">
            <li>
              <a href="#" @click.prevent="previousPage"
                class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
                :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }">
                Previous
              </a>
            </li>
            <li v-for="page in totalPages" :key="page">
              <a href="#" @click.prevent="goToPage(page)"
                class="flex items-center justify-center px-3 h-8 leading-tight border"
                :class="[
                  currentPage === page 
                    ? 'text-blue-600 border-gray-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white'
                    : 'text-gray-500 bg-white border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'
                ]">
                {{ page }}
              </a>
            </li>
            <li>
              <a href="#" @click.prevent="nextPage"
                class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
                :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }">
                Next
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isDarkMode = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(25)
const itemsPerPageOptions = [25, 50, 75, 100]
const searchQuery = ref('')

// Table headers definition
const tableHeaders = ref([
  { key: 'id', label: 'ID' },
  { key: 'title', label: 'Title' },
  { key: 'description', label: 'Description' },
  { key: 'brand', label: 'Brand' },
  { key: 'sku', label: 'SKU' },
  { key: 'category', label: 'Category' },
  { key: 'price', label: 'Price' },
  { key: 'stock', label: 'Stock' },
  { key: 'rating', label: 'Rating' },
  { key: 'createdAt', label: 'Created At', class: 'whitespace-nowrap' }
])

// Initialize empty table data
const tableData = ref([])
const isLoading = ref(false)
const error = ref(null)

// Function to fetch data from API
const fetchTableData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch('https://dummyjson.com/products')
    if (!response.ok) {
      throw new Error('Failed to fetch data')
    }
    const data = await response.json()
    tableData.value = data.products.map(product => ({
      ...product,
      createdAt: new Date().toISOString() // Since API doesn't provide createdAt
    }))
  } catch (err) {
    error.value = err.message
    console.error('Error fetching data:', err)
  } finally {
    isLoading.value = false
  }
}

// Fetch data when component mounts
onMounted(() => {
  fetchTableData()
})

const handleItemsPerPageChange = (value) => {
  itemsPerPage.value = Number(value)
  currentPage.value = 1
}

// Computed property for filtered data
const filteredData = computed(() => {
  if (!searchQuery.value) return tableData.value
  
  const query = searchQuery.value.toLowerCase()
  return tableData.value.filter(item => {
    // Check all fields in the item
    return Object.entries(item).some(([key, value]) => {
      if (value === null || value === undefined) return false
      return value.toString().toLowerCase().includes(query)
    })
  })
})

// Update paginatedData to use filteredData instead of tableData
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredData.value.slice(start, end)
})

// Update totalPages to use filteredData
const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage.value))

// Handle search submit
const handleSearch = (e) => {
  e.preventDefault()
  currentPage.value = 1 // Reset to first page when searching
}

// Handle search input
const handleSearchInput = (e) => {
  searchQuery.value = e.target.value
  currentPage.value = 1 // Reset to first page when search query changes
}

// Format cell content based on the type of data
const formatCellContent = (content, key) => {
  if (content === null || content === undefined) return ''
  
  switch (key) {
    case 'price':
      return `$${content}`
    case 'description':
      return content.length > 300 
        ? content.slice(0, 300).split(' ').slice(0, -1).join(' ') + '...'
        : content
    case 'createdAt':
      return new Date(content).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    default:
      return content.toString()
  }
}

// Pagination methods
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>

<style>
/* Global scrollbar styles */
:root {
  color-scheme: light dark;
}

/* Light mode scrollbar (default) */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background-color: #e5e7eb;
  /* light gray */
}

::-webkit-scrollbar-thumb {
  background-color: #6b7280;
  /* medium gray */
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #4b5563;
  /* darker gray */
}

/* Dark mode scrollbar */
@media (prefers-color-scheme: dark) {
  ::-webkit-scrollbar-track {
    background-color: #374151;
    /* dark gray */
  }

  ::-webkit-scrollbar-thumb {
    background-color: #9ca3af;
    /* lighter gray */
  }

  ::-webkit-scrollbar-thumb:hover {
    background-color: #6b7280;
    /* medium gray */
  }
}

/* Firefox scrollbar */
* {
  scrollbar-width: auto;
  scrollbar-color: #6b7280 #e5e7eb;
  /* light mode */
}

@media (prefers-color-scheme: dark) {
  * {
    scrollbar-color: #9ca3af #1F2937;
    /* dark mode */
  }
}
</style>