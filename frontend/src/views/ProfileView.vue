<template>
  <MainLayout>
    <div class="profile">
      <!-- Header -->
      <div class="header">
        <div class="profile-avatar">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <h1>{{ authStore.user?.name || 'User' }}</h1>
        <p>{{ authStore.user?.email }}</p>
      </div>

      <!-- Points Summary -->
      <div class="points-summary">
        <div class="points-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="points-info">
          <p class="points-label">Total Points</p>
          <h2 class="points-value">{{ authStore.user?.points || 0 }}</h2>
        </div>
      </div>

      <!-- User Information -->
      <div class="section">
        <h3 class="section-title">Account Information</h3>
        <div class="info-card">
          <div class="info-row">
            <div class="info-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>Full Name</span>
            </div>
            <div class="info-value">{{ authStore.user?.name || 'N/A' }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <span>Email</span>
            </div>
            <div class="info-value">{{ authStore.user?.email || 'N/A' }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <span>Member Since</span>
            </div>
            <div class="info-value">{{ formatDate(authStore.user?.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <div class="section">
        <h3 class="section-title">Statistics</h3>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon scans">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
              </svg>
            </div>
            <p class="stat-label">Total Scans</p>
            <p class="stat-value">{{ stats.totalScans }}</p>
          </div>
          <div class="stat-card">
            <div class="stat-icon points">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <p class="stat-label">Points Earned</p>
            <p class="stat-value">{{ stats.totalPoints }}</p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="section">
        <h3 class="section-title">Actions</h3>
        <div class="actions-card">
          <button class="action-item" @click="handleLogout">
            <div class="action-icon logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
            </div>
            <span>Logout</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      </div>

      <!-- App Info -->
      <div class="app-info">
        <p>Serbian Loyalty App</p>
        <p>Version 1.0.0</p>
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

<style scoped>
.profile {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 80px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 20px 30px;
  text-align: center;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
}

.header p {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.points-summary {
  background: white;
  margin: -30px 20px 20px;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.points-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.points-info {
  flex: 1;
}

.points-label {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

.points-value {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  color: #667eea;
}

.section {
  padding: 0 0 24px;
}

.section-title {
  margin: 0 20px 12px 20px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.info-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin: 0 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.info-label svg {
  color: #9ca3af;
}

.info-value {
  font-size: 14px;
  color: #333;
  font-weight: 600;
  text-align: right;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 0 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 12px;
}

.stat-icon.scans {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.points {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
}

.stat-label {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
}

.stat-value {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.actions-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin: 0 20px;
}

.action-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.action-item:hover {
  background: #f9fafb;
}

.action-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.action-icon.logout {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.action-item span {
  flex: 1;
  text-align: left;
}

.chevron {
  color: #9ca3af;
  flex-shrink: 0;
}

.app-info {
  text-align: center;
  padding: 20px;
  color: #9ca3af;
}

.app-info p {
  margin: 0;
  font-size: 13px;
}

.app-info p:first-child {
  font-weight: 600;
  margin-bottom: 4px;
}
</style>
