<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // 添加AI客服配置
  window.difyChatbotConfig = {
    token: 'zRLo0mNPnh8PNH8q'
  }
  
  // 加载AI客服脚本
  const script = document.createElement('script')
  script.src = 'https://udify.app/embed.min.js'
  script.id = 'zRLo0mNPnh8PNH8q'
  script.defer = true
  document.head.appendChild(script)
})
</script>

<template>
  <div class="ai-chat-button">
    <!-- AI客服按钮会由脚本自动插入 -->
  </div>
</template>

<style>
#dify-chatbot-bubble-button {
  background-color: #40B4E5 !important;
  border-radius: 50% !important;
  width: 60px !important;
  height: 60px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  transition: all 0.3s ease !important;
}

#dify-chatbot-bubble-button:hover {
  transform: scale(1.1) !important;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2) !important;
}

#dify-chatbot-bubble-window {
  width: 24rem !important;
  height: 40rem !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}
</style> 