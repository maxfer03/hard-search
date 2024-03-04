<template>
  <div class="search-bar-module" >
    <div class="search" >
      <span class="search-field">
        <i v-if="loadingProducts" class="search-field-spinner pi pi-spin pi-spinner" />
        <InputText @keydown.enter="search" v-model="query" placeholder="Search" />
      </span>
      <Button @click="search" icon="pi pi-search"  rounded size="small"/>
    </div>
    <div v-if="products.length > 0" class="search-data">
      <span v-if="loadingProducts">page {{ searchInfo.current_page }} of {{ searchInfo.total_pages }}</span>
      <span>{{ products.length }} item{{products.length === 1 ? '' : 's'}} found!</span>
    </div>
    <div v-else-if="noItems && products.length === 0" class="search-data">
      Sorry! No items found
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import InputText from 'primevue/inputtext';
import axios from 'axios';
import { useDataStore } from '@/stores/data'
import { storeToRefs } from 'pinia'
import bell from '../assets/finish.mp3'





const audio = new Audio(bell);

const store = useDataStore()

const {mergeProducts, resetProducts, isLoadingProducts, resetSearchInfo} = store
const { products, query, loadingProducts, searchInfo } = storeToRefs(store)

const noItems = ref(false);

const resetToDefault = () => {
  noItems.value = false
  resetProducts()
  resetSearchInfo()
  isLoadingProducts(true)
}


const search = async () => {
  resetToDefault()
  let oopsError = 0
  while (oopsError === 0) {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/search`,
       { 
        params: 
        { 
          query: query.value,
          page: searchInfo.value.current_page
        } 
      });
      console.log(response)
      mergeProducts(response.data.found)
      if(!searchInfo.value.total_pages && !searchInfo.value.url) {
        searchInfo.value.total_pages = response.data.info.total_pages
        searchInfo.value.url = response.data.info.url
      }
      searchInfo.value.current_page++
    } catch (error) {
      noItems.value = true
      oopsError = 1
      console.error(error);
    }
  }
  isLoadingProducts(false)
  audio.play();

}

</script>

<style lang="scss" scoped>
.search-bar-module {
  @apply flex flex-col items-center gap-2;
  .search {
    @apply flex items-center gap-2;

    &-field {
      @apply relative;
      &-spinner {
        @apply absolute top-2/4 -mt-2 right-3 text-surface-400 dark:text-surface-600;
      }

      input {
        @apply w-[250px] pr-9
      }
    }

    button {
      @apply w-full
    }

  }

  .search-data {
    @apply min-h-[50px] mt-3 flex flex-col items-center justify-center gap-1;
  }

}
</style>