import { fileURLToPath, URL } from 'node:url'
import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://aisales-back-release-shicms.ns-jj1vgrim.svc.cluster.local:8000',
        changeOrigin: true,
        timeout: 30000,
        secure: false,
        onError: (err, req, res) => {
          console.error('代理错误:', err);
        }
      },
      '/images': {
        target: 'http://aisales-back-release-shicms.ns-jj1vgrim.svc.cluster.local:8000',
        changeOrigin: true,
        timeout: 30000,
        secure: false,
        rewrite: (path) => path.replace(/^\/images/, '')
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  }
})
