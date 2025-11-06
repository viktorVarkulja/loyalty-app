<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-100 pb-20">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-8 px-5">
        <h1 class="m-0 mb-2 text-[28px] font-bold">Transaction History</h1>
        <p class="m-0 opacity-90 text-base">View all your receipt scans and earned points</p>
      </div>

      <!-- Stats Card -->
      <div class="bg-white -mt-8 mx-5 mb-5 p-5 rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.1)] flex gap-4">
        <div class="flex-1 flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-gradient-to-br from-primary to-primary-dark">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="9" y1="3" x2="9" y2="21"></line>
              <line x1="15" y1="3" x2="15" y2="21"></line>
            </svg>
          </div>
          <div class="flex-1">
            <p class="m-0 mb-1 text-xs text-gray-400 font-medium uppercase">Total Scans</p>
            <p class="m-0 text-2xl font-bold text-gray-800">{{ totalCount }}</p>
          </div>
        </div>
        <div class="flex-1 flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-gradient-to-br from-warning to-amber-600">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </div>
          <div class="flex-1">
            <p class="m-0 mb-1 text-xs text-gray-400 font-medium uppercase">Total Points</p>
            <p class="m-0 text-2xl font-bold text-gray-800">{{ totalPoints }}</p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-[60px] px-5 text-gray-400">
        <div class="w-10 h-10 border-4 border-gray-100 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
        <p>Loading transactions...</p>
      </div>

      <!-- Transactions List -->
      <div v-else-if="transactions.length > 0" class="pb-5 flex flex-col gap-3">
        <div
          v-for="transaction in transactions"
          :key="transaction.id"
          class="bg-white rounded-xl p-4 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 cursor-pointer mx-5 hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)]"
          @click="selectTransaction(transaction)"
        >
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-success to-green-600 rounded-xl flex items-center justify-center text-white shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="m-0 mb-1 text-base font-semibold text-gray-800 whitespace-nowrap overflow-hidden text-ellipsis">{{ transaction.store_name || 'Unknown Store' }}</h3>
              <p class="m-0 mb-2 text-[13px] text-gray-400">{{ formatDate(transaction.scanned_at) }}</p>
              <div class="flex items-center gap-3">
                <span class="text-xs text-gray-500 flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="9" cy="21" r="1"></circle>
                    <circle cx="20" cy="21" r="1"></circle>
                    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                  </svg>
                  {{ transaction.total_items }} items
                </span>
                <span class="text-xs text-gray-500">
                  {{ formatCurrency(transaction.total_amount) }}
                </span>
              </div>
            </div>
            <div class="shrink-0">
              <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-1.5 px-3 rounded-2xl flex items-center gap-1 font-semibold text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
                <span>+{{ transaction.total_points }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-[60px] px-5 text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-5 opacity-30 inline-block">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
          <line x1="15" y1="3" x2="15" y2="21"></line>
        </svg>
        <h3 class="m-0 mb-2 text-xl text-gray-800">No transactions yet</h3>
        <p class="m-0 mb-6 text-sm">Start scanning receipts to see your history here</p>
        <router-link to="/scan" class="inline-block py-3 px-6 bg-gradient-to-br from-primary to-primary-dark text-white no-underline rounded-lg font-semibold transition-transform duration-200 hover:-translate-y-0.5">Scan Your First Receipt</router-link>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="py-5 px-5 flex items-center justify-between gap-4">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="py-2.5 px-5 bg-white text-primary border-2 border-primary rounded-lg font-semibold cursor-pointer transition-all duration-200 flex items-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-primary hover:text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Previous
        </button>
        <span class="text-sm text-gray-500 font-medium">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="py-2.5 px-5 bg-white text-primary border-2 border-primary rounded-lg font-semibold cursor-pointer transition-all duration-200 flex items-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-primary hover:text-white"
        >
          Next
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>

      <!-- Transaction Detail Modal -->
      <div v-if="selectedTransaction" class="fixed top-0 left-0 right-0 bottom-0 bg-black/50 flex items-center justify-center z-[1000] p-5" @click="closeModal">
        <div class="bg-white rounded-2xl max-w-[500px] w-full max-h-[80vh] overflow-y-auto shadow-[0_20px_60px_rgba(0,0,0,0.3)]" @click.stop>
          <div class="p-5 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white z-[1]">
            <h2 class="m-0 text-xl font-bold text-gray-800">Transaction Details</h2>
            <button @click="closeModal" class="bg-none border-none cursor-pointer text-gray-400 p-1 flex items-center justify-center rounded-md transition-all duration-200 hover:bg-gray-100 hover:text-gray-800">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="p-5">
            <div class="mb-6">
              <h3 class="m-0 mb-4 text-base font-semibold text-gray-800">Receipt Information</h3>
              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-400 font-medium">Store</span>
                <span class="text-[15px] text-gray-800 font-semibold text-right">{{ selectedTransaction.store_name || 'Unknown Store' }}</span>
              </div>
              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-400 font-medium">Date & Time</span>
                <span class="text-[15px] text-gray-800 font-semibold text-right">{{ formatDate(selectedTransaction.scanned_at) }}</span>
              </div>
              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-400 font-medium">Total Amount</span>
                <span class="text-[15px] text-gray-800 font-semibold text-right">{{ formatCurrency(selectedTransaction.total_amount) }}</span>
              </div>
              <div class="flex justify-between items-center py-3">
                <span class="text-sm text-gray-400 font-medium">Points Earned</span>
                <span class="text-[15px] text-primary font-semibold text-right">+{{ selectedTransaction.total_points }}</span>
              </div>
            </div>

            <div class="mb-0" v-if="selectedTransaction.items && selectedTransaction.items.length > 0">
              <h3 class="m-0 mb-4 text-base font-semibold text-gray-800">Items ({{ selectedTransaction.total_items }})</h3>
              <div class="flex flex-col gap-3">
                <div v-for="item in selectedTransaction.items" :key="item.id" class="flex justify-between items-start p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1 min-w-0">
                    <p class="m-0 mb-1 text-sm font-semibold text-gray-800">{{ item.product_name }}</p>
                    <p class="m-0 text-xs text-gray-400">{{ item.quantity }}x {{ formatCurrency(item.unit_price) }}</p>
                  </div>
                  <div class="text-right ml-3">
                    <p class="m-0 mb-1 text-sm font-semibold text-gray-800">{{ formatCurrency(item.total_price) }}</p>
                    <p class="m-0 text-xs text-primary font-semibold" v-if="item.points_earned > 0">+{{ item.points_earned }} pts</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { transactionsService } from '../services'
import MainLayout from '../components/MainLayout.vue'

const transactions = ref([])
const selectedTransaction = ref(null)
const isLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)

const totalPoints = computed(() => {
  return transactions.value.reduce((sum, t) => sum + t.total_points, 0)
})

const fetchTransactions = async (page = 1) => {
  isLoading.value = true
  try {
    const data = await transactionsService.getTransactions(page)
    transactions.value = data.results
    totalCount.value = data.count
    totalPages.value = Math.ceil(data.count / 20) // 20 items per page
    currentPage.value = page
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  } finally {
    isLoading.value = false
  }
}

const selectTransaction = (transaction) => {
  selectedTransaction.value = transaction
}

const closeModal = () => {
  selectedTransaction.value = null
}

const previousPage = () => {
  if (currentPage.value > 1) {
    fetchTransactions(currentPage.value - 1)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    fetchTransactions(currentPage.value + 1)
  }
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
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return `Today at ${date.toLocaleTimeString('sr-RS', { hour: '2-digit', minute: '2-digit' })}`
  }
  if (diffDays === 1) {
    return `Yesterday at ${date.toLocaleTimeString('sr-RS', { hour: '2-digit', minute: '2-digit' })}`
  }
  if (diffDays < 7) {
    return `${diffDays} days ago`
  }

  return date.toLocaleDateString('sr-RS', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchTransactions()
})
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
