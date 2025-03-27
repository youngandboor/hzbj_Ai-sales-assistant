<template>
  <div>
    <!-- 英雄区域：顶部带背景的主宣传区 -->
    <div class="hero-section" style="background: linear-gradient(135deg, #40b4e5, #e0e5ec) !important; width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%); margin-top: -76px; padding-top: calc(7rem + 76px); padding-bottom: 7rem;">
      <div class="container">
        <div class="row align-items-center hero-content">
          <!-- 左侧文字区域 -->
          <div class="col-lg-6 animate__animated animate__fadeInLeft">
            <h1 class="display-4 fw-bold mb-4">AI助您找到理想家</h1>
            <p class="lead mb-4">利用人工智能技术，为您提供个性化的房源推荐和智能客服服务，让买房变得简单高效。</p>
            <div class="d-flex gap-3">
              <!-- 主按钮：跳转到房源列表页 -->
              <button class="btn btn-light rounded-pill px-4 py-3" @click="handleRouteChange('/house-list')">开始找房</button>
              <!-- 次要按钮 -->
              <button class="btn btn-outline-light rounded-pill px-4 py-3" @click="scrollToFeatures">了解更多</button>
            </div>
          </div>
          <!-- 右侧图片区域：仅在大屏幕显示 -->
          <div class="col-lg-6 d-none d-lg-block animate__animated animate__fadeInRight">
            <img src="/home/devbox/project/src/assets/front-temp/展示-拷贝.jpg" class="img-fluid rounded-4 animate-float" alt="现代公寓">
          </div>
        </div>
      </div>
    </div>

        <!-- 搜索区域：供用户筛选房源 -->
        <div class="container mt-n5">
      <div class="search-bar">
        <div class="row g-3">
          <!-- 区域/小区名称搜索框 -->
          <div class="col-md-3">
            <input type="text" class="form-control" v-model="searchQuery" placeholder="输入区域、小区名称">
          </div>
          <!-- 价格区间下拉选择框 -->
          <div class="col-md-2">
            <select class="form-select" v-model="priceRange">
              <option value="">价格区间</option>
              <option value="100-200">100-200万</option>
              <option value="200-300">200-300万</option>
              <option value="300-500">300-500万</option>
              <option value="500+">500万以上</option>
            </select>
          </div>
          <!-- 户型下拉选择框 -->
          <div class="col-md-2">
            <select class="form-select" v-model="houseType">
              <option value="">户型</option>
              <option value="1">一室</option>
              <option value="2">二室</option>
              <option value="3">三室</option>
              <option value="4">四室及以上</option>
            </select>
          </div>
          <!-- 面积下拉选择框 -->
          <div class="col-md-2">
            <select class="form-select" v-model="area">
              <option value="">面积</option>
              <option value="0-50">50㎡以下</option>
              <option value="50-90">50-90㎡</option>
              <option value="90-120">90-120㎡</option>
              <option value="120+">120㎡以上</option>
            </select>
          </div>
          <!-- 搜索按钮 -->
          <div class="col-md-3">
            <button class="btn btn-primary w-100 py-2" @click="handleSearch">
              <i class="bi bi-search me-2"></i>智能搜索
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 特色服务区域：展示三个主要服务特点 -->
    <div class="container mt-5">
      <h2 class="section-title text-center">我们的特色服务</h2>
      <div class="row g-4">
        <!-- AI智能客服特色卡片 -->
        <div class="col-md-4">
          <div class="card h-100 text-center p-4" @click="handleRouteChange('/ai-chat')" style="cursor: pointer;">
            <div class="feature-icon mx-auto">
              <i class="bi bi-robot"></i>
            </div>
            <div class="card-body">
              <h4 class="card-title">AI智能客服</h4>
              <p class="card-text">24小时在线智能客服，解答您的所有疑问，提供专业的购房建议。</p>
            </div>
          </div>
        </div>
        <!-- 个性化推荐特色卡片 -->
        <div class="col-md-4">
          <div class="card h-100 text-center p-4">
            <div class="feature-icon mx-auto">
              <i class="bi bi-house-heart"></i>
            </div>
            <div class="card-body">
              <h4 class="card-title">个性化推荐</h4>
              <p class="card-text">基于您的喜好和需求，智能算法为您推荐最适合的房源。</p>
            </div>
          </div>
        </div>
        <!-- VR看房特色卡片 -->
        <div class="col-md-4">
          <div class="card h-100 text-center p-4">
            <div class="feature-icon mx-auto">
              <i class="bi bi-camera-video"></i>
            </div>
            <div class="card-body">
              <h4 class="card-title">VR看房</h4>
              <p class="card-text">足不出户，通过VR技术全方位查看房源，节省您的时间和精力。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 精选房源区域：展示热门推荐的房源 -->
    <div class="container mt-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="section-title mb-0">精选房源</h2>
        <!-- 查看更多按钮：跳转到房源列表页 -->
        <button class="btn btn-outline-primary rounded-pill" @click="handleRouteChange('/house-list')">查看更多</button>
      </div>
      
      <!-- 加载状态显示 -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      
      <!-- 房源列表：使用v-for循环生成 -->
      <div v-else class="row g-4">
        <div v-for="house in processedHouses" :key="house.id" class="col-md-4">
          <!-- 房源卡片 -->
          <div class="card">
            <!-- 房源图片区域 -->
            <div class="position-relative">
              <img 
                :src="house.image" 
                class="card-img-top" 
                :alt="house.title"
                @error="handleImageError"
                loading="lazy"
                :data-house-id="house.id"
                :data-original-src="house.image"
              >
              <!-- VR看房或AI推荐标签 -->
              <span :class="['badge position-absolute top-0 end-0 m-3', house.badgeClass]">{{ house.badge }}</span>
            </div>
            <!-- 房源信息区域 -->
            <div class="card-body">
              <!-- 房源标题和价格 -->
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="card-title mb-0">{{ house.title }}</h5>
                <span class="price-tag">¥{{ house.price }}万</span>
              </div>
              <!-- 房源位置 -->
              <p class="card-text text-muted">{{ house.location }}</p>
              <!-- 房源特点标签 -->
              <div class="property-features mb-3">
                <span v-for="feature in house.features" :key="feature">{{ feature }}</span>
              </div>
              <!-- 查看详情按钮 -->
              <div class="d-grid">
                <a :href="house.url" target="_blank" class="btn btn-outline-primary rounded-pill">查看详情</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 悬浮客服按钮 -->
    <AIChatButton />
  </div>
