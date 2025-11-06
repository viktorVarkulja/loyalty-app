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
}

.layout-wrapper {
  width: 100%;
  min-height: 100vh;
  position: relative;
  background-color: #f5f5f5;
  max-width: 100%;
  margin: 0 auto;
}

.main-content {
  padding-bottom: 80px; /* Space for bottom nav */
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* Tablet - constrain width */
@media (min-width: 640px) and (max-width: 1023px) {
  .main-layout {
    display: flex;
    justify-content: center;
  }

  .layout-wrapper {
    max-width: 640px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
  }
}

/* Desktop - full width */
@media (min-width: 1024px) {
  .layout-wrapper {
    max-width: 100%;
  }

  .main-content {
    max-width: 100%;
    width: 100%;
    padding-left: 40px;
    padding-right: 40px;
  }
}

@media (min-width: 1536px) {
  .main-content {
    padding-left: 60px;
    padding-right: 60px;
  }
}
</style>
