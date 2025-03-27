<script setup>
// 导入用户状态管理
import { useUserStore } from './stores/user'
import { storeToRefs } from 'pinia'
// 导入导航栏组件
import Navbar from './components/Navbar.vue'

// 使用用户状态存储
const userStore = useUserStore()
// 解构获取用户认证状态和用户资料
const { isAuthenticated, userProfile } = storeToRefs(userStore)
</script>

<template>
  <!-- 整个应用的容器 -->
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <Navbar />
    
    <!-- 主内容区域，用于显示路由组件 -->
    <main class="main-content">
      <router-view></router-view>
    </main>

    <!-- 页脚区域 -->
    <footer class="footer">
      <div class="container">
        <p>© 2025 智能房产AI. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* CSS变量定义 */
:root {
  --primary-color: #40b4e5;
  --secondary-color: #e0e5ec;
  --accent-color: #ff006e;
  --light-color: #f8f9fa;
  --dark-color: #212529;
  --gradient-primary: linear-gradient(135deg, #40b4e5, #e0e5ec);
  --gradient-secondary: linear-gradient(135deg, #ff006e, #fb5607);
}

/* 重置所有元素的盒模型 */
*, *::before, *::after {
  box-sizing: border-box;
}

/* 应用容器样式 */
.app-container {
  /* 最小高度为视口高度，确保内容少时页面也能占满屏幕 */
  min-height: 100vh;
  /* 使用flex布局，便于页脚固定在底部 */
  display: flex;
  flex-direction: column;
  /* 网页端宽度设置 */
  width: 100%;
  margin: 0;
  padding: 0;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  padding-top: 76px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 内容包装器，确保所有内容都有正确的宽度和居中显示 */
.content-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 页脚样式 */
.footer {
  text-align: center;
  padding: 20px;
  background-color: #f5f7fa;
  /* 自动外边距置底 */
  margin-top: auto;
  width: 100%;
}

/* 全局HTML和BODY样式 */
html, body {
  /* 网页端宽度设置 */
  width: 100% !important;
  max-width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
  /* 确保不出现水平滚动条 */
  overflow-x: hidden !important;
  /* 确保覆盖默认样式 */
  display: block !important;
  place-items: initial !important;
  /* 字体设置 */
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--dark-color);
  background-color: #f5f7fa;
}

/* 所有图片适应容器 */
img {
  max-width: 100%;
  height: auto;
}

/* 容器宽度调整 */
.container {
  width: 100%;
  max-width: 1600px !important;
  margin: 0 auto !important;
  padding: 0 1rem !important;
}

/* 行布局修复 */
.row {
  margin: 0 -0.5rem;
  padding: 0;
  width: 100%;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color);
}

/* 覆盖默认的#app样式，确保宽度正确 */
#app {
  width: 100%;
  margin: 0;
  padding: 0;
  display: block;
}
</style>
