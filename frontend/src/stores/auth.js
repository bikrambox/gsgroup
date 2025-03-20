// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'
import api from '../api'

// Helper function to decode JWT and check expiration
const decodeToken = (token) => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload;
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
};

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    logoutReason: null,
    hasLoggedOut: localStorage.getItem('hasLoggedOut') === 'true',
    tokenCheckInterval: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !state.hasLoggedOut,
  },

  actions: {
    startTokenCheckTimer() {
      if (this.tokenCheckInterval) {
        clearInterval(this.tokenCheckInterval);
      }
      this.tokenCheckInterval = setInterval(() => {
        if (this.hasLoggedOut || !this.refreshToken) {
          console.log('Stopping token check timer: User is logged out or no refresh token');
          clearInterval(this.tokenCheckInterval);
          this.tokenCheckInterval = null;
          return;
        }
        const tokenPayload = decodeToken(this.refreshToken);
        if (!tokenPayload) {
          console.error('Invalid refresh token format - logging out');
          this.logout('Invalid refresh token');
          return;
        }
        const currentTime = Math.floor(Date.now() / 1000);
        if (tokenPayload.exp < currentTime) {
          console.log('Refresh token has expired - logging out automatically', {
            exp: tokenPayload.exp,
            currentTime
          });
          this.logout('Refresh token expired');
          // Dispatch a custom event to notify the app to redirect
          window.dispatchEvent(new CustomEvent('token-expired'));
        }
      }, 1000);
    },

    stopTokenCheckTimer() {
      if (this.tokenCheckInterval) {
        console.log('Stopping token check timer');
        clearInterval(this.tokenCheckInterval);
        this.tokenCheckInterval = null;
      }
    },

    async checkAuth() {
      if (this.hasLoggedOut) {
        console.log('Skipping checkAuth: User has logged out');
        return false;
      }
      if (this.accessToken) {
        console.log('Checking authentication with access token:', this.accessToken);
        const tokenPayload = decodeToken(this.accessToken);
        if (!tokenPayload) {
          console.error('Invalid access token format');
          this.logout('Invalid access token');
          return false;
        }
        const currentTime = Math.floor(Date.now() / 1000);
        if (tokenPayload.exp < currentTime) {
          console.log('Access token has expired', {
            exp: tokenPayload.exp,
            currentTime
          });
          const refreshed = await this.refreshAccessToken();
          if (refreshed) {
            await this.fetchUserProfile();
            return true;
          } else {
            this.logout('Token expired or invalid');
            return false;
          }
        }
        try {
          await this.fetchUserProfile();
          return true;
        } catch (error) {
          console.error('Token validation failed:', error.response?.data || error.message);
          const refreshed = await this.refreshAccessToken();
          if (refreshed) {
            await this.fetchUserProfile();
            return true;
          } else {
            this.logout('Token expired or invalid');
            return false;
          }
        }
      }
      console.log('No access token available for authentication');
      return false;
    },

    async login(username, password) {
      try {
        const response = await api.post('/api/auth/token/', {
          username,
          password
        });
        console.log('Login response:', response.data);
        this.accessToken = response.data.access;
        this.refreshToken = response.data.refresh;
        localStorage.setItem('accessToken', this.accessToken);
        localStorage.setItem('refreshToken', this.refreshToken);
        this.hasLoggedOut = false;
        localStorage.setItem('hasLoggedOut', 'false');
        await this.fetchUserProfile();
        this.startTokenCheckTimer();
        return true;
      } catch (error) {
        console.error('Login failed in auth store:', error.response?.data || error.message);
        return false;
      }
    },

    async fetchUserProfile() {
      try {
        const response = await api.get('/api/profile/');
        this.user = response.data;
        console.log('User profile fetched:', this.user);
      } catch (error) {
        console.error('Failed to fetch user profile:', error.response?.data || error.message);
        throw error;
      }
    },

    async refreshAccessToken() {
      if (this.hasLoggedOut) {
        console.log('Skipping token refresh: User has logged out');
        return false;
      }
      if (!this.refreshToken) {
        console.error('No refresh token available');
        return false;
      }
      const tokenPayload = decodeToken(this.refreshToken);
      if (!tokenPayload) {
        console.error('Invalid refresh token format');
        this.logout('Invalid refresh token');
        return false;
      }
      const currentTime = Math.floor(Date.now() / 1000);
      if (tokenPayload.exp < currentTime) {
        console.error('Refresh token has expired', {
          exp: tokenPayload.exp,
          currentTime
        });
        this.logout('Refresh token expired');
        return false;
      }
      console.log('Attempting to refresh token with:', {
        refreshToken: this.refreshToken,
        tokenPayload
      });
      try {
        const refreshApi = axios.create({
          baseURL: import.meta.env.VITE_API_URL,
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const response = await refreshApi.post('/api/auth/token/refresh/', {
          refresh: this.refreshToken
        });
        console.log('Refresh token response:', {
          newAccessToken: response.data.access,
          newRefreshToken: response.data.refresh || 'No new refresh token provided'
        });
        this.accessToken = response.data.access;
        localStorage.setItem('accessToken', this.accessToken);
        if (response.data.refresh) {
          this.refreshToken = response.data.refresh;
          localStorage.setItem('refreshToken', this.refreshToken);
        }
        this.logoutReason = null;
        return true;
      } catch (error) {
        console.error('Failed to refresh token:', error.response?.data || error.message);
        this.logout('Refresh token expired or invalid');
        return false;
      }
    },

    logout(reason = null) {
      console.log('Before logout - localStorage state:', {
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        hasLoggedOut: localStorage.getItem('hasLoggedOut')
      });
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      this.logoutReason = reason;
      this.hasLoggedOut = true;
      localStorage.setItem('hasLoggedOut', 'true');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      console.log('After logout - localStorage state:', {
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        hasLoggedOut: localStorage.getItem('hasLoggedOut')
      });
      if (localStorage.getItem('accessToken') || localStorage.getItem('refreshToken')) {
        console.warn('Tokens were not properly cleared from localStorage');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
      this.stopTokenCheckTimer();
    }
  }
});