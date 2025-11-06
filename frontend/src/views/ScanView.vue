<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-100 pb-20">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-8 px-5">
        <h1 class="m-0 mb-2 text-[28px] font-bold">Scan Receipt</h1>
        <p class="m-0 opacity-90 text-base">Point your camera at the QR code on your receipt</p>
      </div>

      <!-- Scanner Section -->
      <div class="p-5 -mt-5">
        <div v-if="!isScanning && !scanResult" class="bg-white rounded-2xl py-10 px-5 text-center shadow-[0_4px_12px_rgba(0,0,0,0.1)]">
          <div class="w-20 h-20 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center text-white mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </div>
          <h3 class="m-0 mb-2 text-xl text-gray-800">Ready to Scan</h3>
          <p class="m-0 mb-6 text-gray-400 text-sm">Tap the button below to start scanning</p>
          <button @click="startScanner" class="py-3.5 px-7 bg-gradient-to-br from-primary to-primary-dark text-white border-none rounded-[10px] font-semibold text-base cursor-pointer transition-transform duration-200 inline-flex items-center gap-2 hover:-translate-y-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="9" y1="3" x2="9" y2="21"></line>
              <line x1="15" y1="3" x2="15" y2="21"></line>
            </svg>
            Start Scanner
          </button>
        </div>

        <!-- Camera View -->
        <div v-if="isScanning" class="bg-white rounded-2xl overflow-hidden shadow-[0_4px_12px_rgba(0,0,0,0.1)] relative">
          <qrcode-stream
            @detect="onDecode"
            @error="onError"
            @camera-on="onCameraOn"
            @camera-off="onCameraOff"
            :track="paintBoundingBox"
          >
            <div class="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center pointer-events-none">
              <div class="w-[250px] h-[250px] border-[3px] border-success rounded-xl shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]"></div>
            </div>
          </qrcode-stream>
          <button @click="stopScanner" class="my-4 mx-auto flex py-3.5 px-7 bg-white text-primary border-2 border-primary rounded-[10px] font-semibold text-base cursor-pointer transition-all duration-200 items-center gap-2 hover:bg-primary hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            Cancel
          </button>
        </div>

        <!-- Processing State -->
        <div v-if="isProcessing" class="bg-white rounded-2xl py-10 px-5 text-center shadow-[0_4px_12px_rgba(0,0,0,0.1)]">
          <div class="w-[50px] h-[50px] border-4 border-gray-100 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
          <p class="m-0 text-gray-400 text-base">Processing receipt...</p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="my-5 mx-5 p-4 bg-red-50 border-l-4 border-error rounded-lg flex items-center gap-3 text-red-800">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span class="flex-1 text-sm font-medium">{{ errorMessage }}</span>
        <button @click="clearError" class="bg-none border-none cursor-pointer text-red-800 p-1 flex items-center justify-center rounded transition-colors hover:bg-red-200">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Success Result -->
      <div v-if="scanResult" class="bg-white mx-5 -mt-5 rounded-2xl overflow-hidden shadow-[0_4px_12px_rgba(0,0,0,0.1)]">
        <div class="bg-gradient-to-br from-success to-green-600 text-white py-8 px-5 text-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <h2 class="m-0 mb-2 text-2xl font-bold">Receipt Scanned!</h2>
          <p class="m-0 text-[32px] font-bold">+{{ scanResult.total_points }} points</p>
        </div>

        <div class="p-6">
          <div class="flex justify-between items-center py-3 border-b border-gray-100">
            <span class="text-sm text-gray-400 font-medium">Store</span>
            <span class="text-[15px] text-gray-800 font-semibold">{{ scanResult.store_name || 'Unknown Store' }}</span>
          </div>
          <div class="flex justify-between items-center py-3 border-b border-gray-100">
            <span class="text-sm text-gray-400 font-medium">Total Amount</span>
            <span class="text-[15px] text-gray-800 font-semibold">{{ formatCurrency(scanResult.total_amount) }}</span>
          </div>
          <div class="flex justify-between items-center py-3 border-b border-gray-100">
            <span class="text-sm text-gray-400 font-medium">Items Matched</span>
            <span class="text-[15px] text-gray-800 font-semibold">{{ scanResult.matched_items }}/{{ scanResult.total_items }}</span>
          </div>
          <div class="flex justify-between items-center py-3">
            <span class="text-sm text-gray-400 font-medium">Date</span>
            <span class="text-[15px] text-gray-800 font-semibold">{{ formatDate(scanResult.scanned_at) }}</span>
          </div>
        </div>

        <div class="p-5 flex gap-3">
          <router-link to="/" class="flex-1 py-3.5 px-7 bg-gradient-to-br from-primary to-primary-dark text-white border-none rounded-[10px] font-semibold text-base cursor-pointer transition-transform duration-200 inline-flex items-center gap-2 justify-center no-underline hover:-translate-y-0.5">Go to Home</router-link>
          <button @click="scanAnother" class="flex-1 py-3.5 px-7 bg-white text-primary border-2 border-primary rounded-[10px] font-semibold text-base cursor-pointer transition-all duration-200 inline-flex items-center gap-2 justify-center no-underline hover:bg-primary hover:text-white">Scan Another</button>
        </div>
      </div>

      <!-- Manual Input Option -->
      <div v-if="!isScanning && !scanResult && !isProcessing" class="pb-5 px-5">
        <button @click="showManualInput = !showManualInput" class="w-full py-3 px-3 bg-white text-primary border border-gray-200 rounded-lg text-sm font-medium cursor-pointer transition-all duration-200 hover:bg-gray-50 hover:border-primary">
          {{ showManualInput ? 'Hide' : 'Or enter QR data manually' }}
        </button>

        <div v-if="showManualInput" class="mt-3 bg-white p-4 rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.08)]">
          <textarea
            v-model="manualQrData"
            placeholder="Paste QR code data here..."
            rows="4"
            class="w-full p-3 border border-gray-200 rounded-md text-sm font-mono resize-y mb-3 outline-none focus:border-primary"
          ></textarea>
          <button @click="processManualInput" :disabled="!manualQrData.trim()" class="w-full py-3.5 px-7 bg-gradient-to-br from-primary to-primary-dark text-white border-none rounded-[10px] font-semibold text-base cursor-pointer transition-transform duration-200 inline-flex items-center gap-2 justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:-translate-y-0.5">
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
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
