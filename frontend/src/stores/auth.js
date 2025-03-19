// FileName: frontend\src\stores\auth.js

import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),

  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },

  actions: {
    async login(email, password) {
      try {
        await api.post('/api/auth/login/', {
          email,
          password
        })
        this.isAuthenticated = true
        await this.fetchUserProfile()
        return true
      } catch (error) {
        console.error('Login failed in auth store:', error.response?.data || error.message)
        this.isAuthenticated = false
        return false
      }
    },

    async fetchUserProfile() {
      try {
        const response = await api.get('/api/auth/profile/')
        this.user = response.data
      } catch (error) {
        console.error('Failed to fetch user profile:', error.response?.data || error.message)
        this.isAuthenticated = false
        this.user = null
      }
    },

    async logout() {
      try {
        await api.post('/api/auth/logout/')
        this.user = null
        this.isAuthenticated = false
      } catch (error) {
        console.error('Logout failed:', error.response?.data || error.message)
      }
    }
  }
})