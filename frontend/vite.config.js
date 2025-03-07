// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'  //Corrected Import.
import autoprefixer from 'autoprefixer'

export default defineConfig({
  plugins: [vue(), tailwindcss()], // TailwindCSS plugin
  css: {
    postcss: {
      plugins: [autoprefixer],
    },
  },
  server: {
    host: '0.0.0.0',  // Listen on all network interfaces (important for Docker/VMs)
    port: 4430,       // The port Vite's dev server runs on
    proxy: {          // Proxy API requests to your Django backend
      '/api': {
        target: 'http://localhost:8000', // Your Django server
        changeOrigin: true,   // Needed for virtual hosted sites
        secure: false,      // If your Django backend doesn't use HTTPS locally
      },
    },
    // Crucial for allowing access from your domain:
    allowedHosts: [
      'vps1139.basicserver.io', // Explicitly allow your domain
       //'localhost',              // You might also want localhost
        // Add more specific allowed host if desired, or use:
        // 'all',  //This allows all hosts
    ],
  },
  build: {
    outDir: 'dist',        // Output directory for production builds
    assetsDir: 'assets',   // Subdirectory for assets within dist
    sourcemap: true,      // Generate sourcemaps for debugging
  },
})
