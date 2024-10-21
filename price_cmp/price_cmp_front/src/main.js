import { createApp } from 'vue';
import App from './App.vue';
import login_page from './components/login_page.vue';
import register_page from './components/register_page.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { path: '/login', component: login_page },
    { path: '/register', component: register_page }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

createApp(App).use(router).mount('#app');
