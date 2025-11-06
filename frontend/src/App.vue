<template>
  <router-view />

  <!-- PWA Update Prompt -->
  <div v-if="needRefresh" class="pwa-toast">
    <div class="pwa-message">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 2v6h-6M3 12a9 9 0 0 1 15-6.7L21 8M3 22v-6h6M21 12a9 9 0 0 1-15 6.7L3 16"></path>
      </svg>
      <span>New version available!</span>
    </div>
    <div class="pwa-actions">
      <button @click="updateServiceWorker" class="pwa-btn primary">Update</button>
      <button @click="closePrompt" class="pwa-btn secondary">Later</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'

const { needRefresh, updateServiceWorker } = useRegisterSW({
  onRegistered(registration) {
    console.log('Service Worker registered:', registration)
  },
  onRegisterError(error) {
    console.error('Service Worker registration error:', error)
  }
})

const closePrompt = () => {
  needRefresh.value = false
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

/* PWA Update Toast */
.pwa-toast {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  padding: 16px 20px;
  z-index: 9999;
  max-width: 90%;
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 100px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

.pwa-message {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #333;
  font-weight: 500;
}

.pwa-message svg {
  color: #667eea;
  flex-shrink: 0;
}

.pwa-actions {
  display: flex;
  gap: 8px;
}

.pwa-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.pwa-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.pwa-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.pwa-btn.secondary {
  background: #f3f4f6;
  color: #6b7280;
}

.pwa-btn.secondary:hover {
  background: #e5e7eb;
}
</style>
