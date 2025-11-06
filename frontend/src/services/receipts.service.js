import api from './api'

export const receiptsService = {
  /**
   * Scan a receipt QR code
   * @param {string} qrData - The QR code data from the fiscal receipt
   * @returns {Promise<Object>} - Transaction details with matched/unmatched items
   */
  async scanReceipt(qrData) {
    const response = await api.post('/receipts/scan/', { qr_data: qrData })
    return response.data
  }
}
