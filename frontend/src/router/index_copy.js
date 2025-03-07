// frontend\src\router\index.js
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import FileUpload from '../views/file_upload.vue' // Add this import

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/file-upload', // Add this route
    name: 'FileUpload',
    component: FileUpload
  }
]

export default routes