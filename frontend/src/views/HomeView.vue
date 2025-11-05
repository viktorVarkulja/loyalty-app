<template>
  <div class="home">
    <h1>Welcome to Serbian Loyalty App!</h1>
    <p v-if="authStore.user">Hello, {{ authStore.userName }}!</p>
    <p>Your points: {{ authStore.userPoints }}</p>
    <button @click="handleLogout" class="btn-logout">Logout</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.home {
  padding: 40px;
  text-align: center;
}

h1 {
  color: #667eea;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  margin: 10px 0;
}

.btn-logout {
  margin-top: 20px;
  padding: 12px 24px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #c82333;
}
</style>
