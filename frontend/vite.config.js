import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Rutas del backend FastAPI que el servidor de desarrollo reenvía a :8000
const backend = { target: 'http://127.0.0.1:8000', changeOrigin: true };

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': backend,
      '/health': backend,
      '/docs': backend,
      '/redoc': backend,
      '/openapi.json': backend,
    },
  },
});