</template>

<script>
import AIChatButton from '@/components/AIChatButton.vue'
import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  timeout: 30000
});

// 定义API基础URL和图片代理URL
const API_BASE = 'http://aisales-back-release-shicms.ns-jj1vgrim.svc.cluster.local:8000';
const PROXY_IMAGE_URL = `${API_BASE}/properties/proxy-image/`;

export default {
  name: 'Home',
  components: {
    AIChatButton
  },
  // 组件数据
  data() {
    return {
      // 搜索表单数据
      searchQuery: '',     // 搜索关键词
      priceRange: '',      // 价格区间
      houseType: '',       // 户型
      area: '',            // 面积
      // 精选房源数据
      featuredHouses: [],
      // 添加加载状态
      isLoading: false,
      // 添加错误状态
      error: null,
      // 添加图片加载状态
      imageLoadStatus: {}
    }
  },
  // 添加计算属性
  computed: {
    // 处理图片URL的计算属性
    processedHouses() {
      return this.featuredHouses.map(house => ({
        ...house,
        image: this.getProxyImageUrl(house.image)
      }));
    }
  },
  // 组件方法
  methods: {
    // 添加获取代理图片URL的方法
    getProxyImageUrl(originalUrl) {
      if (!originalUrl) {
        return '/src/assets/front-temp/展示-拷贝.jpg';
      }
      return `/api/properties/proxy-image/?url=${encodeURIComponent(originalUrl)}`;
    },
    // 处理搜索按钮点击事件：跳转到房源列表页并传递搜索参数
    handleSearch() {
      window.scrollTo(0, 0); // 重置滚动位置
      this.$router.push({
        path: '/house-list',
        query: {
          q: this.searchQuery,
          price: this.priceRange,
          type: this.houseType,
          area: this.area
        }
      })
    },
    // 滚动到特色服务区域
    scrollToFeatures() {
      const featuresSection = document.querySelector('.section-title');
      if (featuresSection) {
        const offset = 100; // 添加一个偏移量，确保标题不会被导航栏遮挡
        const elementPosition = featuresSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    },
    // 处理图片加载错误
    handleImageError(e) {
      const img = e.target;
      const houseId = img.getAttribute('data-house-id');
      
      // 如果已经尝试过加载，直接使用默认图片
      if (this.imageLoadStatus[houseId]?.retried) {
        img.src = '/src/assets/front-temp/展示-拷贝.jpg';
        return;
      }
      
      // 标记为已尝试
      this.imageLoadStatus[houseId] = {
        retried: true
      };
      
      // 尝试使用代理URL
      const originalSrc = img.getAttribute('data-original-src');
      if (originalSrc) {
        img.src = this.getProxyImageUrl(originalSrc);
      } else {
        img.src = '/src/assets/front-temp/展示-拷贝.jpg';
      }
    },
    // 处理路由跳转
    handleRouteChange(path) {
      window.scrollTo(0, 0); // 重置滚动位置
      this.$router.push(path);
    },
    // 获取精选房源数据
    async fetchFeaturedHouses() {
      console.log('开始获取房源数据...');
      this.isLoading = true;
      this.error = null;
      
      try {
        const url = '/api/properties/properties';
        console.log('发送请求到:', url);
        
        const response = await axios.get(url, {
          params: {
            page: 1,
            page_size: 100,
            ordering: '-created_at'
          }
        });
        
        console.log('收到响应:', response.data);
        
        if (!response.data?.results) {
          console.error('API返回数据格式不正确:', response.data);
          throw new Error('API返回数据格式不正确');
        }
        
        const houses = response.data.results;
        console.log('获取到的房源数量:', houses.length);
        
        // 随机选择3个房源
        const selectedHouses = [];
        const usedIndexes = new Set();
        
        while (selectedHouses.length < 3 && selectedHouses.length < houses.length) {
          const randomIndex = Math.floor(Math.random() * houses.length);
          if (!usedIndexes.has(randomIndex)) {
            usedIndexes.add(randomIndex);
            const house = houses[randomIndex];
            console.log('处理房源数据:', house);
            
            // 获取房源详情
            try {
              const detailResponse = await axios.get(`/api/properties/${house.id}/`);
              const property = detailResponse.data;
              console.log('房源详情:', property);
              
              // 规范化房源数据结构
              selectedHouses.push({
                id: house.id,
                title: house.title || '未命名房源',
                price: house.price ? house.price.toFixed(1) : '暂无价格',
                location: house.features || '暂无位置信息',
                image: property.images?.[0]?.image || '/src/assets/front-temp/展示-拷贝.jpg',
                features: [
                  house.areas ? house.areas : '暂无面积',
                  house.rooms ? house.rooms : '暂无户型',
                  house.direction || '暂无朝向'
                ].filter(feature => feature !== '暂无'),
                badge: Math.random() > 0.5 ? 'VR看房' : 'AI推荐',
                badgeClass: Math.random() > 0.5 ? 'badge-vr' : 'badge-ai',
                url: house.url  // 添加房源URL
              });
            } catch (detailError) {
              console.error('获取房源详情失败:', detailError);
              // 如果获取详情失败，使用列表数据中的图片
              selectedHouses.push({
                id: house.id,
                title: house.title || '未命名房源',
                price: house.price ? house.price.toFixed(1) : '暂无价格',
                location: house.features || '暂无位置信息',
                image: house.images?.[0]?.image || '/src/assets/front-temp/展示-拷贝.jpg',
                features: [
                  house.areas ? house.areas : '暂无面积',
                  house.rooms ? house.rooms : '暂无户型',
                  house.direction || '暂无朝向'
                ].filter(feature => feature !== '暂无'),
                badge: Math.random() > 0.5 ? 'VR看房' : 'AI推荐',
                badgeClass: Math.random() > 0.5 ? 'badge-vr' : 'badge-ai',
                url: house.url  // 添加房源URL
              });
            }
          }
        }
        
        console.log('最终选择的房源:', selectedHouses);
        this.featuredHouses = selectedHouses;
      } catch (error) {
        console.error('获取精选房源失败:', error);
        
        // 根据错误类型显示不同的错误信息
        if (error.code === 'ECONNABORTED') {
          this.error = '请求超时，请检查网络连接';
        } else if (error.response) {
          console.error('错误响应:', error.response.data);
          this.error = error.response.data.message || '服务器响应错误';
        } else if (error.request) {
          console.error('未收到响应:', error.request);
          this.error = '无法连接到服务器，请检查网络连接';
        } else {
          console.error('请求配置错误:', error.message);
          this.error = '请求配置错误';
        }
        
        // 使用默认数据作为后备
        this.featuredHouses = [
          {
            id: 1,
            title: '现代简约三居室',
            price: 380,
            location: '朝阳区 · 三里屯',
            image: '/src/assets/front-temp/展示-拷贝.jpg',
            features: ['120㎡', '3室', '南北通透'],
            badge: 'VR看房',
            badgeClass: 'badge-vr',
            url: 'https://hz.lianjia.com/ershoufang/'
          },
          {
            id: 2,
            title: '豪华江景两居室',
            price: 450,
            location: '浦东新区 · 陆家嘴',
            image: '/src/assets/front-temp/展示-拷贝.jpg',
            features: ['89㎡', '2室', '江景房'],
            badge: 'AI推荐',
            badgeClass: 'badge-ai',
            url: 'https://hz.lianjia.com/ershoufang/'
          },
          {
            id: 3,
            title: '花园洋房四居室',
            price: 680,
            location: '海淀区 · 中关村',
            image: '/src/assets/front-temp/展示-拷贝.jpg',
            features: ['180㎡', '4室', '花园'],
            badge: 'VR看房',
            badgeClass: 'badge-vr',
            url: 'https://hz.lianjia.com/ershoufang/'
          }
        ];
      } finally {
        console.log('设置加载状态为 false');
        this.isLoading = false;
      }
    }
  },
  // 组件挂载时获取数据
  mounted() {
    this.fetchFeaturedHouses();
  },
  // 添加路由跳转前的处理
  beforeRouteLeave(to, from, next) {
    // 重置滚动位置
    window.scrollTo(0, 0);
    next();
  }
}
</script>

<style scoped>
/* 英雄区域样式 - 高优先级确保渐变背景显示 */
.hero-section {
  /* 渐变背景色 - 使用内联方式和!important确保显示 */
  background: linear-gradient(135deg, #40b4e5, #e0e5ec) !important;
  color: white !important;
  padding: 5rem 0;
  position: relative;
  overflow: hidden;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  margin-top: -76px;
  padding-top: calc(7rem + 76px);
  padding-bottom: 7rem;
  box-sizing: border-box;
}

/* 英雄区域背景图片叠加效果 */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 背景图片 */
  background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1073&q=80');
  background-size: cover;
  background-position: center;
  /* 透明度控制 */
  opacity: 0.2;
  z-index: 0;
}

/* 英雄区域内容层，确保在背景上方 */
.hero-content {
  position: relative;
  z-index: 1;
  width: 100%;
}

/* 搜索栏样式 */
.search-bar {
  border-radius: 16px;
  padding: 1.5rem;
  /* 阴影效果 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  background: white;
  margin-top: 2rem;
  width: 100%;
}

/* 确保每个容器部分宽度正确 */
.container {
  width: 100%;
  max-width: 1200px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

/* VR看房徽章样式 */
.badge-vr {
  background: linear-gradient(135deg, #40b4e5, #e0e5ec) !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 16px;
  font-weight: bold;
}

/* AI推荐徽章样式 */
.badge-ai {
  background: linear-gradient(135deg, #ff006e, #fb5607) !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 16px;
  font-weight: bold;
}

/* 卡片样式 */
.card {
  width: 100%;
  transition: all 0.3s ease;
}

/* 卡片悬浮效果 */
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

/* 确保图片自适应容器 */
.card-img-top {
  width: 100%;
  object-fit: cover;
  height: 200px;
}

/* 悬浮客服按钮样式 */
#dify-chatbot-bubble-button {
  background-color: #40b4e5 !important;
}
#dify-chatbot-bubble-window {
  width: 24rem !important;
  height: 40rem !important;
}
</style> 