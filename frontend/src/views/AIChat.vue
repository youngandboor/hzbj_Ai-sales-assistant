<template>
  <div>
    <Navbar />
    <!-- 智能客服聊天 -->
    <section id="ai-chat" class="page-section">
      <div class="container">
        <h2 class="section-title mb-4 mt-0">智能客服</h2>
        
        <div class="row">
          <!-- 左侧功能介绍 -->
          <div class="col-lg-7 mb-4 mb-lg-0">
            <div class="card h-100">
              <div class="card-body">
                <h4 class="card-title mb-4">智能客服功能介绍</h4>
                <div class="d-flex align-items-center mb-4">
                  <div class="feature-icon me-3">
                    <i class="bi bi-robot"></i>
                  </div>
                  <div>
                    <h5>24小时在线服务</h5>
                    <p class="mb-0">无论何时何地，我们的AI智能客服都能为您提供即时的房产咨询服务。</p>
                  </div>
                </div>
                <div class="d-flex align-items-center mb-4">
                  <div class="feature-icon me-3">
                    <i class="bi bi-graph-up"></i>
                  </div>
                  <div>
                    <h5>专业市场分析</h5>
                    <p class="mb-0">提供实时的房价走势、区域分析和投资建议，助您做出明智的购房决策。</p>
                  </div>
                </div>
                <div class="d-flex align-items-center mb-4">
                  <div class="feature-icon me-3">
                    <i class="bi bi-house-heart"></i>
                  </div>
                  <div>
                    <h5>个性化房源推荐</h5>
                    <p class="mb-0">根据您的需求和喜好，智能推荐最适合您的房源，节省您的时间和精力。</p>
                  </div>
                </div>
                <div class="d-flex align-items-center">
                  <div class="feature-icon me-3">
                    <i class="bi bi-calculator"></i>
                  </div>
                  <div>
                    <h5>贷款方案规划</h5>
                    <p class="mb-0">提供多种贷款方案比较和月供计算，帮您找到最优的购房融资方式。</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 右侧聊天框 -->
          <div class="col-lg-5">
            <div class="chat-interface-container">
              <iframe
                src="https://udify.app/chatbot/zRLo0mNPnh8PNH8q"
                style="width: 100%; height: 100%; min-height: 700px"
                frameborder="0"
                allow="microphone">
              </iframe>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 添加浮动聊天按钮 -->
    <AIChatButton />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import AIChatButton from '@/components/AIChatButton.vue'

export default {
  name: 'AIChat',
  components: {
    Navbar,
    AIChatButton
  }
}
</script>

<style scoped>
:root {
  --primary-color: #40b4e5;
  --secondary-color: #e0e5ec;
  --accent-color: #ff006e;
  --light-color: #f8f9fa;
  --dark-color: #212529;
  --gradient-primary: linear-gradient(135deg, #40b4e5, #e0e5ec);
  --gradient-secondary: linear-gradient(135deg, #ff006e, #fb5607);
}

.page-section {
  padding: 1rem 0;
  min-height: calc(100vh - 76px);
  width: 80vw;
}

.container {
  width: 100%;
  max-width: 1600px !important;
  margin: 0 auto !important;
  padding: 0 1rem !important;
}

.row {
  margin: 0 -0.5rem;
  padding: 0;
  width: 100%;
}

/* 让两列各占一半 */
.col-lg-6 {
  flex: 0 0 50%;
  max-width: 50%;
  padding: 0 0.5rem;
}

.section-title {
  position: relative;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 50px;
  height: 4px;
  background: var(--gradient-primary);
  border-radius: 2px;
}

.card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: none;
  height: 700px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  background: var(--gradient-primary);
  color: white;
  font-size: 1.5rem;
}

.chat-interface-container {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: none;
  height: 700px;
}

/* 悬浮客服按钮样式 */
#dify-chatbot-bubble-button {
  background-color: #40b4e5;
  border-radius: 50%;
}

#dify-chatbot-bubble-window {
  width: 24rem;
  height: 40rem;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .col-lg-6 {
    flex: 0 0 100%;
    max-width: 100%;
    padding: 0 0.5rem;
  }
  
  .feature-icon {
    width: 48px;
    height: 48px;
    font-size: 1.2rem;
  }
  
  .chat-interface-container {
    min-height: 500px;
  }
  
  #dify-chatbot-bubble-window {
    width: 20rem;
    height: 35rem;
  }
}

@media (max-width: 768px) {
  .page-section {
    padding: 1.5rem 0;
  }
  
  .section-title {
    margin-bottom: 1.5rem;
  }
  
  .chat-interface-container {
    min-height: 400px;
  }
  
  #dify-chatbot-bubble-window {
    width: 18rem;
    height: 30rem;
  }
  
  .feature-icon {
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 576px) {
  .chat-interface-container iframe {
    min-height: 350px;
  }
  
  #dify-chatbot-bubble-window {
    width: 16rem;
    height: 28rem;
  }
  
  .feature-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  h5 {
    font-size: 1rem;
  }
}
</style>
