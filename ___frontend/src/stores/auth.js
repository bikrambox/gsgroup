import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token')
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('/api/token/', {
          username,
          password
        })
        
        this.token = response.data.access
        localStorage.setItem('token', this.token)
        
        // Fetch user profile
        await this.fetchUserProfile()
        
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },
    
    async fetchUserProfile() {
      try {
        const response = await axios.get('/api/profile/', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        this.user = response.data
      } catch (error) {
        console.error('Failed to fetch user profile:', error)
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
