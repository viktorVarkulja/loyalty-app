<template>
  <div class="min-h-screen bg-gray-100 sm:flex sm:justify-center md:block">
    <div class="w-full min-h-screen relative bg-gray-100 max-w-full mx-auto sm:max-w-[640px] sm:shadow-[0_0_30px_rgba(0,0,0,0.1)] sm:bg-white md:max-w-full lg:max-w-full">
      <main class="pb-20 min-h-screen bg-gray-100 lg:px-10 lg:w-full lg:max-w-full 2xl:px-[60px]">
        <slot />
      </main>
      <BottomNav />
    </div>
  </div>
</template>

<script setup>
import BottomNav from './BottomNav.vue'
</script>
