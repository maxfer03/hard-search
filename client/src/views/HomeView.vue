<template>
  <div class="home-view"> 
    <h1 class="title" >Hard Search</h1>
  <SearchBarComponentComponent/>
  <div class="dashboard" >
    <TableComponent/>
  </div>
  </div>
</template>

<script setup>
import SearchBarComponentComponent from "@/components/SearchBarComponent.vue"
import TableComponent from "@/components/TableComponent.vue"
</script>

<style lang="scss" scoped >
.home-view {
  @apply flex flex-col py-5 gap-5 items-center;
  .title {
    @apply text-primary-500;
  }
  .dashboard {
    @apply flex items-center flex-col gap-2 lg:flex-row lg:items-start 
  }
}
</style>