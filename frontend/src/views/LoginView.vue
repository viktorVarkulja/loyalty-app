<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary to-primary-dark p-5">
    <div class="bg-white py-10 px-10 rounded-xl shadow-[0_10px_40px_rgba(0,0,0,0.1)] w-full max-w-[400px]">
      <h1 class="text-primary m-0 mb-2.5 text-2xl text-center">Serbian Loyalty App</h1>
      <h2 class="text-gray-800 m-0 mb-8 text-[28px] text-center">Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="mb-5">
          <label for="email" class="block mb-2 text-gray-600 font-medium">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="your@email.com"
            :disabled="isLoading"
            class="w-full py-3 px-3 border-2 border-gray-200 rounded-lg text-base transition-colors box-border outline-none focus:border-primary disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <div class="mb-5">
          <label for="password" class="block mb-2 text-gray-600 font-medium">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="Your password"
            :disabled="isLoading"
            class="w-full py-3 px-3 border-2 border-gray-200 rounded-lg text-base transition-colors box-border outline-none focus:border-primary disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <div v-if="error" class="py-3 px-3 bg-red-50 border border-red-200 rounded-lg text-red-700 mb-5">
          {{ error }}
        </div>

        <button type="submit" class="w-full py-3.5 px-3.5 bg-gradient-to-br from-primary to-primary-dark text-white border-none rounded-lg text-base font-semibold cursor-pointer transition-transform duration-200 disabled:opacity-60 disabled:cursor-not-allowed hover:-translate-y-0.5" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="text-center mt-5 text-gray-600">
        Don't have an account?
        <router-link to="/register" class="text-primary no-underline font-semibold hover:underline">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authService } from '../services'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const isLoading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await authService.login({
      email: form.value.email,
      password: form.value.password
    })

    // Store tokens
    authStore.setTokens(response.access, response.refresh)

    // Store user data
    authStore.setUser(response.user)

    // Redirect to home
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
