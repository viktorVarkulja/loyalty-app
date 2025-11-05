import api from './api'

export const authService = {
  // Register new user
  async register(userData) {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  // Login user
  async login(credentials) {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  // Get user profile
  async getProfile() {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  // Update user profile
  async updateProfile(data) {
    const response = await api.patch('/auth/profile/update/', data)
    return response.data
  },

  // Refresh token
  async refreshToken(refreshToken) {
    const response = await api.post('/auth/token/refresh/', {
      refresh: refreshToken
    })
    return response.data
  }
}
