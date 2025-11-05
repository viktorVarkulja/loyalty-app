import api from './api'

export const productsService = {
  // Get all products
  async getProducts(page = 1) {
    const response = await api.get(`/products/?page=${page}`)
    return response.data
  },

  // Get single product
  async getProduct(id) {
    const response = await api.get(`/products/${id}/`)
    return response.data
  },

  // Search products
  async searchProducts(query) {
    const response = await api.get(`/products/search/?q=${encodeURIComponent(query)}`)
    return response.data
  },

  // Get all stores
  async getStores() {
    const response = await api.get('/stores/')
    return response.data
  },

  // Get favorite stores
  async getFavoriteStores() {
    const response = await api.get('/stores/favorites/')
    return response.data
  },

  // Add favorite store
  async addFavoriteStore(storeId) {
    const response = await api.post('/stores/favorites/add/', {
      store_id: storeId
    })
    return response.data
  },

  // Remove favorite store
  async removeFavoriteStore(favoriteId) {
    const response = await api.delete(`/stores/favorites/${favoriteId}/`)
    return response.data
  }
}
