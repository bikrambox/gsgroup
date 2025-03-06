// frontend/src/api/index.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/',  // Remove the /api/ to avoid duplication
    withCredentials: true,  // Enable credentials (cookies, authorization headers) for CSRF
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');  // Or wherever you store your JWT
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    // Get CSRF token from cookies if available
    const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
}, error => Promise.reject(error));

export default api;