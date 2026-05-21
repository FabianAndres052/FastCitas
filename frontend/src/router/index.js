import { createRouter, createWebHistory } from 'vue-router'
import BienvenidaView from '../views/BienvenidaView.vue'
import LoginView from '../views/LoginView.vue'
import RegistroView from '../views/RegistroView.vue'
import HomeView from '../views/HomeView.vue'
import AdminView from '../views/AdminView.vue'

const rutas = [
  { path: '/', component: BienvenidaView },
  { path: '/login', component: LoginView },
  { path: '/registro', component: RegistroView },
  {
    path: '/inicio',
    component: HomeView,
    beforeEnter: (to, from, next) => {
      const usuario = localStorage.getItem('usuario')
      if (!usuario) next('/login')
      else next()
    }
  },
  {
    path: '/admin',
    component: AdminView,
    beforeEnter: (to, from, next) => {
      const usuario = JSON.parse(localStorage.getItem('usuario') || '{}')
      if (!usuario || usuario.rol !== 'admin') next('/login')
      else next()
    }
  }
]

const enrutador = createRouter({
  history: createWebHistory(),
  routes: rutas
})

export default enrutador