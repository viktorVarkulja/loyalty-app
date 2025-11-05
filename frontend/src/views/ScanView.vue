<template>
  <MainLayout>
    <div class="scan">
      <!-- Header -->
      <div class="header">
        <h1>Scan Receipt</h1>
        <p>Point your camera at the QR code on your receipt</p>
      </div>

      <!-- Scanner Section -->
      <div class="scanner-container">
        <div v-if="!isScanning && !scanResult" class="scanner-placeholder">
          <div class="camera-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </div>
          <h3>Ready to Scan</h3>
          <p>Tap the button below to start scanning</p>
          <button @click="startScanner" class="btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="9" y1="3" x2="9" y2="21"></line>
              <line x1="15" y1="3" x2="15" y2="21"></line>
            </svg>
            Start Scanner
          </button>
        </div>

        <!-- Camera View -->
        <div v-if="isScanning" class="camera-view">
          <qrcode-stream
            @detect="onDecode"
            @error="onError"
            @camera-on="onCameraOn"
            @camera-off="onCameraOff"
            :track="paintBoundingBox"
          >
            <div class="scanner-overlay">
              <div class="scanner-frame"></div>
            </div>
          </qrcode-stream>
          <button @click="stopScanner" class="btn-secondary">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            Cancel
          </button>
        </div>

        <!-- Processing State -->
        <div v-if="isProcessing" class="processing">
          <div class="spinner"></div>
          <p>Processing receipt...</p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-banner">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>{{ errorMessage }}</span>
        <button @click="clearError" class="close-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Success Result -->
      <div v-if="scanResult" class="result-card">
        <div class="result-header">
          <div class="success-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <h2>Receipt Scanned!</h2>
          <p class="points-earned">+{{ scanResult.total_points }} points</p>
        </div>

        <div class="result-details">
          <div class="detail-row">
            <span class="label">Store</span>
            <span class="value">{{ scanResult.store_name || 'Unknown Store' }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Total Amount</span>
            <span class="value">{{ formatCurrency(scanResult.total_amount) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Items Matched</span>
            <span class="value">{{ scanResult.matched_items }}/{{ scanResult.total_items }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Date</span>
            <span class="value">{{ formatDate(scanResult.scanned_at) }}</span>
          </div>
        </div>

        <div class="result-actions">
          <router-link to="/" class="btn-primary">Go to Home</router-link>
          <button @click="scanAnother" class="btn-secondary">Scan Another</button>
        </div>
      </div>

      <!-- Manual Input Option -->
      <div v-if="!isScanning && !scanResult && !isProcessing" class="manual-input">
        <button @click="showManualInput = !showManualInput" class="toggle-manual">
          {{ showManualInput ? 'Hide' : 'Or enter QR data manually' }}
        </button>

        <div v-if="showManualInput" class="manual-form">
          <textarea
            v-model="manualQrData"
            placeholder="Paste QR code data here..."
            rows="4"
          ></textarea>
          <button @click="processManualInput" :disabled="!manualQrData.trim()" class="btn-primary">
            Process Receipt
          </button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { QrcodeStream } from 'qrcode-reader-vue3'
import { receiptsService } from '../services'
import { useAuthStore } from '../stores/auth'
import MainLayout from '../components/MainLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const isScanning = ref(false)
const isProcessing = ref(false)
const scanResult = ref(null)
const errorMessage = ref('')
const showManualInput = ref(false)
const manualQrData = ref('')

const startScanner = () => {
  isScanning.value = true
  errorMessage.value = ''
  scanResult.value = null
}

const stopScanner = () => {
  isScanning.value = false
}

const onDecode = async (detectedCodes) => {
  if (detectedCodes && detectedCodes.length > 0 && !isProcessing.value) {
    const qrData = detectedCodes[0].rawValue
    await processQrCode(qrData)
  }
}

const onError = (error) => {
  console.error('Camera error:', error)
  errorMessage.value = 'Camera access denied or not available. Please check your browser settings.'
  isScanning.value = false
}

const onCameraOn = () => {
  console.log('Camera is on')
}

const onCameraOff = () => {
  console.log('Camera is off')
}

const paintBoundingBox = (detectedCodes, ctx) => {
  for (const detectedCode of detectedCodes) {
    const { boundingBox: { x, y, width, height } } = detectedCode

    ctx.lineWidth = 2
    ctx.strokeStyle = '#4ade80'
    ctx.strokeRect(x, y, width, height)
  }
}

const processQrCode = async (qrData) => {
  if (!qrData || isProcessing.value) return

  isProcessing.value = true
  isScanning.value = false
  errorMessage.value = ''

  try {
    const result = await receiptsService.scanReceipt(qrData)

    if (result.success) {
      scanResult.value = result.transaction
      // Update points in auth store
      if (authStore.user) {
        authStore.updatePoints(authStore.user.points + result.transaction.total_points)
      }
    } else {
      errorMessage.value = result.error || 'Failed to process receipt'
    }
  } catch (error) {
    console.error('Failed to process receipt:', error)
    errorMessage.value = error.response?.data?.error || 'An error occurred while processing the receipt'
  } finally {
    isProcessing.value = false
  }
}

const processManualInput = async () => {
  if (!manualQrData.value.trim()) return
  await processQrCode(manualQrData.value.trim())
  manualQrData.value = ''
  showManualInput.value = false
}

const scanAnother = () => {
  scanResult.value = null
  errorMessage.value = ''
  manualQrData.value = ''
}

const clearError = () => {
  errorMessage.value = ''
}

const formatCurrency = (amount) => {
  if (!amount) return 'N/A'
  return new Intl.NumberFormat('sr-RS', {
    style: 'currency',
    currency: 'RSD'
  }).format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleString('sr-RS', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.scan {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 80px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px 20px;
}

.header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
}

.header p {
  margin: 0;
  opacity: 0.9;
  font-size: 16px;
}

.scanner-container {
  padding: 20px;
  margin-top: -20px;
}

.scanner-placeholder {
  background: white;
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.camera-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 24px;
}

.scanner-placeholder h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #333;
}

.scanner-placeholder p {
  margin: 0 0 24px 0;
  color: #9ca3af;
  font-size: 14px;
}

.btn-primary {
  padding: 14px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 14px 28px;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 10px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.camera-view {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
}

.camera-view button {
  margin: 16px auto;
  display: flex;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.scanner-frame {
  width: 250px;
  height: 250px;
  border: 3px solid #4ade80;
  border-radius: 12px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
}

.processing {
  background: white;
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.processing p {
  margin: 0;
  color: #9ca3af;
  font-size: 16px;
}

.error-banner {
  margin: 20px;
  padding: 16px;
  background: #fee2e2;
  border-left: 4px solid #ef4444;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #991b1b;
}

.error-banner svg {
  flex-shrink: 0;
}

.error-banner span {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #991b1b;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background: rgba(153, 27, 27, 0.1);
}

.result-card {
  background: white;
  margin: 20px;
  margin-top: -20px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-header {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
  color: white;
  padding: 32px 20px;
  text-align: center;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.result-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
}

.points-earned {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
}

.result-details {
  padding: 24px 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row .label {
  font-size: 14px;
  color: #9ca3af;
  font-weight: 500;
}

.detail-row .value {
  font-size: 15px;
  color: #333;
  font-weight: 600;
}

.result-actions {
  padding: 20px;
  display: flex;
  gap: 12px;
}

.result-actions .btn-primary,
.result-actions .btn-secondary {
  flex: 1;
  justify-content: center;
}

.manual-input {
  padding: 0 20px 20px;
}

.toggle-manual {
  width: 100%;
  padding: 12px;
  background: white;
  color: #667eea;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-manual:hover {
  background: #f9fafb;
  border-color: #667eea;
}

.manual-form {
  margin-top: 12px;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.manual-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  font-family: monospace;
  resize: vertical;
  margin-bottom: 12px;
}

.manual-form textarea:focus {
  outline: none;
  border-color: #667eea;
}

.manual-form .btn-primary {
  width: 100%;
  justify-content: center;
}
</style>
