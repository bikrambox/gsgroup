<!-- FileName: frontend\src\views\file_upload.vue -->
<template>
  <div class="max-w-2xl mx-auto p-6 bg-white">
    <!-- File Input with Drag-and-Drop -->
    <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center relative mt-4"
      @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop"
      :class="{ 'bg-blue-50': isDragging }">
      <input type="file" ref="fileInput" @change="handleFileChange" class="hidden" accept=".json" multiple />
      <div class="flex flex-col items-center">
        <svg class="h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M7 16V4m0 0L3 8m4-4l4-4m10 12h-6m6 0l-4 4m0-8l-4-4m-2 12V8m0 0l-4 4m4-4l4 4" />
        </svg>
        <p class="text-gray-600">Drag & Drop file here or <span @click="$refs.fileInput.click()"
            class="text-blue-600 cursor-pointer hover:underline">Choose file</span></p>
        <p class="text-sm text-gray-500 mt-2">Supported formats: .json • Maximum size: 10MB</p>
      </div>
    </div>

    <!-- Selected Files List -->
    <div v-if="selectedFiles.length > 0" class="mt-4">
      <p class="text-sm text-gray-600">Number of files: {{ selectedFiles.length }}</p>
      <div v-for="(file, index) in selectedFiles" :key="index"
        class="flex items-center justify-between p-2 bg-gray-50 rounded-lg mb-2">
        <div class="flex items-center">
          <svg class="h-6 w-6 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path style="fill:#FBA026;" d="M442.879,325.778c3.298,97.524-89.057,175.55-186.879,175.514
	c-97.822,0.037-190.177-77.991-186.879-175.514c0.2-48.649,58.399-127.918,104.417-194.489C221.442,64.634,257.168,10.675,256,10.71
	c-1.168-0.033,34.558,53.924,82.462,120.58C384.481,197.86,442.679,277.13,442.879,325.778z" />
            <path style="fill:#EB4E49;" d="M235.174,499.169c65.086,12.728,229.971-90.253,28.638-291.586c0,0,3.472,96.025-38.184,159.678
	c0,0-3.472-34.134-41.655-75.211C183.974,292.05,83.575,469.523,235.174,499.169z" />
            <g>
              <path style="fill:#231F20;" d="M315.475,155.523c-3.357-4.87-10.025-6.095-14.894-2.74c-4.869,3.355-6.096,10.024-2.74,14.893
		c38.163,55.369,61.206,89.91,68.49,102.664c1.977,3.459,5.59,5.399,9.309,5.399c1.8,0,3.626-0.455,5.301-1.411
		c5.136-2.933,6.921-9.475,3.988-14.61C377.346,246.442,353.979,211.386,315.475,155.523z" />
              <path style="fill:#231F20;"
                d="M287.765,115.48c-3.369-4.858-10.042-6.067-14.902-2.697s-6.067,10.042-2.697,14.903l0.772,1.112
		c2.08,3.003,5.417,4.612,8.812,4.612c2.103,0,4.229-0.618,6.089-1.906c4.862-3.369,6.073-10.039,2.705-14.901L287.765,115.48z" />
              <path style="fill:#231F20;" d="M453.586,325.573c-0.302-47.909-48.229-116.819-94.579-183.464
		c-3.971-5.708-7.896-11.353-11.736-16.908c-0.037-0.054-0.075-0.107-0.113-0.16C301.761,61.874,270.569,14.82,266.134,7.16
		c-0.177-0.484-0.395-0.974-0.661-1.472c-1.816-3.408-5.337-5.572-9.167-5.682c-4.069-0.137-7.877,2.099-9.786,5.694
		c-0.261,0.493-0.478,0.978-0.652,1.455c-4.435,7.658-35.631,54.72-81.025,117.883c-0.039,0.054-0.076,0.107-0.114,0.16
		c-3.841,5.557-7.767,11.202-11.737,16.911c-46.35,66.645-94.276,135.554-94.578,183.463
		c-1.476,44.935,16.197,88.793,49.773,123.511c38.105,39.401,93.331,62.919,147.736,62.918c0.047,0,0.095,0,0.141,0
		c54.414,0,109.644-23.519,147.75-62.921C437.39,414.365,455.062,370.508,453.586,325.573z M237.229,488.66L237.229,488.66
		c-34.07-6.663-56.782-21.833-67.505-45.09c-19.976-43.33,3.916-105.081,16.618-132.371c25.463,32.02,28.606,56.931,28.632,57.147
		c0.459,4.512,3.71,8.246,8.118,9.32c4.402,1.071,9.011-0.744,11.495-4.54c29.726-45.426,37.505-105.351,39.425-139.395
		c69.346,75.93,92.189,145.705,64.286,198.111C315.42,474.815,264.019,493.903,237.229,488.66z M388.42,434.192
		c-15.586,16.116-34.367,29.255-54.807,38.791c9.533-9.241,17.552-19.733,23.593-31.078c15.854-29.775,18.359-65.254,7.248-102.599
		c-12.991-43.665-44.304-90.532-93.068-139.296c-3.111-3.11-7.807-3.998-11.843-2.246c-4.035,1.755-6.585,5.802-6.43,10.199
		c0.029,0.822,2.211,73.554-24.595,131.844c-6.184-14.624-17.194-34.065-36.699-55.048c-2.325-2.501-5.699-3.745-9.093-3.344
		c-3.391,0.398-6.389,2.39-8.07,5.363c-2.267,4.006-55.157,98.894-24.4,165.709c1.047,2.274,2.186,4.479,3.397,6.631
		c-10.896-7.228-21.024-15.571-30.068-24.922C94.041,403.649,78.5,365.275,79.824,326.14c0.003-0.106,0.005-0.211,0.006-0.318
		c0.17-41.248,48.29-110.439,90.745-171.484c3.962-5.697,7.88-11.332,11.715-16.878c28.003-38.966,49.198-69.895,59.343-84.869
		c5.542-8.178,10.435-15.499,14.367-21.49c3.932,5.992,8.826,13.314,14.367,21.493c10.143,14.969,31.335,45.893,59.342,84.865
		c3.835,5.547,7.753,11.181,11.715,16.878c42.455,61.046,90.576,130.235,90.746,171.485c0,0.106,0.002,0.212,0.006,0.318
		C433.5,365.273,417.961,403.647,388.42,434.192z" />
              <path style="fill:#231F20;" d="M307.898,338.94c-5.594,1.919-8.573,8.009-6.654,13.603c7.227,21.07,7.737,39.367,1.515,54.382
		c-5.965,14.395-17.065,23.755-25.327,29.071c-4.973,3.2-6.41,9.827-3.21,14.799c2.046,3.181,5.494,4.915,9.014,4.915
		c1.984,0,3.992-0.552,5.785-1.705c10.831-6.97,25.44-19.375,33.522-38.883c8.28-19.983,7.928-43.376-1.042-69.529
		C319.582,339.999,313.493,337.022,307.898,338.94z" />
            </g>
          </svg>
          <div>
            <p class="text-sm font-medium text-gray-900">{{ file.name }}</p>
            <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
          </div>
        </div>
        <div class="flex items-center">
          <div v-if="loading && fileProgress[index] !== undefined" class="w-1/3 mr-4">
            <div class="bg-gray-200 rounded-full h-2">
              <div class="bg-blue-600 h-2 rounded-full" :style="{ width: `${fileProgress[index]}%` }"></div>
            </div>
            <p class="text-xs text-gray-500 text-right mt-1">{{ fileProgress[index] }}%</p>
          </div>
          <button
            @click="removeFile(index)"
            class="text-red-600 hover:text-red-800 focus:outline-none"
            title="Remove file"
            :disabled="loading"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
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
      <button v-if="!loading && selectedFiles.length > 0 && !uploadComplete" @click="uploadFiles"
        class="mt-4 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none"
        :disabled="loading">
        Upload Files
      </button>
      <div v-if="uploadComplete && !error"
        class="mt-4 p-2 bg-green-100 text-green-700 rounded-lg flex items-center justify-center">
        <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <p>Upload Success! {{ uploadedFileCount }} {{ uploadedFileCount === 1 ? 'file' : 'files' }} successfully uploaded!</p>
      </div>
      <div v-if="uploadComplete && !error && fileLocations.length > 0" class="mt-2 text-gray-600 location-container">
        <p v-for="(location, index) in fileLocations" :key="index" class="location-text break-all">
          Location: "{{ location }}"
        </p>
      </div>
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
      <!-- Add a timer to auto-dismiss the duplicate error -->
      <div v-if="error.isDuplicateError" class="mt-2">
        <p class="text-sm text-gray-600">This message will disappear in {{ errorDismissTimer }} seconds.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import api from '../api/index'

