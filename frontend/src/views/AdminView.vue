<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- <AdminHeader :show-logout="true" /> -->

    <!-- User Table -->
    <main class="flex-1 max-w-7xl w-full mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <h2 class="text-2xl font-semibold text-gray-900 mb-6">Users</h2>
        <div v-if="errorMessage" class="text-center text-sm text-red-600 mb-4">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="text-center text-sm text-green-600 mb-4">
          {{ successMessage }}
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-sm font-bold text-gray-500 uppercase tracking-wider">ID</th>
                <th class="px-6 py-3 text-left text-sm font-bold text-gray-500 uppercase tracking-wider">Company Name</th>
                <th class="px-6 py-3 text-left text-sm font-bold text-gray-500 uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-sm font-bold text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-sm font-bold text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
              <tr v-else v-for="user in users" :key="user.id">
                <td class="px-6 py-4 whitespace-nowrap text-base font-semibold text-gray-500">{{ user.id }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-base font-semibold text-gray-900">{{ user.username }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-base font-semibold text-gray-500">{{ user.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-base font-semibold">
                  <span :class="user.is_active ? 'text-green-600' : 'text-red-600'">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-base font-semibold">
                  <button
                    @click="toggleStatus(user)"
                    class="mr-4 px-2 py-1 rounded"
                    :class="user.is_active ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-green-600 text-white hover:bg-green-700'"
                    :disabled="isUpdating"
                  >
                    {{ user.is_active ? 'Deactivate' : 'Activate' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const users = ref([])
const isLoading = ref(false)
const isUpdating = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Fetch users from /api/adminfront/
const fetchUsers = async () => {
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await api.get('/api/adminfront/')
    users.value = response.data
  } catch (error) {
    console.error('Failed to fetch users:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to fetch users.'
    if (error.response?.status === 403) {
      authStore.logout('Permission denied')
      router.push('/admin')
    }
  } finally {
    isLoading.value = false
  }
}

// Toggle user status by making a POST request to /api/adminfront/
const toggleStatus = async (user) => {
  isUpdating.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await api.post('/api/adminfront/', {
      user_id: user.id,
      is_active: !user.is_active,
    })
    successMessage.value = response.data.detail
    await fetchUsers() // Refresh the user list
  } catch (error) {
    console.error('Failed to update user status:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to update user status.'
    if (error.response?.status === 403) {
      authStore.logout('Permission denied')
      router.push('/admin')
    }
  } finally {
    isUpdating.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>