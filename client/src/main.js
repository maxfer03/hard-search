import 'primevue/resources/themes/fluent-light/theme.css'
import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import Wind from '@/presets/wind';
import Button from "primevue/button"
import App from './App.vue'
import router from './router'
import { inject } from '@vercel/analytics';
const app = createApp(App)

app.use(createPinia())
app.component('Button', Button)
app.use(router)
app.use(PrimeVue, {
  unstyled: true,
  pt: Wind
})
app.mount('#app')
inject()
