<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Serbian Loyalty App</h1>
      <h2>Register</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="John Doe"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="your@email.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="At least 8 characters"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="password_confirm">Confirm Password</label>
          <input
            id="password_confirm"
            v-model="form.password_confirm"
            type="password"
            required
            placeholder="Confirm your password"
            :disabled="isLoading"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="isLoading">
          {{ isLoading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <p class="auth-link">
        Already have an account?
        <router-link to="/login">Login here</router-link>
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
  name: '',
  email: '',
  password: '',
  password_confirm: ''
})

const isLoading = ref(false)
const error = ref(null)

const handleRegister = async () => {
  // Validate passwords match
  if (form.value.password !== form.value.password_confirm) {
    error.value = 'Passwords do not match'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await authService.register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password,
      password_confirm: form.value.password_confirm
    })

    // Store tokens
    authStore.setTokens(response.tokens.access, response.tokens.refresh)

    // Store user data
    authStore.setUser(response.user)

    // Redirect to home
    router.push('/')
  } catch (err) {
    if (err.response?.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        error.value = Object.values(errorData).flat().join(', ')
      } else {
        error.value = errorData
      }
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #667eea;
  margin: 0 0 10px 0;
  font-size: 24px;
  text-align: center;
}

h2 {
  color: #333;
  margin: 0 0 30px 0;
  font-size: 28px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 12px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
  margin-bottom: 20px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.auth-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>
