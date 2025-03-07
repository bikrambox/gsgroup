<!-- FileName: frontend\src\views\file_upload.vue -->

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100 dark:bg-gray-900">
    <div class="w-full max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
      <h2 class="text-center text-xl font-semibold text-gray-900 dark:text-white mb-6">File Upload</h2>

      <!-- Drag and Drop Area -->
      <div
        class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center"
        :class="{ 'border-blue-500 bg-blue-50 dark:bg-blue-900': isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleFileDrop"
      >
        <label for="file-upload" class="cursor-pointer">
          <div v-if="!selectedFile" class="flex flex-col items-center">
            <svg class="w-12 h-12 text-gray-400 dark:text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V8m0 0L3 12m4-4l4 4m6-4v8m0 0l4-4m-4 4l-4-4"></path>
            </svg>
            <p class="text-gray-500 dark:text-gray-400">Drag and drop or <span class="text-blue-600 dark:text-blue-400 hover:underline">browse</span> your files</p>
          </div>

          <!-- File Info, Progress, and Error Message -->
          <div v-if="selectedFile" class="flex flex-col items-center">
            <p class="text-gray-900 dark:text-white font-medium">{{ selectedFile.name }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ formatFileSize(selectedFile.size) }}</p>
            <div v-if="uploadProgress < 100" class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-2">
              <div
                class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                :style="{ width: `${uploadProgress}%` }"
              ></div>
            </div>
            <p v-if="uploadProgress < 100" class="text-sm text-gray-500 dark:text-gray-400 mt-1">Uploading... {{ uploadProgress }}%</p>
            <p v-if="uploadError" class="text-sm text-red-500 dark:text-red-400 mt-1">{{ uploadError }}</p>
            <p v-if="uploadProgress === 100" class="text-sm text-green-500 dark:text-green-400 mt-1">Upload complete!</p>
          </div>
        </label>
        <input
          id="file-upload"
          type="file"
          class="hidden"
          @change="handleFileSelect"
          multiple
        />
      </div>

      <!-- Done and Upload Buttons -->
      <div class="mt-6 space-x-4">
        <button
          v-if="selectedFile && uploadProgress < 100"
          @click="handleUpload"
          class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition duration-300"
          :disabled="isUploading"
        >
          <span v-if="!isUploading">Upload</span>
          <span v-else class="flex items-center justify-center">Uploading... <span class="ml-2 animate-spin h-4 w-4 border-t-2 border-b-2 border-white rounded-full"></span></span>
        </button>
        <button
          v-if="selectedFile && uploadProgress === 100"
          @click="handleDone"
          class="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 dark:focus:ring-green-400 transition duration-300"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const isDragging = ref(false)
const selectedFile = ref(null)
const uploadProgress = ref(0)
const isUploading = ref(false)
const uploadError = ref(null)

const handleFileDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    selectedFile.value = file
    uploadProgress.value = 0
    uploadError.value = null
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    uploadProgress.value = 0
    uploadError.value = null
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const handleUpload = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadError.value = null
  const formData = new FormData()
  formData.append('files', selectedFile.value) // Changed from 'file' to 'files' to match backend expectation

  try {
    const response = await api.post('/api/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        uploadProgress.value = percentCompleted
      },
    })
    uploadProgress.value = 100
    console.log('Upload successful:', response.data)
  } catch (error) {
    uploadError.value = 'Upload failed: ' + (error.response?.data?.error || error.message)
    uploadProgress.value = 0
    console.error('Upload error:', error)
  } finally {
    isUploading.value = false
  }
}

const handleDone = () => {
  selectedFile.value = null
  uploadProgress.value = 0
  uploadError.value = null
  console.log('File upload completed')
}
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>