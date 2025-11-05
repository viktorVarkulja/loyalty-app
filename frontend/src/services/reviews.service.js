import api from './api'

export const reviewsService = {
  // Submit product for review
  async submitReview(data) {
    const response = await api.post('/reviews/', data)
    return response.data
  },

  // Get my review requests
  async getMyReviews() {
    const response = await api.get('/reviews/my/')
    return response.data
  },

  // Get all reviews (admin only)
  async getAllReviews() {
    const response = await api.get('/reviews/')
    return response.data
  },

  // Get review details
  async getReview(id) {
    const response = await api.get(`/reviews/${id}/`)
    return response.data
  }
}
