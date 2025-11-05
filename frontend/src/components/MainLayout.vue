<template>
  <div class="main-layout">
    <div class="layout-wrapper">
      <main class="main-content">
        <slot />
      </main>
      <BottomNav />
    </div>
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
  justify-content: center;
}

.layout-wrapper {
  width: 100%;
  min-height: 100vh;
  position: relative;
}

.main-content {
  padding-bottom: 80px; /* Space for bottom nav */
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* Tablet and Desktop */
@media (min-width: 768px) {
  .layout-wrapper {
    max-width: 768px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
  }
}

@media (min-width: 1024px) {
  .layout-wrapper {
    max-width: 900px;
  }
}
</style>
