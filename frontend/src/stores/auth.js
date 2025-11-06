import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { isTokenExpired } from '@/utils/jwt'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value)
  const userPoints = computed(() => user.value?.points || 0)
  const userEmail = computed(() => user.value?.email || '')
  const userName = computed(() => user.value?.name || '')
  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  // Actions
  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  }

  function setUser(userData) {
    user.value = userData
  }

  function clearAuth() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  function setLoading(value) {
    isLoading.value = value
  }

  function setError(errorMessage) {
    error.value = errorMessage
  }

  function clearError() {
    error.value = null
  }

  function updatePoints(newPoints) {
    if (user.value) {
      user.value.points = newPoints
    }
  }

  function logout() {
    clearAuth()
  }

  /**
   * Check if the access token is expired and attempt to refresh it
   * @returns {Promise<boolean>} - True if token is valid or successfully refreshed, false otherwise
   */
  async function checkTokenExpiration() {
    // If no access token, user is not authenticated
    if (!accessToken.value) {
      return false
    }

    // Check if access token is expired
    if (isTokenExpired(accessToken.value)) {
      // Try to refresh with refresh token
      if (refreshToken.value && !isTokenExpired(refreshToken.value)) {
        try {
          const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken.value
          })

          if (response.data && response.data.access) {
            // Update access token (keep same refresh token)
            accessToken.value = response.data.access
            localStorage.setItem('accessToken', response.data.access)

            // If a new refresh token is provided, update it too
            if (response.data.refresh) {
              refreshToken.value = response.data.refresh
              localStorage.setItem('refreshToken', response.data.refresh)
            }

            return true
          }
        } catch (error) {
          console.error('Failed to refresh token:', error)
          return false
        }
      }

      // Access token expired and no valid refresh token
      return false
    }

    // Access token is still valid
    return true
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    userPoints,
    userEmail,
    userName,
    isAdmin,
    // Actions
    setTokens,
    setUser,
    clearAuth,
    logout,
    setLoading,
    setError,
    clearError,
    updatePoints,
    checkTokenExpiration
  }
})
