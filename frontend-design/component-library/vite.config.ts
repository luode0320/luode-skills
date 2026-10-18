import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import pearlMock from './mock/server.mjs'

const apiProxyTarget = process.env.VITE_API_PROXY_TARGET || 'http://localhost:8080'
// 默认走本地 mock（零后端可跑）；设 VITE_MOCK=off 回退真实后端代理
const useMock = process.env.VITE_MOCK !== 'off'

export default defineConfig({
  plugins: [vue(), ...(useMock ? [pearlMock()] : [])],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/api': {
        target: apiProxyTarget,
        changeOrigin: true,
      },
    },
  },
})
