import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Badge from 'primevue/badge'
import ProgressBar from 'primevue/progressbar'
import Skeleton from 'primevue/skeleton'
import Tag from 'primevue/tag'
import 'primeicons/primeicons.css'
import axios from 'axios'
axios.defaults.baseURL = ''

const app = createApp(App)

app.use(router)
app.use(PrimeVue, { theme: { preset: Aura } })
app.use(ToastService)

app.component('Toast', Toast)
app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('InputText', InputText)
app.component('Badge', Badge)
app.component('ProgressBar', ProgressBar)
app.component('Skeleton', Skeleton)
app.component('Tag', Tag)

app.config.globalProperties.$axios = axios

app.mount('#app')