const fileInput = ref(null)
const selectedFiles = ref([])
const loading = ref(false)
const uploadProgress = ref(0)
const fileProgress = ref([]) // Track progress for each file
const uploadComplete = ref(false)
const error = ref(null)
const fileLocation = ref(null)
const fileLocations = ref([]) // Array to store multiple FTP paths
const isDragging = ref(false)
const uploadedFileCount = ref(0) // New ref to store the number of uploaded files
const errorDismissTimer = ref(5) // Timer for auto-dismissing duplicate error
let errorDismissInterval = null // Store the interval ID for cleanup

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
  appendFiles(files)
}

const handleFileChange = (event) => {
  const files = Array.from(event.target.files || [])
  console.log('Selected files from input:', files)
  // Only process if files are selected, otherwise do nothing
  if (files.length > 0) {
    appendFiles(files)
  } else {
    console.log('No files selected from input, ignoring...')
    // Do not set error here to avoid crashing the process
  }
}

const appendFiles = (files) => {
  // Filter out duplicates by file name
  const newFiles = files.filter(file => !selectedFiles.value.some(existingFile => existingFile.name === file.name))
  const duplicateFiles = files.filter(file => selectedFiles.value.some(existingFile => existingFile.name === file.name))

  if (duplicateFiles.length > 0) {
    const duplicateNames = duplicateFiles.map(file => file.name).join(', ')
    error.value = {
      message: `Duplicate Files: ${duplicateNames}`,
      isDuplicateError: true // Flag to identify this as a duplicate error
    }
    // Reset and start a new timer to auto-dismiss the duplicate error after 5 seconds
    errorDismissTimer.value = 5
    if (errorDismissInterval) clearInterval(errorDismissInterval) // Clear any existing interval
    errorDismissInterval = setInterval(() => {
      errorDismissTimer.value -= 1
      if (errorDismissTimer.value <= 0) {
        clearInterval(errorDismissInterval)
        if (error.value && error.value.isDuplicateError) {
          error.value = null // Clear the error if it's a duplicate error
        }
      }
    }, 1000)
  }

  if (newFiles.length === 0 && duplicateFiles.length > 0) {
    return // No new files to add, and duplicates are handled with error
  }

  // Append new files to the existing list
  if (newFiles.length > 0) {
    selectedFiles.value = [...selectedFiles.value, ...newFiles]
    fileProgress.value = selectedFiles.value.map(() => 0) // Update progress array
    uploadComplete.value = false
    if (!error.value || !error.value.isDuplicateError) {
      error.value = null // Clear non-duplicate errors
    }
    fileLocation.value = null
  }
}

