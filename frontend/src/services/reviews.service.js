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
  },

  // Transaction Item Review APIs
  // Request review for unmatched transaction item
  async requestItemReview(itemId, notes = '') {
    const response = await api.post(`/items/${itemId}/request-review/`, { notes })
    return response.data
  },

  // Get pending item reviews (admin only)
  async getPendingItemReviews() {
    const response = await api.get('/reviews/pending/')
    return response.data
  },

  // Approve item review (admin only)
  async approveItemReview(itemId, data) {
    const response = await api.post(`/reviews/${itemId}/approve/`, data)
    return response.data
  },

  // Reject item review (admin only)
  async rejectItemReview(itemId, notes = '') {
    const response = await api.post(`/reviews/${itemId}/reject/`, { notes })
    return response.data
  }
}
