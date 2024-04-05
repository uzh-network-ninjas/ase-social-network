import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { i18n } from '@/i18n'
import PrimeVue from 'primevue/config'
import presets from '@/presets'
import Ripple from 'primevue/ripple'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(PrimeVue, {
  unstyled: true,
  ripple: true,
  pt: presets
})

app.directive('ripple', Ripple)

app.mount('#app')