// Function to remove a file from the list
const removeFile = (index) => {
  selectedFiles.value.splice(index, 1) // Remove the file at the given index
  fileProgress.value.splice(index, 1) // Update the progress array
  if (selectedFiles.value.length === 0) {
    error.value = null // Clear any error messages if no files remain
  }
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
    error.value = { message: 'No files selected' }
    return
  }

  // Clear any duplicate error before proceeding with the upload
  if (error.value && error.value.isDuplicateError) {
    error.value = null
    clearInterval(errorDismissInterval) // Stop the timer
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

  if (error.value && !error.value.isDuplicateError) return

  try {
    console.log('Sending request to:', `${import.meta.env.VITE_API_URL}/api/upload/`)
    const response = await api.post('/api/upload/', formData, {
      timeout: 30000,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadProgress.value = percentCompleted
          // Simulate per-file progress
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
          // Store the number of successfully uploaded files
          uploadedFileCount.value = response.data.results.length
          // Extract FTP paths for all successful uploads
          fileLocations.value = response.data.results.map(result => result.ftp_path)
          // Clear the selected files list
          selectedFiles.value = []
          fileProgress.value = []
          // Revert to upload button after 5 seconds
          setTimeout(() => {
            uploadComplete.value = false
            fileLocations.value = []
            uploadedFileCount.value = 0 // Reset the count after the message disappears
          }, 5000)
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

// Cleanup the interval on component unmount to prevent memory leaks
onBeforeUnmount(() => {
  if (errorDismissInterval) {
    clearInterval(errorDismissInterval)
  }
})

onMounted(() => {
  console.log('API URL:', import.meta.env.VITE_API_URL)
})
</script>

<style scoped>
/* Center the entire component in the middle of the screen */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* Full viewport height */
  background-color: #f7fafc;
  /* Match the background color from the screenshot */
  padding: 1rem;
  /* Add padding to prevent sticking to edges on small screens */
}

/* Ensure the inner container (max-w-3xl) doesn't stretch too much */
.max-w-3xl {
  width: 100%;
  max-width: 48rem;
  /* Match the width from the screenshot */
}

/* Styling for location display */
.location-container {
  text-align: center;
}

.location-text {
  margin: 0.25rem 0;
  /* Add small margin between multiple locations */
  word-break: break-all;
  /* Ensure long paths wrap properly */
  padding: 0 10px;
  max-width: 100%;
}

/* Drag-and-drop styling */
.border-dashed:hover {
  background-color: #f0f9ff;
  transition: background-color 0.3s;
}

.bg-blue-50 {
  background-color: #f0f9ff;
}

/* Ensure file list items stack properly */
.mb-2 {
  margin-bottom: 0.5rem;
}

/* Styling for delete button */
button:disabled svg {
  stroke: #d1d5db; /* Gray out the icon when disabled */
}
</style>