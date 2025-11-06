<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-100">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-8 px-5">
        <div>
          <h1 class="m-0 mb-2 text-[28px] font-bold">Hello, {{ authStore.userName }}!</h1>
          <p class="m-0 opacity-90 text-base">Welcome back to your loyalty dashboard</p>
        </div>
      </div>

      <!-- Points Card -->
      <div class="bg-white -mt-8 mx-5 mb-5 p-6 rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.1)] flex items-center gap-5">
        <div class="w-16 h-16 bg-gradient-to-br from-primary to-primary-dark rounded-2xl flex items-center justify-center text-white">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="flex-1">
          <p class="m-0 text-sm text-gray-400 font-medium">Your Points</p>
          <h2 class="mt-1 mb-0 text-4xl font-bold text-primary">{{ pointsBalance }}</h2>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="p-5">
        <h3 class="m-0 mb-4 text-lg font-semibold text-gray-800">Quick Actions</h3>
        <div class="grid grid-cols-2 gap-3">
          <router-link to="/scan" class="bg-white p-5 rounded-xl no-underline flex flex-col items-center gap-3 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)]">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-primary to-primary-dark">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
              </svg>
            </div>
            <span class="text-[13px] font-medium text-gray-800 text-center">Scan Receipt</span>
          </router-link>

          <router-link to="/products" class="bg-white p-5 rounded-xl no-underline flex flex-col items-center gap-3 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)]">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-success to-green-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <span class="text-[13px] font-medium text-gray-800 text-center">View Products</span>
          </router-link>

          <button @click="showWebshop = true" class="bg-white p-5 rounded-xl flex flex-col items-center gap-3 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)] border-none cursor-pointer">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-purple-500 to-purple-700">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <span class="text-[13px] font-medium text-gray-800 text-center">Webshop</span>
          </button>

          <router-link to="/transactions" class="bg-white p-5 rounded-xl no-underline flex flex-col items-center gap-3 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)]">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-warning to-amber-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <span class="text-[13px] font-medium text-gray-800 text-center">Transaction History</span>
          </router-link>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="p-5" v-if="recentTransactions.length > 0">
        <h3 class="m-0 mb-4 text-lg font-semibold text-gray-800">Recent Activity</h3>
        <div class="bg-white rounded-xl overflow-hidden shadow-[0_2px_8px_rgba(0,0,0,0.08)]">
          <div v-for="transaction in recentTransactions" :key="transaction.id" class="flex items-center gap-4 p-4 border-b border-gray-100 last:border-b-0">
            <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center text-green-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="flex-1">
              <p class="m-0 mb-1 text-[15px] font-medium text-gray-800">Receipt Scanned</p>
              <p class="m-0 text-[13px] text-gray-400">{{ formatDate(transaction.scanned_at) }}</p>
            </div>
            <div class="text-base font-semibold text-green-600">+{{ transaction.total_points }}</div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="py-[60px] px-5 text-center text-gray-400" v-else>
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-5 opacity-30 inline-block">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
          <line x1="15" y1="3" x2="15" y2="21"></line>
        </svg>
        <h3 class="m-0 mb-2 text-xl text-gray-800">No activity yet</h3>
        <p class="m-0 mb-6 text-sm">Start scanning receipts to earn points!</p>
        <router-link to="/scan" class="inline-block py-3 px-6 bg-gradient-to-br from-primary to-primary-dark text-white no-underline rounded-lg font-semibold transition-transform duration-200 hover:-translate-y-0.5">Scan Your First Receipt</router-link>
      </div>
    </div>

    <!-- Webshop Modal -->
    <WebshopModal :isVisible="showWebshop" @close="showWebshop = false" />
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { transactionsService } from '../services'
import MainLayout from '../components/MainLayout.vue'
import WebshopModal from '../components/WebshopModal.vue'

const authStore = useAuthStore()
const pointsBalance = ref(0)
const recentTransactions = ref([])
const isLoading = ref(false)
const showWebshop = ref(false)

const fetchPointsBalance = async () => {
  try {
    const data = await transactionsService.getPointsBalance()
    pointsBalance.value = data.points
    authStore.updatePoints(data.points)
  } catch (error) {
    console.error('Failed to fetch points:', error)
  }
}

const fetchRecentTransactions = async () => {
  try {
    const data = await transactionsService.getTransactions(1)
    recentTransactions.value = data.results.slice(0, 5) // Show only 5 recent
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`

  return date.toLocaleDateString()
}

onMounted(async () => {
  isLoading.value = true
  await Promise.all([
    fetchPointsBalance(),
    fetchRecentTransactions()
  ])
  isLoading.value = false
})
</script>
