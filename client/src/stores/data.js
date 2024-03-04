import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', () => {
  const query = ref('')
  const loadingProducts = ref(false)
  const searchInfo = ref({
    current_page: 0,
    total_pages: null,
    url: null
  })
  const products = ref([])
  function mergeProducts(arr) {
    products.value = [...products.value, ...arr]
  }

  function resetProducts() {
    products.value = []
  }

  const isLoadingProducts = (value) => {
    loadingProducts.value = value
  } 

  const resetSearchInfo = () => {
    searchInfo.value = {
      current_page: 0,
      total_pages: null,
      url: ''
    }
  }

  return { query, loadingProducts, searchInfo, products, mergeProducts, resetProducts, isLoadingProducts, resetSearchInfo }
})
