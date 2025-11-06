import axios from 'axios'
import router from '../router'

// Use environment variable or fallback to localhost
// For phone access, start dev server with: npm run dev -- --host 0.0.0.0
// Then access via your computer's IP address
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken
          })

          const { access } = response.data
          localStorage.setItem('accessToken', access)

          // If a new refresh token is provided, update it too (for token rotation)
          if (response.data.refresh) {
            localStorage.setItem('refreshToken', response.data.refresh)
          }

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        } else {
          // No refresh token, show session expired modal
          handleSessionExpired()
        }
      } catch (refreshError) {
        // Refresh failed, show session expired modal
        handleSessionExpired()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Function to handle session expiration
function handleSessionExpired() {
  // Clear all auth data from localStorage
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('auth')

  // Mark that session expired to show modal
  sessionStorage.setItem('sessionExpired', 'true')

  // Redirect to login
  if (router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
}

// Function to handle logout and redirect (kept for compatibility)
function handleLogout() {
  handleSessionExpired()
}

export default api
