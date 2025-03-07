<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-semibold text-gray-900 mb-4">File Upload</h2>
    
    <!-- File Input -->
    <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
      <input
        type="file"
        ref="fileInput"
        @change="handleFileChange"
        class="hidden"
        accept=".json"
        multiple
      />
      <button
        @click="$refs.fileInput.click()"
        class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none"
        :disabled="loading"
      >
        Choose File(s)
      </button>
      <p v-if="selectedFiles.length > 0" class="mt-2 text-gray-600">
        Selected: {{ selectedFiles.map(f => f.name).join(', ') }}
      </p>
      <p v-if="uploadProgress > 0" class="mt-2 text-gray-600">Upload Progress: {{ uploadProgress }}%</p>
    </div>

    <!-- Spinner and Status -->
    <div class="mt-4 text-center">
      <div v-if="loading" class="flex justify-center">
        <svg class="animate-spin h-6 w-6 text-green-600" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
      </div>
      <button
        v-if="!loading && selectedFiles.length > 0"
        @click="uploadFiles"
        class="mt-4 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none"
        :disabled="loading"
      >
        Upload
      </button>
      <p v-if="uploadComplete && !error" class="mt-2 text-green-600">Upload to FTP complete!</p>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
      <h3 class="font-semibold">Upload Failed</h3>
      <ul class="list-disc pl-5 mt-2">
        <li v-for="(result, index) in error.results" :key="index">
          <strong>File:</strong> {{ result.filename }}<br>
          <strong>Status:</strong> {{ result.status }}<br>
          <strong>Message:</strong> {{ result.message || 'Unknown error occurred' }}
        </li>
      </ul>
      <p v-if="error.user" class="mt-2"><strong>User:</strong> {{ error.user }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/index'

const fileInput = ref(null)
const selectedFiles = ref([])
const loading = ref(false)
const uploadProgress = ref(0)
const uploadComplete = ref(false)
const error = ref(null)

const handleFileChange = (event) => {
  selectedFiles.value = Array.from(event.target.files)
  uploadComplete.value = false
  error.value = null
}

const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) {
    error.value = { message: 'Please select at least one file' }
    return
  }

  loading.value = true
  uploadProgress.value = 0
  const formData = new FormData()
  selectedFiles.value.forEach(file => {
    if (!file.name.toLowerCase().endsWith('.json')) {
      error.value = { message: 'Please upload only JSON files' }
      loading.value = false
      return
    }
    formData.append('files', file)
  })

  if (error.value) return

  try {
    const response = await api.post('/api/upload/', formData, {
      timeout: 30000, // 30 seconds timeout
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        uploadProgress.value = percentCompleted
      }
    })

    if (response.data.message === 'File upload processing completed' && response.data.results) {
      const hasError = response.data.results.some(result => result.status === 'error')
      if (hasError) {
        error.value = response.data
      } else {
        uploadComplete.value = true
      }
    } else {
      throw new Error('Unexpected response format')
    }
  } catch (err) {
    console.error('Upload failed:', err)
    error.value = err.response?.data || {
      message: 'Upload failed due to an unexpected error',
      results: [{ status: 'error', message: err.message }]
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Add any custom styles if needed */
</style>