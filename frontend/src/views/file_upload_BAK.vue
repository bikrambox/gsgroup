<!-- FileName: frontend\src\views\file_upload.vue -->
<template>
  <div class="max-w-md mx-auto p-6 bg-white">
    <h2 class="text-2xl font-semibold text-gray-900 mb-1">JSON File Upload:</h2>
    <p class="text-gray-600">File size limit: 10MB</p>
    
    
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
      <p v-if="uploadComplete && fileLocation" class="mt-2 text-gray-600 location-text">
        Location: "{{ fileLocation }}"
      </p>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
      <h3 class="font-semibold">Upload Failed</h3>
      <ul v-if="Array.isArray(error.results)" class="list-disc pl-5 mt-2">
        <li v-for="(result, index) in error.results" :key="index">
          <strong>File:</strong> {{ result.filename || 'Unknown' }}<br>
          <strong>Status:</strong> {{ result.status || 'error' }}<br>
          <strong>Message:</strong> {{ result.message || error.message || 'Unknown error occurred' }}
        </li>
      </ul>
      <p v-else class="mt-2">{{ error.message || 'Unknown error occurred' }}</p>
      <p v-if="error.user" class="mt-2"><strong>User:</strong> {{ error.user }}</p>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index'

const fileInput = ref(null)
const selectedFiles = ref([])
const loading = ref(false)
const uploadProgress = ref(0)
const uploadComplete = ref(false)
const error = ref(null)
const fileLocation = ref(null)

const handleFileChange = (event) => {
  const files = Array.from(event.target.files || [])
  console.log('Selected files:', files)
  if (files.length === 0) {
    error.value = { message: 'No files selected' }
    return
  }
  selectedFiles.value = files
  uploadComplete.value = false
  error.value = null
  fileLocation.value = null
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
    if (file && typeof file.name === 'string' && !file.name.toLowerCase().endsWith('.json')) {
      error.value = { message: `File ${file.name} is not a JSON file` }
      loading.value = false
      return
    }
    if (file) formData.append('files', file)
  })

  if (error.value) return

  try {
    console.log('Sending request to:', `${import.meta.env.VITE_API_URL}/api/upload/`)
    const response = await api.post('/api/upload/', formData, {
      timeout: 30000,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadProgress.value = percentCompleted
          console.log(`Upload progress: ${percentCompleted}%`)
        }
      },
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.status === 200) {
      if (response.data.message === 'File upload processing completed' && response.data.results) {
        const hasError = response.data.results.some(result => result.status === 'error')
        if (hasError) {
          error.value = response.data
        } else {
          uploadComplete.value = true
          fileLocation.value = response.data.results[0]?.ftp_path || 'Location not provided'
        }
      } else {
        throw new Error('Unexpected response format')
      }
    } else if (response.status === 400) {
      error.value = response.data
    } else {
      throw new Error(`Upload request failed with status ${response.status}`)
    }
  } catch (err) {
    console.error('Upload failed:', err)
    error.value = err.response?.data || {
      message: 'Upload failed due to an unexpected error',
      results: [{ status: 'error', message: err.message }]
    }
  } finally {
    loading.value = false
    fileInput.value.value = null
  }
}

onMounted(() => {
  console.log('API URL:', import.meta.env.VITE_API_URL)
})
</script>
<style scoped>
/* Ensure the location text is centered and has proper spacing */
.location-text {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
  word-break: break-all; /* Prevent long paths from overflowing */
  padding: 0 10px; /* Add some padding for better readability */
}

/* Optional: Adjust the container if needed */
/* .max-w-md {
  display: flex;
  flex-direction: column;
  align-items: center;
} */
</style>