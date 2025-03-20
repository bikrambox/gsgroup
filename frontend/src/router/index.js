// // frontend/src/router/index.js
// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '../stores/auth'

// const routes = [
//   {
//     path: '/',
//     component: () => import('../views/Login.vue'),
//   },
//   {
//     path: '/register',
//     component: () => import('../views/Sign_up.vue'),
//   },
//   {
//     path: '/adminlogin',
//     component: () => import('../views/AdminLoginView.vue'),
//   },
//   {
//     path: '/admindashboard',
//     component: () => import('../views/AdminView.vue'),
//     meta: { requiresAuth: true, requiresAdmin: true },
//   },
//   {
//     path: '/fileupload',
//     component: () => import('../views/file_upload.vue'),
//     meta: { requiresAuth: true },
//   },
// ]

// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// })

// router.beforeEach(async (to, from, next) => {
//   const authStore = useAuthStore()
//   await authStore.checkAuth()
//   const isAuthenticated = authStore.isAuthenticated
//   const isAdmin = authStore.user?.profile_summary?.is_staff || false

//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next('/')
//   } else if (to.meta.requiresAdmin && (!isAuthenticated || !isAdmin)) {
//     next('/adminlogin')
//   } else if (to.path === '/' && isAuthenticated) {
//     next('/fileupload')
//   } else if (to.path === '/register' && isAuthenticated) {
//     next('/fileupload')
//   } else if (to.path === '/adminlogin' && isAuthenticated && isAdmin) {
//     next('/admindashboard')
//   } else {
//     next()
//   }
// })

// export default router


// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/fileupload',
    component: () => import('../views/file_upload.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/register',
    component: () => import('../views/Sign_up.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/adminlogin',
    component: () => import('../views/AdminLoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/admindashboard',
    component: () => import('../views/AdminView.vue'),
    meta: { requiresAuth: true, requiresSuperuser: true }, // Require superuser access
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  await authStore.checkAuth(); // Wait for token validation
  const isAuthenticated = authStore.isAuthenticated;
  // const isSuperuser = authStore.user?.is_superuser || false; // Check if the user is a superuser
  const isAdmin = authStore.user?.profile_summary?.is_staff || false; // Check is_staff instead of is_superuser

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/'); // Redirect to login if not authenticated
  } else if (to.meta.requiresSuperuser && (!isAuthenticated || !isAdmin)) {
    next('/adminlogin'); // Redirect to admin login if not a superuser
  } else if (to.path === '/' && isAuthenticated) {
    next('/fileupload'); // Redirect authenticated users to fileupload
  } else if (to.path === '/register' && isAuthenticated) {
    next('/fileupload'); // Redirect authenticated users to fileupload
  } else if (to.path === '/adminlogin' && isAuthenticated && isAdmin) {
    next('/admindashboard'); // Redirect authenticated superusers to admin dashboard
  } else {
    next();
  }
});

export default router;