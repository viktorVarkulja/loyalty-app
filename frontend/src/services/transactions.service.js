import api from './api'

export const transactionsService = {
  // Scan receipt
  async scanReceipt(qrData) {
    const response = await api.post('/receipts/scan/', {
      qr_data: qrData
    })
    return response.data
  },

  // Get points balance
  async getPointsBalance() {
    const response = await api.get('/points/balance/')
    return response.data
  },

  // Get transaction history
  async getTransactions(page = 1) {
    const response = await api.get(`/transactions/?page=${page}`)
    return response.data
  },

  // Get single transaction
  async getTransaction(id) {
    const response = await api.get(`/transactions/${id}/`)
    return response.data
  }
}
