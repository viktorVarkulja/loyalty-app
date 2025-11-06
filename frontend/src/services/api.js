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

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        } else {
          // No refresh token, redirect to login
          handleLogout()
        }
      } catch (refreshError) {
        // Refresh failed, clear auth and redirect to login
        handleLogout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Function to handle logout and redirect
function handleLogout() {
  // Clear all auth data from localStorage
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('auth')

  // Redirect to login
  if (router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
}

export default api
