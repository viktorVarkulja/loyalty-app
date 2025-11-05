<template>
  <div class="main-layout">
    <main class="main-content">
      <slot />
    </main>
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from './BottomNav.vue'
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  padding-bottom: 80px; /* Space for bottom nav */
  min-height: 100vh;
}
</style>
