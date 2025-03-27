<template>
  <div>
    <Navbar />
    
    <!-- 房源列表页 -->
    <section id="listings" class="page-section bg-light pt-3">
      <div class="container">
        <h2 class="section-title mb-5">房源列表</h2>
        
        <div class="row">
          <!-- 筛选区域 -->
          <div class="col-lg-3">
            <div class="filter-card sticky-top" style="top: 100px;">
              <h5 class="mb-4">筛选条件</h5>
              
              <!-- 搜索框 -->
              <div class="mb-4">
                <label class="form-label">搜索</label>
                <div class="input-group">
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="searchQuery"
                    placeholder="输入关键词搜索"
                  >
                  <button 
                    class="btn btn-primary" 
                    @click="applyFilters"
                  >
                    搜索
                  </button>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label">价格区间</label>
                <div class="range-slider mb-2">
                  <div class="range-selected" :style="{ left: priceRange.left + '%', right: priceRange.right + '%' }"></div>
                </div>
                <div class="range-input">
                  <input type="range" v-model="priceRange.min" min="0" max="1000" step="10">
                  <input type="range" v-model="priceRange.max" min="0" max="1000" step="10">
                </div>
                <div class="d-flex justify-content-between">
                  <span>{{ priceRange.min }}万</span>
                  <span>{{ priceRange.max }}万</span>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label">户型</label>
                <div class="d-flex flex-wrap gap-2">
                  <div v-for="type in houseTypes" :key="type.value" class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="selectedTypes" :value="type.value">
                    <label class="form-check-label">{{ type.label }}</label>
                  </div>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label">面积</label>
                <div class="range-slider mb-2">
                  <div class="range-selected" :style="{ left: areaRange.left + '%', right: areaRange.right + '%' }"></div>
                </div>
                <div class="range-input">
                  <input type="range" v-model="areaRange.min" min="0" max="300" step="5">
                  <input type="range" v-model="areaRange.max" min="0" max="300" step="5">
                </div>
                <div class="d-flex justify-content-between">
                  <span>{{ areaRange.min }}㎡</span>
                  <span>{{ areaRange.max }}㎡</span>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label">特色</label>
                <div class="d-flex flex-wrap gap-2">
                  <div v-for="feature in features" :key="feature.value" class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="selectedFeatures" :value="feature.value">
                    <label class="form-check-label">{{ feature.label }}</label>
                  </div>
                </div>
              </div>
              
              <div class="d-grid">
                <button class="btn btn-primary rounded-pill" @click="applyFilters">应用筛选</button>
              </div>
            </div>
          </div>
          
          <!-- 房源列表 -->
          <div class="col-lg-9">
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
            
            <!-- 房源列表 -->
            <div v-else>
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                  <span class="text-muted">共找到 <strong>{{ totalHouses }}</strong> 套房源</span>
                </div>
                <div class="d-flex align-items-center">
                  <span class="me-2">排序：</span>
                  <select class="form-select form-select-sm" v-model="sortBy" style="width: auto;">
                    <option value="default">默认排序</option>
                    <option value="price-asc">价格从低到高</option>
                    <option value="price-desc">价格从高到低</option>
                    <option value="area-desc">面积从大到小</option>
                    <option value="newest">最新发布</option>
                  </select>
                </div>
              </div>
              
              <div class="row g-4">
                <div v-for="house in houses" :key="house.id" class="col-md-6 col-lg-4">
                  <div class="card">
                    <div class="position-relative">
                      <img 
                        :src="house.image" 
                        class="card-img-top" 
                        :alt="house.title"
                        @error="handleImageError"
                        :data-original-src="house.image"
                      >
                      <span :class="['badge position-absolute top-0 end-0 m-3', house.badgeClass]">{{ house.badge }}</span>
                    </div>
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="card-title mb-0">{{ house.title }}</h5>
                        <span class="price-tag">¥{{ house.price }}万</span>
                      </div>
                      <p class="card-text text-muted">{{ house.location }}</p>
                      <div class="property-features mb-3">
                        <span v-for="feature in house.features" :key="feature">{{ feature }}</span>
                      </div>
                      <div class="d-grid">
                        <a :href="house.url" target="_blank" class="btn btn-outline-primary rounded-pill">查看详情</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 分页 -->
            <nav class="mt-5">
              <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
                </li>
                <!-- 第一页 -->
                <li class="page-item" :class="{ active: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(1)">1</a>
                </li>
                <!-- 省略号 -->
                <li v-if="currentPage > 4" class="page-item disabled">
                  <span class="page-link">...</span>
                </li>
                <!-- 当前页附近的页码 -->
                <template v-for="page in displayedPages" :key="page">
                  <li class="page-item" :class="{ active: currentPage === page }">
                    <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                  </li>
                </template>
                <!-- 省略号 -->
                <li v-if="currentPage < totalPages - 3" class="page-item disabled">
                  <span class="page-link">...</span>
                </li>
                <!-- 最后一页 -->
                <li v-if="totalPages > 1" class="page-item" :class="{ active: currentPage === totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(totalPages)">{{ totalPages }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </section>

    <!-- 悬浮客服按钮 -->
    <AIChatButton />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import AIChatButton from '@/components/AIChatButton.vue'
import axios from 'axios'

export default {
  name: 'HouseList',
  components: {
    Navbar,
    AIChatButton
  },
  data() {
    return {
      searchQuery: '',  // 搜索关键词
      priceRange: {
        min: 100,
        max: 1000,
        left: 10,
        right: 0
      },
      areaRange: {
        min: 0,
        max: 300,
        left: 0,
        right: 0
      },
      houseTypes: [
        { label: '一室', value: '1室' },
        { label: '二室', value: '2室' },
        { label: '三室', value: '3室' },
        { label: '四室及以上', value: '4室' }
      ],
      features: [
        { label: '南北通透', value: 'north-south' },
        { label: '电梯房', value: 'elevator' },
        { label: '近地铁', value: 'subway' },
        { label: '学区房', value: 'school' },
        { label: '精装修', value: 'renovated' }
      ],
      selectedTypes: [],
      selectedFeatures: [],
      sortBy: 'default',
      currentPage: 1,
      pageSize: 18,
      totalPages: 20,
      totalHouses: 0,
      houses: [],
      imageLoadStatus: {},
      isLoading: false,
      error: null,
      API_BASE: '/api'
    }
  },
  methods: {
    async fetchHouses(page = 1) {
      console.log('开始获取房源数据...');
      this.isLoading = true;
      this.error = null;
      
      try {
        // 构建查询参数
        const params = {
          page: page,
          page_size: this.pageSize,
          ordering: '-created_at'
        };

        // 添加搜索关键词
        if (this.searchQuery) {
          params.search = this.searchQuery;
        }

        // 添加价格范围
        if (this.priceRange.min > 0) {
          params.min_price = this.priceRange.min;
        }
        if (this.priceRange.max < 1000) {
          params.max_price = this.priceRange.max;
        }

        // 添加户型筛选
        if (this.selectedTypes.length > 0) {
          params.house_type = this.selectedTypes.join(',');
        }

        // 添加面积范围
        if (this.areaRange.min > 0) {
          params.min_area = this.areaRange.min;
        }
        if (this.areaRange.max < 300) {
          params.max_area = this.areaRange.max;
        }

        // 添加特色筛选
        if (this.selectedFeatures.length > 0) {
          params.features = this.selectedFeatures.join(',');
        }

        // 添加排序
        switch (this.sortBy) {
          case 'price-asc':
            params.ordering = 'price';
            break;
          case 'price-desc':
            params.ordering = '-price';
            break;
          case 'area-desc':
            params.ordering = '-area';
            break;
          case 'newest':
            params.ordering = '-created_at';
            break;
        }

        console.log('请求参数:', params);
        const response = await axios.get(`${this.API_BASE}/properties/properties/`, { params });
        console.log('收到响应:', response.data);
        
        if (!response.data?.results) {
          console.error('API返回数据格式不正确:', response.data);
          throw new Error('API返回数据格式不正确');
        }
        
        const houses = response.data.results;
        console.log('获取到的房源数量:', houses.length);
        
        // 更新总页数和总房源数
        this.totalHouses = response.data.count || 360;
        this.totalPages = Math.ceil(this.totalHouses / this.pageSize);
        
        this.houses = await Promise.all(houses.map(async (house) => {
          try {
            const detailResponse = await axios.get(`${this.API_BASE}/properties/properties/${house.id}/`);
            const property = detailResponse.data;
            console.log('房源详情:', property);
            
            return {
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
              url: house.url
            };
          } catch (detailError) {
            console.error('获取房源详情失败:', detailError);
            return {
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
              url: house.url
            };
          }
        }));
      } catch (error) {
        console.error('获取房源列表失败:', error);
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
      } finally {
        this.isLoading = false;
      }
    },
    handleImageError(event) {
      const img = event.target;
      const originalSrc = img.getAttribute('data-original-src');
      if (originalSrc && !this.imageLoadStatus[originalSrc]) {
        this.imageLoadStatus[originalSrc] = true;
        img.src = this.getProxyImageUrl(originalSrc);
      } else {
        img.src = '/src/assets/front-temp/展示-拷贝.jpg';
      }
    },
    getProxyImageUrl(originalUrl) {
      return `${this.API_BASE}/properties/proxy-image/?url=${encodeURIComponent(originalUrl)}`;
    },
    applyFilters() {
      this.currentPage = 1;  // 重置到第一页
      this.fetchHouses(1);
    },
    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        await this.fetchHouses(page);
        // 滚动到页面顶部
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  },
  computed: {
    displayedPages() {
      const pages = [];
      const current = this.currentPage;
      const total = this.totalPages;
      
      // 如果当前页是第1页或最后一页，不添加当前页（因为已经在模板中显示）
      if (current !== 1 && current !== total) {
        pages.push(current);
      }
      
      // 显示当前页前后的页码，但要排除第1页和最后一页（因为已经在模板中显示）
      if (current > 1 && current - 1 !== 1) pages.push(current - 1);
      if (current < total && current + 1 !== total) pages.push(current + 1);
      
      // 如果当前页靠近开始，显示更多后面的页码
      if (current <= 3) {
        for (let i = current + 2; i <= Math.min(current + 3, total - 1); i++) {
          if (i !== total) {  // 排除最后一页
            pages.push(i);
          }
        }
      }
      // 如果当前页靠近结束，显示更多前面的页码
      else if (current >= total - 2) {
        for (let i = current - 2; i >= Math.max(current - 3, 2); i--) {
          if (i !== 1) {  // 排除第一页
            pages.push(i);
          }
        }
      }
      // 如果当前页在中间，显示前后各一个页码
      else {
        if (current - 1 !== 1) pages.push(current - 1);  // 排除第一页
        if (current + 1 !== total) pages.push(current + 1);  // 排除最后一页
      }
      
      // 排序并去重
      return [...new Set(pages)].sort((a, b) => a - b);
    }
  },
  mounted() {
    this.fetchHouses(1);
  }
}
</script>

<style scoped>
.filter-card {
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  background: white;
  margin-bottom: 2rem;
}

.range-slider {
  height: 5px;
  position: relative;
  background-color: #e1e9f8;
  border-radius: 2px;
}

.range-selected {
  height: 100%;
  position: absolute;
  border-radius: 2px;
  background: var(--gradient-primary);
}

.range-input {
  position: relative;
}

.range-input input {
  position: absolute;
  width: 100%;
  height: 5px;
  top: -5px;
  background: none;
  pointer-events: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.range-input input::-webkit-slider-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  border: 3px solid white;
  background: var(--primary-color);
  pointer-events: auto;
  -webkit-appearance: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.range-input input::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  border: 3px solid white;
  background: var(--primary-color);
  pointer-events: auto;
  -moz-appearance: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.badge-vr {
  background: var(--gradient-primary);
  color: white;
}

.badge-ai {
  background: var(--gradient-secondary);
  color: white;
}
</style> 