import { createApp } from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Crypto from 'crypto-js'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Signin from './components/SignIn.vue'
import Home from './components/Home.vue'
import Register from './components/Register.vue'
import Results from './components/Result.vue'
import Detail from './components/Detail.vue'

const routes = [
  { path: '/', component: Signin },
  { path: '/register', component: Register },
  { path: '/home', component: Home },
  { path: '/result', component: Results },
  { path: '/detail', component: Detail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.use(VueAxios,axios)
app.use(Crypto)
app.mount('#app')

