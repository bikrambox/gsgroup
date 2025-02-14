import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import autoprefixer from 'autoprefixer'
import postcss from 'postcss'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(),],
  css: {
    postcss: {
      plugins: [
        // tailwindcss,
        autoprefixer,
      ],
    },
  },
  server: {host: '0.0.0.0',
    // proxy: {
    //   '/api': {
    //     target: 'http://localhost:8000',
    //     changeOrigin: true,
    //   },
    // },
  },
})
