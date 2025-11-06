<template>
  <router-view />

  <!-- Session Expired Modal -->
  <SessionExpiredModal :isVisible="showSessionExpiredModal" @close="closeSessionExpiredModal" />

  <!-- PWA Update Prompt -->
  <div v-if="needRefresh" class="fixed bottom-20 left-1/2 -translate-x-1/2 bg-white rounded-xl shadow-2xl p-4 z-[9999] max-w-[90%] w-[400px] flex flex-col gap-3 animate-slide-up">
    <div class="flex items-center gap-3 text-gray-800 font-medium">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary shrink-0">
        <path d="M21 2v6h-6M3 12a9 9 0 0 1 15-6.7L21 8M3 22v-6h6M21 12a9 9 0 0 1-15 6.7L3 16"></path>
      </svg>
      <span>New version available!</span>
    </div>
    <div class="flex gap-2">
      <button @click="updateServiceWorker" class="flex-1 px-4 py-2.5 bg-gradient-to-r from-primary to-primary-dark text-white rounded-lg font-semibold text-sm cursor-pointer transition-all hover:-translate-y-0.5 hover:shadow-lg hover:shadow-primary/40">
        Update
      </button>
      <button @click="closePrompt" class="flex-1 px-4 py-2.5 bg-gray-100 text-gray-600 rounded-lg font-semibold text-sm cursor-pointer transition-colors hover:bg-gray-200">
        Later
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'
import { useAuthStore } from '@/stores/auth'
import SessionExpiredModal from '@/components/SessionExpiredModal.vue'

const authStore = useAuthStore()
const showSessionExpiredModal = ref(false)

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

const closeSessionExpiredModal = () => {
  showSessionExpiredModal.value = false
  sessionStorage.removeItem('sessionExpired')
}

// Check token expiration on app mount
onMounted(async () => {
  // Check if we were redirected due to session expiration
  if (sessionStorage.getItem('sessionExpired') === 'true') {
    showSessionExpiredModal.value = true
    return
  }

  // Check token expiration if user is authenticated
  if (authStore.isAuthenticated) {
    const isTokenValid = await authStore.checkTokenExpiration()

    if (!isTokenValid) {
      // Show session expired modal
      showSessionExpiredModal.value = true
      sessionStorage.setItem('sessionExpired', 'true')
    }
  }
})
</script>

<style>
@keyframes slide-up {
  from {
    transform: translate(-50%, 100px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
</style>
