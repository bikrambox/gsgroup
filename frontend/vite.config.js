import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import autoprefixer from 'autoprefixer'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  css: {
    postcss: {
      plugins: [autoprefixer],
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173, // Default Vite port, adjust if needed
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
  },
})