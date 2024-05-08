import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  build: {
    target: "es2022"
  },
  esbuild: {
    target: "es2022"
  },
  optimizeDeps:{
    esbuildOptions: {
      target: "es2022",
    },
    include: [
      "vue-google-maps-community-fork",
      "fast-deep-equal",
    ],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  define: {
    'process.env.VITE_GOOGLE_API_KEY': `"${process.env.VITE_GOOGLE_API_KEY}"`,
    'process.env.VITE_GOOGLE_API_MAP_ID': `"${process.env.VITE_GOOGLE_API_MAP_ID}"`
  }
})
