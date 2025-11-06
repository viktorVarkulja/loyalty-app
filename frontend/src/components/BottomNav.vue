<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white flex justify-around items-center py-2 pb-[calc(0.5rem+env(safe-area-inset-bottom))] shadow-[0_-2px_10px_rgba(0,0,0,0.1)] z-[100] sm:max-w-[640px] sm:left-1/2 sm:-translate-x-1/2 sm:rounded-t-2xl lg:max-w-none lg:left-1/2 lg:-translate-x-1/2 lg:w-auto lg:justify-center lg:gap-10 lg:px-10 2xl:gap-[60px] 2xl:px-[60px]">
    <router-link to="/" class="flex flex-col items-center justify-center no-underline text-gray-400 transition-colors duration-300 py-2 px-4 min-w-[60px] sm:py-2.5 sm:px-5 sm:min-w-[80px] lg:py-3 lg:px-8 lg:min-w-[120px] 2xl:py-3.5 2xl:px-10 2xl:min-w-[140px]" :class="{ 'text-primary': isActive('/') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-1">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span class="text-xs font-medium sm:text-[13px] lg:text-[15px]">Home</span>
    </router-link>

    <router-link to="/products" class="flex flex-col items-center justify-center no-underline text-gray-400 transition-colors duration-300 py-2 px-4 min-w-[60px] sm:py-2.5 sm:px-5 sm:min-w-[80px] lg:py-3 lg:px-8 lg:min-w-[120px] 2xl:py-3.5 2xl:px-10 2xl:min-w-[140px]" :class="{ 'text-primary': isActive('/products') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-1">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
      <span class="text-xs font-medium sm:text-[13px] lg:text-[15px]">Products</span>
    </router-link>

    <router-link to="/scan" class="flex flex-col items-center justify-center no-underline text-white bg-gradient-to-br from-primary to-primary-dark rounded-full w-14 h-14 -mt-5 shadow-[0_4px_12px_rgba(102,126,234,0.4)] lg:py-3.5 lg:px-9" :class="{ 'text-white': isActive('/scan') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="9" y1="3" x2="9" y2="21"></line>
        <line x1="15" y1="3" x2="15" y2="21"></line>
      </svg>
      <span class="hidden">Scan</span>
    </router-link>

    <router-link to="/transactions" class="flex flex-col items-center justify-center no-underline text-gray-400 transition-colors duration-300 py-2 px-4 min-w-[60px] sm:py-2.5 sm:px-5 sm:min-w-[80px] lg:py-3 lg:px-8 lg:min-w-[120px] 2xl:py-3.5 2xl:px-10 2xl:min-w-[140px]" :class="{ 'text-primary': isActive('/transactions') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-1">
        <line x1="12" y1="1" x2="12" y2="23"></line>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
      </svg>
      <span class="text-xs font-medium sm:text-[13px] lg:text-[15px]">History</span>
    </router-link>

    <router-link to="/profile" class="flex flex-col items-center justify-center no-underline text-gray-400 transition-colors duration-300 py-2 px-4 min-w-[60px] sm:py-2.5 sm:px-5 sm:min-w-[80px] lg:py-3 lg:px-8 lg:min-w-[120px] 2xl:py-3.5 2xl:px-10 2xl:min-w-[140px]" :class="{ 'text-primary': isActive('/profile') }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-1">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
      <span class="text-xs font-medium sm:text-[13px] lg:text-[15px]">Profile</span>
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
