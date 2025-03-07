// FileName: frontend\src\router\index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import SignUp from '../views/Sign_up.vue'
import FileUpload from '../views/file_upload.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/login', component: Login },
  { path: '/signup', component: SignUp },
  { path: '/file-upload', component: FileUpload },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router