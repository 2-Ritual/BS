import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { h } from 'vue';

const routes = [
    {
        path: '/login',
        name: '登录页',
        component: () => import('../components/login_page.vue')
    },
    {
        path: '/register',
        name: '注册页',
        component: () => import('../components/register_page.vue')
    },
    {
        path: '/404',
        name: 'NoPage 404',
        component: () => import('../components/404.vue'),
        meta: { hidden: true }
    },
    {
        path: '/:pathMatch(.*)',
        redirect: '/404',
        meta: { hidden: true }
    },
    {
        path: '/',
        redirect: '/login',
        meta: { hidden: true }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

let expire = 21600000;

//路由守卫
//全局守卫，登录拦截
//进行路由拦截：当没有登陆标识，直接打回登陆页面，如何避免退回到 登陆页呢？
router.beforeEach((to, from, next) => {
    // 从本地缓存中获取保存的 token 信息
    const tokenObj = JSON.parse(window.localStorage.getItem('isLogin'))
    if (to.path === "/login") {
        next()
    } else {
        // 如果没有token，强制跳转到登录页面；如果有，则判断token时间是否过期
        if (!tokenObj || !tokenObj.token) {
            next('/login')
        } else {
            let date = new Date().getTime();
            if (date - tokenObj.startTime > expire) {
                window.localStorage.removeItem('isLogin');
                next('/login')
                ElMessage({
                    message: h('p', null, [
                        h('span', null, '登录状态过期'),
                        h('i', { style: 'color: teal' }, '请重新登录！'),
                    ]),
                })
            } else {
                next();
            }
        }
    }
});

export default router