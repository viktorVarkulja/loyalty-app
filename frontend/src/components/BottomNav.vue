<template>
  <nav class="bottom-nav">
    <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>Home</span>
    </router-link>

    <router-link to="/products" class="nav-item" :class="{ active: isActive('/products') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
      <span>Products</span>
    </router-link>

    <router-link to="/scan" class="nav-item scan-btn" :class="{ active: isActive('/scan') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="9" y1="3" x2="9" y2="21"></line>
        <line x1="15" y1="3" x2="15" y2="21"></line>
      </svg>
    </router-link>

    <router-link to="/transactions" class="nav-item" :class="{ active: isActive('/transactions') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="1" x2="12" y2="23"></line>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
      </svg>
      <span>History</span>
    </router-link>

    <router-link to="/profile" class="nav-item" :class="{ active: isActive('/profile') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
      <span>Profile</span>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const isActive = (path) => {
  return computed(() => route.path === path)
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: #9ca3af;
  transition: color 0.3s;
  padding: 8px 16px;
  min-width: 60px;
}

.nav-item svg {
  margin-bottom: 4px;
}

.nav-item span {
  font-size: 12px;
  font-weight: 500;
}

.nav-item.active {
  color: #667eea;
}

.nav-item.scan-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  margin-top: -20px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-item.scan-btn svg {
  margin-bottom: 0;
}

.nav-item.scan-btn span {
  display: none;
}
</style>
