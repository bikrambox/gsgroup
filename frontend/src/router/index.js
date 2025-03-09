// FileName: frontend\src\router\index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import SignUp from '../views/Sign_up.vue'
import FileUpload from '../views/file_upload.vue'

// Define routes
const routes = [
  {
    path: '/',
    component: () => import('../views/Home.vue'), // Dynamic import
  },
  {
    path: '/login',
    component: () => import('../views/Login.vue'), // Dynamic import
  },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
  },
  {
    path: '/signup',
    component: () => import('../views/Sign_up.vue'),
  },
  {
    path: '/fileupload', // Changed from '/file-upload' to '/fileupload'
    component: () => import('../views/file_upload.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router