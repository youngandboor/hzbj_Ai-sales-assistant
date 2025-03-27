import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

// 导入组件
import Home from '../views/Home.vue'
import HouseList from '../views/HouseList.vue'
import UserCenter from '../views/UserCenter.vue'
import Login from '../views/Login.vue'
import AIChat from '../views/AIChat.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/house-list',
      name: 'HouseList',
      component: HouseList
    },
    {
      path: '/user-center',
      name: 'UserCenter',
      component: UserCenter,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/chat',
      name: 'chat',
      component: AIChat
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router 