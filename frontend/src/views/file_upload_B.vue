<!-- FileName: frontend\src\views\file_upload.vue -->
<template>
  <div class="max-w-md mx-auto p-6 bg-white">
    <!-- <h2 class="text-2xl font-semibold text-gray-900 mb-1">JSON File Upload:</h2> -->


    <!-- File Input with Drag-and-Drop -->
    <div
      class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center relative"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      :class="{ 'bg-blue-50': isDragging }"
    >
      <input
        type="file"
        ref="fileInput"
        @change="handleFileChange"
        class="hidden"
        accept=".json"
        multiple
      />
      <div class="flex flex-col items-center">
        <svg class="h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4-4m10 12h-6m6 0l-4 4m0-8l-4-4m-2 12V8m0 0l-4 4m4-4l4 4" />
        </svg>
        <p class="text-gray-600">Drag & Drop file here or <span @click="$refs.fileInput.click()" class="text-blue-600 cursor-pointer hover:underline">Choose file</span></p>
        <p class="text-sm text-gray-500 mt-2">Supported formats: .json • Maximum size: 10MB</p>
      </div>
    </div>

    <!-- Selected Files List -->
    <div v-if="selectedFiles.length > 0" class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 mb-2">Number of files • {{ selectedFiles.length }}</h3>
      <div v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between p-2 bg-gray-50 rounded-lg mb-2">
        <div class="flex items-center">
          <svg class="h-6 w-6 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <div>
            <p class="text-sm font-medium text-gray-900">{{ file.name }}</p>
            <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
          </div>
        </div>
        <div v-if="loading && fileProgress[index] !== undefined" class="w-1/3">
          <div class="bg-gray-200 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full" :style="{ width: `${fileProgress[index]}%` }"></div>
          </div>
          <p class="text-xs text-gray-500 text-right mt-1">{{ fileProgress[index] }}%</p>
        </div>
      </div>
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
        v-if="!loading && selectedFiles.length > 0 && !uploadComplete"
        @click="uploadFiles"
        class="mt-4 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none"
        :disabled="loading"
      >
        Upload Files
      </button>
      <div v-if="uploadComplete && !error" class="mt-4 p-2 bg-green-100 text-green-700 rounded-lg flex items-center justify-center">
        <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <p>Upload Success! {{ selectedFiles.length }} {{ selectedFiles.length === 1 ? 'file' : 'files'}} successfully uploaded!</p>
      </div>
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
const fileProgress = ref([]) // Track progress for each file
const uploadComplete = ref(false)
const error = ref(null)
const fileLocation = ref(null)
const isDragging = ref(false)

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  if (files.length === 0) {
    error.value = { message: 'No files dropped' }
    return
  }
  handleFileChange({ target: { files } })
}

const handleFileChange = (event) => {
  const files = Array.from(event.target.files || [])
  console.log('Selected files:', files)
  if (files.length === 0) {
    error.value = { message: 'No files selected' }
    return
  }
  selectedFiles.value = files
  fileProgress.value = files.map(() => 0) // Initialize progress for each file
  uploadComplete.value = false
  error.value = null
  fileLocation.value = null
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) {
    error.value = { message: 'Please select at least one file' }
    return
  }

  loading.value = true
  uploadProgress.value = 0
  fileProgress.value = selectedFiles.value.map(() => 0) // Reset progress
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
          // Simulate per-file progress (in a real scenario, you'd need per-file progress from the server)
          fileProgress.value = fileProgress.value.map(() => percentCompleted)
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
  word-break: break-all;
  padding: 0 10px;
}

/* Drag-and-drop styling */
.border-dashed:hover {
  background-color: #f0f9ff;
  transition: background-color 0.3s;
}

.bg-blue-50 {
  background-color: #f0f9ff;
}
</style>