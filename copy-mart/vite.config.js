import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import backendWatchdog from './scripts/backend-watchdog.js'
// import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    backendWatchdog(),
    // vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: ['.js', '.ts', '.jsx', '.tsx', '.vue', '.json']
  },
  server: {
    host: true,
    port: 5173
  },
  envDir: '../',
})
