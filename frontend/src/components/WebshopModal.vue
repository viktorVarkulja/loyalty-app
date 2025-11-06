<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="handleClose">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Webshop</h2>
        <button @click="handleClose" class="close-btn">×</button>
      </div>

      <div class="points-balance">
        <span>Your Points:</span>
        <strong>{{ userPoints }} points</strong>
      </div>

      <div class="modal-body">
        <div class="products-grid">
          <div v-for="product in products" :key="product.id" class="product-card">
            <div class="product-image">
              {{ product.emoji }}
            </div>
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-description">{{ product.description }}</p>
            <div class="product-footer">
              <span class="product-price">10 points</span>
              <button
                @click="handlePurchase(product)"
                :disabled="purchasing || userPoints < 10"
                class="buy-btn"
              >
                {{ purchasing ? 'Processing...' : userPoints < 10 ? 'Not enough points' : 'Buy' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])
const authStore = useAuthStore()
const purchasing = ref(false)

const userPoints = computed(() => authStore.user?.points || 0)

const products = [
  {
    id: 1,
    name: 'Coffee',
    description: 'Fresh brewed coffee',
    emoji: '☕'
  },
  {
    id: 2,
    name: 'Pizza Slice',
    description: 'Delicious pizza slice',
    emoji: '🍕'
  },
  {
    id: 3,
    name: 'Ice Cream',
    description: 'Cold and sweet',
    emoji: '🍦'
  },
  {
    id: 4,
    name: 'Burger',
    description: 'Tasty burger',
    emoji: '🍔'
  },
  {
    id: 5,
    name: 'Donut',
    description: 'Sweet glazed donut',
    emoji: '🍩'
  },
  {
    id: 6,
    name: 'Sushi',
    description: 'Fresh sushi roll',
    emoji: '🍣'
  }
]

const handlePurchase = async (product) => {
  if (userPoints.value < 10) {
    alert('You don\'t have enough points!')
    return
  }

  const confirmed = confirm(`Purchase ${product.name} for 10 points?`)
  if (!confirmed) return

  purchasing.value = true

  try {
    // Call points/use endpoint
    const response = await api.post('/points/use/', {
      points: 10,
      reason: `Webshop purchase: ${product.name}`
    })

    // Update local store with new points from response
    const remainingPoints = response.data.data.remaining_points
    authStore.updatePoints(remainingPoints)

    alert(`✅ Successfully purchased ${product.name}!\nRemaining points: ${remainingPoints}`)
  } catch (error) {
    console.error('Purchase failed:', error)

    // Check if it's an insufficient points error
    if (error.response?.status === 400) {
      alert('❌ Insufficient points!')
    } else {
      alert('❌ Purchase failed. Please try again.')
    }
  } finally {
    purchasing.value = false
  }
}

const handleClose = () => {
  if (!purchasing.value) {
    emit('close')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6b7280;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
}

.points-balance {
  padding: 16px 24px;
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.125rem;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.product-card {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: all 0.2s;
}

.product-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.product-image {
  font-size: 3rem;
  margin-bottom: 8px;
}

.product-name {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.product-description {
  margin: 0 0 12px 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.product-footer {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: auto;
}

.product-price {
  font-weight: 600;
  color: #667eea;
}

.buy-btn {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
}

.buy-btn:hover:not(:disabled) {
  background-color: #5568d3;
}

.buy-btn:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
}
</style>
