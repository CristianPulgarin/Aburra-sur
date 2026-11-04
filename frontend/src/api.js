// Base de la API FastAPI. Vacío = rutas relativas servidas por el proxy de Vite (vite.config.js).
// Para apuntar a otro servidor: crear frontend/.env con VITE_API_URL=http://host:puerto
export const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');

export const apiUrl = (path) => `${API_BASE}${path}`;
