<template>
  <!-- 导航栏：固定在顶部，带渐变背景 -->
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background: linear-gradient(135deg, #40b4e5, #e0e5ec) !important;">
    <div class="container">
      <!-- 网站品牌名称和链接 -->
      <router-link class="navbar-brand" to="/">智能房产<span class="text-warning">AI</span></router-link>
      <!-- 移动端折叠按钮 -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- 导航菜单 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- 导航链接 -->
        <ul class="navbar-nav ms-auto">
          <!-- 首页链接 -->
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/' }" to="/">首页</router-link>
          </li>
          <!-- 房源列表链接 -->
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/house-list' }" to="/house-list">房源列表</router-link>
          </li>
          <!-- 用户中心链接 -->
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/user-center' }" to="/user-center">用户中心</router-link>
          </li>
          <!-- 智能客服链接 -->
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/chat' }" to="/chat">智能客服</router-link>
          </li>
        </ul>
        <!-- 登录/用户信息区域 -->
        <div class="ms-3">
          <!-- 未登录显示登录按钮 -->
          <button v-if="!isAuthenticated" class="btn btn-light rounded-pill px-4" @click="$router.push('/login')">登录</button>
          <!-- 已登录显示用户下拉菜单 -->
          <div v-else class="dropdown">
            <button class="btn btn-light rounded-pill px-4 dropdown-toggle" type="button" data-bs-toggle="dropdown">
              {{ username }}
            </button>
            <ul class="dropdown-menu">
              <li><router-link class="dropdown-item" to="/user-center">个人中心</router-link></li>
              <li><a class="dropdown-item" href="#" @click="handleLogout">退出登录</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

export default {
  name: 'Navbar',
  setup() {
    const userStore = useUserStore()
    const { isAuthenticated, user } = storeToRefs(userStore)
    return { isAuthenticated, user }
  },
  computed: {
    username() {
      return this.user?.username || '未登录'
    }
  },
  methods: {
    async handleLogout() {
      const userStore = useUserStore()
      await userStore.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
/* 确保导航栏背景色正确显示 */
.navbar {
  background: linear-gradient(135deg, #40b4e5, #e0e5ec) !important;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  z-index: 1030;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

/* 品牌名称样式 */
.navbar-brand {
  font-weight: 700;
  letter-spacing: 0.5px;
  color: white !important;
}

/* 导航链接样式 */
.nav-link {
  color: rgba(255, 255, 255, 0.9) !important;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-link:hover, 
.nav-link.active {
  color: white !important;
  transform: translateY(-2px);
}

/* 确保移动设备上的下拉菜单不超出屏幕 */
@media (max-width: 768px) {
  .navbar-collapse {
    max-width: 100vw;
    overflow-x: hidden;
  }
  
  .navbar-nav {
    width: 100%;
  }
}
</style> 