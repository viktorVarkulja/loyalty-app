<template>
  <MainLayout>
    <div class="home">
      <!-- Header -->
      <div class="header">
        <div class="greeting">
          <h1>Hello, {{ authStore.userName }}!</h1>
          <p>Welcome back to your loyalty dashboard</p>
        </div>
      </div>

      <!-- Points Card -->
      <div class="points-card">
        <div class="points-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="points-content">
          <p class="points-label">Your Points</p>
          <h2 class="points-value">{{ pointsBalance }}</h2>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3>Quick Actions</h3>
        <div class="actions-grid">
          <router-link to="/scan" class="action-card">
            <div class="action-icon scan">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
              </svg>
            </div>
            <span>Scan Receipt</span>
          </router-link>

          <router-link to="/products" class="action-card">
            <div class="action-icon products">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <span>View Products</span>
          </router-link>

          <router-link to="/transactions" class="action-card">
            <div class="action-icon history">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <span>Transaction History</span>
          </router-link>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="recent-activity" v-if="recentTransactions.length > 0">
        <h3>Recent Activity</h3>
        <div class="activity-list">
          <div v-for="transaction in recentTransactions" :key="transaction.id" class="activity-item">
            <div class="activity-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="activity-details">
              <p class="activity-title">Receipt Scanned</p>
              <p class="activity-date">{{ formatDate(transaction.scanned_at) }}</p>
            </div>
            <div class="activity-points">+{{ transaction.total_points }}</div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" v-else>
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
          <line x1="15" y1="3" x2="15" y2="21"></line>
        </svg>
        <h3>No activity yet</h3>
        <p>Start scanning receipts to earn points!</p>
        <router-link to="/scan" class="btn-primary">Scan Your First Receipt</router-link>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { transactionsService } from '../services'
import MainLayout from '../components/MainLayout.vue'

const authStore = useAuthStore()
const pointsBalance = ref(0)
const recentTransactions = ref([])
const isLoading = ref(false)

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

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px 20px;
}

.greeting h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
}

.greeting p {
  margin: 0;
  opacity: 0.9;
  font-size: 16px;
}

.points-card {
  background: white;
  margin: -30px 20px 20px;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
}

.points-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.points-content {
  flex: 1;
}

.points-label {
  margin: 0;
  font-size: 14px;
  color: #9ca3af;
  font-weight: 500;
}

.points-value {
  margin: 4px 0 0 0;
  font-size: 36px;
  font-weight: 700;
  color: #667eea;
}

.quick-actions {
  padding: 20px;
}

.quick-actions h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.action-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.action-icon.scan {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.action-icon.products {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
}

.action-icon.history {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.action-card span {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  text-align: center;
}

.recent-activity {
  padding: 20px;
}

.recent-activity h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.activity-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background: #e8f5e9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #22c55e;
}

.activity-details {
  flex: 1;
}

.activity-title {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.activity-date {
  margin: 0;
  font-size: 13px;
  color: #9ca3af;
}

.activity-points {
  font-size: 16px;
  font-weight: 600;
  color: #22c55e;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #9ca3af;
}

.empty-state svg {
  margin-bottom: 20px;
  opacity: 0.3;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #333;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
}

.btn-primary {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}
</style>
