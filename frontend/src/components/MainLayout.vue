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
  display: flex;
  flex-direction: column;
}

.main-content {
  padding-bottom: 80px; /* Space for bottom nav */
  min-height: 100vh;
  width: 100%;
}

/* Desktop centering */
@media (min-width: 768px) {
  .main-layout {
    align-items: center;
  }

  .main-content {
    max-width: 768px;
    width: 100%;
  }
}

@media (min-width: 1024px) {
  .main-content {
    max-width: 900px;
  }
}
</style>
