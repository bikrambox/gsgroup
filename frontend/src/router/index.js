import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth' // Assuming an auth store exists

// Define routes
const routes = [
  {
    path: '/',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  // {
  //   path: '/signup',
  //   component: () => import('../views/Sign_up.vue'),
  //   meta: { requiresAuth: false },
  // },
  {
    path: '/fileupload',
    component: () => import('../views/file_upload.vue'),
    meta: { requiresAuth: true },
    // meta: { requiresAuth: false },
  },
  {
    path: '/register',
    component: () => import('../views/Sign_up.vue'),
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guard to handle authentication and redirects
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  // If route requires auth and user is not authenticated, redirect to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/');
  } 
  // If already authenticated and trying to access login, redirect to fileupload
  else if (to.path === '/' && isAuthenticated) {
    next('/fileupload');
  } 
  // If authenticated and trying to access /register or /signup, redirect to fileupload
  else if ((to.path === '/register') && isAuthenticated) {
    next('/fileupload');
  } 
  // Proceed to the requested route
  else {
    next();
  }
});

export default router;