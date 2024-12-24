import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import User from '../views/User/index.vue';
import { ElementPlus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: import('../views/Login/index.vue'),
    children: [
      // 添加子路由
      // {
      //   path: '/example',
      //   name: 'Example',
      //   component: ExampleComponent,
      // },
    ],
  },
  {
    path: '/search',
    name: 'Search',
    component: import('../views/Search/index.vue'),
    meta: { requiresAuth: true },
    children: [
      // 添加子路由
      // {
      //   path: '/example',
      //   name: 'Example',
      //   component: ExampleComponent,
      // },
    ],
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    meta: { requiresAuth: true },
    children: [
      // 添加子路由
      // {
      //   path: '/example',
      //   name: 'Example',
      //   component: ExampleComponent,
      // },
    ],
  },
];
 
const router = createRouter({
  history: createWebHistory(),
  routes,
});
 // 导航守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('uid'); // 检查登录状态的函数，自行实现

  if (to.matched.some(route => route.meta.requiresAuth)) {
    // 如果路由需要登录验证
    if (isLoggedIn) {
      // 如果已登录，允许进入
      next();
    } else {
      // 如果未登录，重定向到登录页
      ElMessage.error('请先登录！');
      next('/login');
    }
  } else {
    // 如果路由不需要登录验证，直接进入
    next();
  }
});
export default router;