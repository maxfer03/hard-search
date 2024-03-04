<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { SpeedInsights } from '@vercel/speed-insights/vue';
</script>

<template>
  <main class="app">
    <SpeedInsights />
    <!-- <header>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </header> -->
    <RouterView />
    <footer class="footer" >
      <div class="promo">
        By <a class="link" href="https://www.linkedin.com/in/maxfarenas/" target="_blank" >Max Fernandez</a>
      </div>
    </footer>
  </main>
</template>

<style scoped lang="scss">
main {
  header {
  @apply pt-10 flex flex-col gap-2 items-center;
    nav {
      @apply flex gap-2;
    }
  }
  footer {
    @apply flex justify-center items-center mb-5 
  }
}
</style>
