<template>
  <MainLayout>
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <div class="bg-gradient-to-br from-primary to-primary-dark text-white p-6 pb-8">
        <h1 class="text-2xl font-bold m-0">Favorite Stores</h1>
        <p class="mt-2 text-white/90 text-sm">Manage your favorite stores for personalized offers</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-5 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        <p class="mt-2 text-gray-600">Loading stores...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="p-5">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {{ error }}
        </div>
      </div>

      <!-- Content -->
      <div v-else class="p-5">
        <!-- Favorite Stores Section -->
        <div v-if="favoriteStores.length > 0" class="mb-6">
          <h2 class="text-lg font-semibold text-gray-800 mb-3">Your Favorites</h2>
          <div class="space-y-3">
            <div
              v-for="favorite in favoriteStores"
              :key="favorite.id"
              class="bg-white rounded-xl p-4 shadow-sm flex items-center justify-between"
            >
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center text-white font-bold text-lg">
                  {{ favorite.store.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800 m-0">{{ favorite.store.name }}</h3>
                  <p v-if="favorite.store.location" class="text-sm text-gray-500 m-0 mt-1">
                    {{ favorite.store.location }}
                  </p>
                </div>
              </div>
              <button
                @click="removeFavorite(favorite.id)"
                :disabled="removing === favorite.id"
                class="px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors disabled:opacity-50"
              >
                {{ removing === favorite.id ? 'Removing...' : 'Remove' }}
              </button>
            </div>
          </div>
        </div>

        <!-- All Stores Section -->
        <div class="mb-3">
          <h2 class="text-lg font-semibold text-gray-800 mb-3">
            {{ favoriteStores.length > 0 ? 'Add More Stores' : 'All Stores' }}
          </h2>
        </div>

        <!-- Empty State -->
        <div v-if="availableStores.length === 0 && allStores.length === 0" class="text-center py-12">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
          </div>
          <p class="text-gray-500">No stores available</p>
        </div>

        <!-- Available Stores List -->
        <div v-else-if="availableStores.length === 0 && favoriteStores.length > 0" class="text-center py-12">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-600">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <p class="text-gray-500">All stores are in your favorites!</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="store in availableStores"
            :key="store.id"
            class="bg-white rounded-xl p-4 shadow-sm flex items-center justify-between"
          >
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center text-gray-600 font-bold text-lg">
                {{ store.name.charAt(0).toUpperCase() }}
              </div>
              <div>
                <h3 class="font-semibold text-gray-800 m-0">{{ store.name }}</h3>
                <p v-if="store.location" class="text-sm text-gray-500 m-0 mt-1">
                  {{ store.location }}
                </p>
              </div>
            </div>
            <button
              @click="addFavorite(store.id)"
              :disabled="adding === store.id"
              class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50"
            >
              {{ adding === store.id ? 'Adding...' : 'Add' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productsService } from '../services'
import MainLayout from '../components/MainLayout.vue'

const isLoading = ref(true)
const error = ref(null)
const allStores = ref([])
const favoriteStores = ref([])
const adding = ref(null)
const removing = ref(null)

// Compute available stores (not in favorites)
const availableStores = computed(() => {
  const favoriteStoreIds = favoriteStores.value.map(f => f.store.id)
  return allStores.value.filter(store => !favoriteStoreIds.includes(store.id))
})

// Fetch all data
const fetchData = async () => {
  isLoading.value = true
  error.value = null

  try {
    const [stores, favorites] = await Promise.all([
      productsService.getStores(),
      productsService.getFavoriteStores()
    ])

    allStores.value = stores
    favoriteStores.value = favorites
  } catch (err) {
    console.error('Error fetching stores:', err)
    error.value = err.response?.data?.detail || 'Failed to load stores. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Add store to favorites
const addFavorite = async (storeId) => {
  adding.value = storeId

  try {
    const newFavorite = await productsService.addFavoriteStore(storeId)
    favoriteStores.value.unshift(newFavorite)
  } catch (err) {
    console.error('Error adding favorite:', err)
    const message = err.response?.data?.detail || 'Failed to add favorite store'
    alert(message)
  } finally {
    adding.value = null
  }
}

// Remove store from favorites
const removeFavorite = async (favoriteId) => {
  removing.value = favoriteId

  try {
    await productsService.removeFavoriteStore(favoriteId)
    favoriteStores.value = favoriteStores.value.filter(f => f.id !== favoriteId)
  } catch (err) {
    console.error('Error removing favorite:', err)
    const message = err.response?.data?.detail || 'Failed to remove favorite store'
    alert(message)
  } finally {
    removing.value = null
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Add any additional component-specific styles here */
</style>
