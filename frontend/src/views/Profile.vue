<template>
  <div class="profile-container">
    <div class="profile-card" v-if="user">
      <h2>User Profile</h2>
      
      <div class="profile-info">
        <div class="info-group">
          <label>Username</label>
          <div>{{ user.username }}</div>
        </div>
        
        <div class="info-group">
          <label>Email</label>
          <div>{{ user.email }}</div>
        </div>
        
        <div class="info-group">
          <label>Last Login</label>
          <div>{{ user.last_login_formatted }}</div>
        </div>
        
        <div class="info-group">
          <label>Account Age</label>
          <div>{{ user.account_age }}</div>
        </div>
      </div>

      <div class="change-password-section">
        <h3>Change Password</h3>
        <form @submit.prevent="handlePasswordChange">
          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input 
              type="password" 
              id="currentPassword"
              v-model="passwordForm.currentPassword"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input 
              type="password" 
              id="newPassword"
              v-model="passwordForm.newPassword"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <input 
              type="password" 
              id="confirmPassword"
              v-model="passwordForm.confirmPassword"
              required
            >
          </div>
          
          <div v-if="error" class="error">
            {{ error }}
          </div>
          
          <div v-if="success" class="success">
            {{ success }}
          </div>
          
          <button type="submit" :disabled="loading">
            {{ loading ? 'Changing Password...' : 'Change Password' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const auth = useAuthStore()
const user = ref(null)
const error = ref('')
const success = ref('')
const loading = ref(false)

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

onMounted(async () => {
  try {
    const response = await axios.get('/api/profile/', {
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    })
    user.value = response.data
  } catch (e) {
    error.value = 'Failed to load profile'
  }
})

async function handlePasswordChange() {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    error.value = 'New passwords do not match'
    return
  }
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    await axios.post('/api/profile/', {
      password: {
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword,
        confirm_password: passwordForm.value.confirmPassword
      }
    }, {
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    })
    
    success.value = 'Password changed successfully'
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to change password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.profile-info {
  margin-bottom: 2rem;
}

.info-group {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.info-group label {
  display: block;
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.change-password-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #dee2e6;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #45a049;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #dc3545;
  margin-bottom: 1rem;
}

.success {
  color: #28a745;
  margin-bottom: 1rem;
}
</style>
