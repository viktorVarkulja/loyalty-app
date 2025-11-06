<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-100">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-8 px-5">
        <h1 class="m-0 mb-2 text-[28px] font-bold">Products</h1>
        <p class="m-0 opacity-90 text-base">Browse products and see how many points you can earn</p>
      </div>

      <!-- Search Bar -->
      <div class="p-5 -mt-5">
        <div class="bg-white rounded-xl py-3 px-4 flex items-center gap-3 shadow-[0_4px_12px_rgba(0,0,0,0.1)]">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 shrink-0">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search products..."
            class="flex-1 border-none outline-none text-base text-gray-800 placeholder:text-gray-400"
          />
          <button v-if="searchQuery" @click="clearSearch" class="bg-gray-100 border-none rounded-full w-7 h-7 flex items-center justify-center cursor-pointer text-gray-500 transition-colors hover:bg-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-[60px] px-5 text-gray-400">
        <div class="w-10 h-10 border-4 border-gray-100 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
        <p>Loading products...</p>
      </div>

      <!-- Products List -->
      <div v-else-if="displayedProducts.length > 0" class="pb-5 px-5 flex flex-col gap-3">
        <div
          v-for="product in displayedProducts"
          :key="product.id"
          class="bg-white rounded-xl p-4 flex items-center gap-4 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)]"
        >
          <div class="w-14 h-14 bg-gradient-to-br from-success to-green-600 rounded-xl flex items-center justify-center text-white shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="m-0 mb-2 text-base font-semibold text-gray-800 whitespace-nowrap overflow-hidden text-ellipsis">{{ product.name }}</h3>
            <div class="flex items-center gap-2">
              <span class="text-xs font-medium py-1 px-2 rounded-md uppercase" :class="product.status.toLowerCase() === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                {{ product.status }}
              </span>
            </div>
          </div>
          <div class="shrink-0">
            <div class="bg-gradient-to-br from-primary to-primary-dark text-white py-2 px-4 rounded-[20px] flex items-center gap-1.5 font-semibold text-base">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              <span>{{ product.points }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-[60px] px-5 text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-5 opacity-30 inline-block">
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <h3 class="m-0 mb-2 text-xl text-gray-800">No products found</h3>
        <p v-if="searchQuery" class="m-0 mb-6 text-sm">Try searching for something else</p>
        <p v-else class="m-0 mb-6 text-sm">No products available at the moment</p>
        <button v-if="searchQuery" @click="clearSearch" class="py-3 px-6 bg-gradient-to-br from-primary to-primary-dark text-white border-none rounded-lg font-semibold cursor-pointer transition-transform duration-200 hover:-translate-y-0.5">
          Clear Search
        </button>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1 && !searchQuery" class="py-5 px-5 flex items-center justify-between gap-4">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="py-2.5 px-5 bg-white text-primary border-2 border-primary rounded-lg font-semibold cursor-pointer transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-primary hover:text-white"
        >
          Previous
        </button>
        <span class="text-sm text-gray-500 font-medium">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="py-2.5 px-5 bg-white text-primary border-2 border-primary rounded-lg font-semibold cursor-pointer transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-primary hover:text-white"
        >
          Next
        </button>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { productsService } from '../services'
import MainLayout from '../components/MainLayout.vue'

const products = ref([])
const searchResults = ref([])
const searchQuery = ref('')
const isLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)

const displayedProducts = computed(() => {
  return searchQuery.value ? searchResults.value : products.value
})

const fetchProducts = async (page = 1) => {
  isLoading.value = true
  try {
    const data = await productsService.getProducts(page)
    products.value = data.results
    totalCount.value = data.count
    totalPages.value = Math.ceil(data.count / 20) // 20 items per page
    currentPage.value = page
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    isLoading.value = false
  }
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  isLoading.value = true
  try {
    const data = await productsService.searchProducts(searchQuery.value)
    searchResults.value = data
  } catch (error) {
    console.error('Failed to search products:', error)
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
}

const previousPage = () => {
  if (currentPage.value > 1) {
    fetchProducts(currentPage.value - 1)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    fetchProducts(currentPage.value + 1)
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
