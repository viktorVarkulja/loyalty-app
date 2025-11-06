<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="handleClose">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Session Expired</h2>
      </div>
      <div class="modal-body">
        <p>Your session has expired. Please log in again to continue.</p>
      </div>
      <div class="modal-footer">
        <button @click="handleLogin" class="btn-primary">
          Login Again
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = () => {
  // Clear authentication state
  authStore.clearAuth()

  // Close the modal
  emit('close')

  // Redirect to login page
  router.push('/login')
}

const handleClose = () => {
  // Allow closing by clicking overlay, but still redirect to login
  handleLogin()
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-width: 400px;
  width: 90%;
  padding: 0;
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
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  margin: 0;
  color: #6b7280;
  line-height: 1.5;
  font-size: 1rem;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-primary:active {
  background-color: #1d4ed8;
}

.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}
</style>
