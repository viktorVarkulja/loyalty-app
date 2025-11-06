<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-100 pb-20">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-10 px-5 pb-8 text-center">
        <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <h1 class="m-0 mb-2 text-2xl font-bold">{{ authStore.user?.name || 'User' }}</h1>
        <p class="m-0 opacity-90 text-sm">{{ authStore.user?.email }}</p>
      </div>

      <!-- Points Summary -->
      <div class="bg-white -mt-8 mx-5 mb-5 p-5 rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.1)] flex items-center gap-4">
        <div class="w-14 h-14 bg-gradient-to-br from-warning to-amber-600 rounded-xl flex items-center justify-center text-white shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="flex-1">
          <p class="m-0 mb-1 text-[13px] text-gray-400 font-medium">Total Points</p>
          <h2 class="m-0 text-[32px] font-bold text-primary">{{ authStore.user?.points || 0 }}</h2>
        </div>
      </div>

      <!-- User Information -->
      <div class="pb-6">
        <h3 class="m-0 mx-5 mb-3 text-base font-semibold text-gray-800">Account Information</h3>
        <div class="bg-white rounded-xl overflow-hidden shadow-[0_2px_8px_rgba(0,0,0,0.08)] mx-5">
          <div class="flex justify-between items-center p-4 border-b border-gray-100">
            <div class="flex items-center gap-3 text-gray-500 text-sm font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>Full Name</span>
            </div>
            <div class="text-sm text-gray-800 font-semibold text-right">{{ authStore.user?.name || 'N/A' }}</div>
          </div>
          <div class="flex justify-between items-center p-4 border-b border-gray-100">
            <div class="flex items-center gap-3 text-gray-500 text-sm font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <span>Email</span>
            </div>
            <div class="text-sm text-gray-800 font-semibold text-right">{{ authStore.user?.email || 'N/A' }}</div>
          </div>
          <div class="flex justify-between items-center p-4">
            <div class="flex items-center gap-3 text-gray-500 text-sm font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <span>Member Since</span>
            </div>
            <div class="text-sm text-gray-800 font-semibold text-right">{{ formatDate(authStore.user?.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <div class="pb-6">
        <h3 class="m-0 mx-5 mb-3 text-base font-semibold text-gray-800">Statistics</h3>
        <div class="grid grid-cols-2 gap-3 mx-5">
          <div class="bg-white p-5 rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.08)] text-center">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white mx-auto mb-3 bg-gradient-to-br from-primary to-primary-dark">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
              </svg>
            </div>
            <p class="m-0 mb-2 text-xs text-gray-400 font-medium">Total Scans</p>
            <p class="m-0 text-2xl font-bold text-gray-800">{{ stats.totalScans }}</p>
          </div>
          <div class="bg-white p-5 rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.08)] text-center">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white mx-auto mb-3 bg-gradient-to-br from-success to-green-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <p class="m-0 mb-2 text-xs text-gray-400 font-medium">Points Earned</p>
            <p class="m-0 text-2xl font-bold text-gray-800">{{ stats.totalPoints }}</p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="pb-6">
        <h3 class="m-0 mx-5 mb-3 text-base font-semibold text-gray-800">Actions</h3>
        <div class="bg-white rounded-xl overflow-hidden shadow-[0_2px_8px_rgba(0,0,0,0.08)] mx-5">
          <button class="w-full flex items-center gap-3 p-4 bg-none border-none cursor-pointer transition-colors duration-200 text-[15px] font-medium text-gray-800 hover:bg-gray-50" @click="handleLogout">
            <div class="w-10 h-10 rounded-[10px] flex items-center justify-center text-white shrink-0 bg-gradient-to-br from-error to-red-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
            </div>
            <span class="flex-1 text-left">Logout</span>
            <svg class="text-gray-400 shrink-0" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      </div>

      <!-- App Info -->
      <div class="text-center py-5 px-5 text-gray-400">
        <p class="m-0 font-semibold mb-1 text-[13px]">Serbian Loyalty App</p>
        <p class="m-0 text-[13px]">Version 1.0.0</p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { transactionsService } from '../services'
import MainLayout from '../components/MainLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({
  totalScans: 0,
  totalPoints: 0
})

const fetchStats = async () => {
  try {
    const data = await transactionsService.getTransactions(1)
    stats.value.totalScans = data.count

    // Calculate total points from all transactions
    let allTransactions = data.results
    let totalPoints = 0

    // If there are more pages, we need to fetch them all
    if (data.count > 20) {
      const totalPages = Math.ceil(data.count / 20)
      const promises = []
      for (let page = 2; page <= totalPages; page++) {
        promises.push(transactionsService.getTransactions(page))
      }
      const results = await Promise.all(promises)
      results.forEach(result => {
        allTransactions = [...allTransactions, ...result.results]
      })
    }

    totalPoints = allTransactions.reduce((sum, t) => sum + t.total_points, 0)
    stats.value.totalPoints = totalPoints
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('sr-RS', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchStats()
})
</script>
