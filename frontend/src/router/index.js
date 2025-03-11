import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth' // Assuming an auth store exists

// Define routes
const routes = [
  // {
  //   path: '/',
  //   component: () => import('../views/Home.vue'),
  //   meta: { requiresAuth: false },
  // },
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
  {
    path: '/signup',
    component: () => import('../views/Sign_up.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/fileupload',
    component: () => import('../views/file_upload.vue'),
    // meta: { requiresAuth: false },
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guard to handle authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated; // Assuming this method exists

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next('/');
  } else if (to.path === '/' && isAuthenticated) {
    // If already authenticated and trying to access login, redirect to fileupload
    next('/fileupload');
  } else {
    next();
  }
});

export default router;