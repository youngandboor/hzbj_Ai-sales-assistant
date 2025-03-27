<template>
  <div>
    <Navbar />
    <!-- 用户中心 -->
    <section id="user-center" class="page-section">
      <div class="container">
        <h2 class="section-title mb-4 mt-0">用户中心</h2>
        
        <div class="row">
          <div class="col-lg-4">
            <div class="card">
              <div class="user-profile">
                <div class="user-avatar">
                  <img :src="user?.avatar || 'https://pic1.zhimg.com/50/v2-42883f117e47e1b885960675941906d4_hd.jpg?source=1940ef5c'" alt="用户头像">
                </div>
                <h5>{{ user?.username || '未登录' }}</h5>
                <p class="text-muted">{{ user?.realName || '未设置' }}</p>
              </div>
              <div class="list-group list-group-flush">
                <a href="#profile" class="list-group-item list-group-item-action active" data-bs-toggle="pill">个人资料</a>
                <a href="#favorites" class="list-group-item list-group-item-action" data-bs-toggle="pill">我的收藏</a>
                <a href="#viewings" class="list-group-item list-group-item-action" data-bs-toggle="pill">看房预约</a>
                <a href="#messages" class="list-group-item list-group-item-action" data-bs-toggle="pill">消息中心</a>
                <a href="#settings" class="list-group-item list-group-item-action" data-bs-toggle="pill">账户设置</a>
              </div>
            </div>
          </div>
          
          <div class="col-lg-8">
            <div class="tab-content">
              <!-- 个人资料 -->
              <div class="tab-pane fade show active" id="profile">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title mb-4">个人资料</h4>
                    <form @submit.prevent="handleProfileUpdate">
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">用户名</label>
                        <div class="col-sm-9">
                          <input type="text" class="form-control" v-model="profileForm.username">
                        </div>
                      </div>
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">真实姓名</label>
                        <div class="col-sm-9">
                          <input type="text" class="form-control" v-model="profileForm.realName">
                        </div>
                      </div>
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">手机号码</label>
                        <div class="col-sm-9">
                          <input type="tel" class="form-control" v-model="profileForm.phone">
                        </div>
                      </div>
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">电子邮箱</label>
                        <div class="col-sm-9">
                          <input type="email" class="form-control" v-model="profileForm.email">
                        </div>
                      </div>
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">购房意向</label>
                        <div class="col-sm-9">
                          <select class="form-select" v-model="profileForm.intention">
                            <option value="刚需">刚需</option>
                            <option value="改善">改善</option>
                            <option value="投资">投资</option>
                          </select>
                        </div>
                      </div>
                      <div class="row mb-3">
                        <label class="col-sm-3 col-form-label">意向区域</label>
                        <div class="col-sm-9">
                          <select class="form-select" v-model="profileForm.area">
                            <option value="不限">不限</option>
                            <option value="滨江区">滨江区</option>
                            <option value="拱墅区">拱墅区</option>
                            <option value="上城区">上城区</option>
                            <option value="西湖区">西湖区</option>
                            <option value="钱塘区">钱塘区</option>
                            
                          </select>
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-sm-9 offset-sm-3">
                          <button type="submit" class="btn btn-primary rounded-pill">保存修改</button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
              
              <!-- 我的收藏 -->
              <div class="tab-pane fade" id="favorites">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title mb-4">我的收藏</h4>
                    <div class="row g-4">
                      <div v-for="property in favoriteProperties" :key="property.id" class="col-md-6">
                        <div class="card">
                          <div class="position-relative">
                            <img :src="property.image" class="card-img-top" :alt="property.title">
                            <span class="badge-vr position-absolute top-0 end-0 m-3">{{ property.badge }}</span>
                          </div>
                          <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                              <h5 class="card-title mb-0">{{ property.title }}</h5>
                              <span class="price-tag">{{ property.price }}</span>
                            </div>
                            <p class="card-text text-muted">{{ property.location }}</p>
                            <div class="property-features mb-3">
                              <span v-for="feature in property.features" :key="feature">{{ feature }}</span>
                            </div>
                            <div class="d-flex gap-2">
                              <a :href="property.detailUrl" class="btn btn-outline-primary rounded-pill flex-grow-1">查看详情</a>
                              <button class="btn btn-outline-danger rounded-circle" @click="removeFavorite(property.id)">
                                <i class="bi bi-trash"></i>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 看房预约 -->
              <div class="tab-pane fade" id="viewings">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title mb-4">看房预约</h4>
                    <div class="table-responsive">
                      <table class="table table-hover">
                        <thead>
                          <tr>
                            <th>房源信息</th>
                            <th>预约时间</th>
                            <th>状态</th>
                            <th>操作</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="viewing in viewings" :key="viewing.id">
                            <td>{{ viewing.property }}</td>
                            <td>{{ viewing.time }}</td>
                            <td>
                              <span :class="['badge', viewing.status === '已确认' ? 'bg-success' : 'bg-warning text-dark']">
                                {{ viewing.status }}
                              </span>
                            </td>
                            <td>
                              <button class="btn btn-sm btn-outline-primary rounded-pill me-2">查看详情</button>
                              <button class="btn btn-sm btn-outline-danger rounded-pill" @click="cancelViewing(viewing.id)">
                                取消预约
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 消息中心 -->
              <div class="tab-pane fade" id="messages">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title mb-4">消息中心</h4>
                    <ul class="list-group">
                      <li v-for="message in messages" :key="message.id" class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <h6 class="mb-1">{{ message.title }}</h6>
                          <p class="text-muted mb-0 small">{{ message.content }}</p>
                          <small class="text-muted">{{ message.time }}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-primary rounded-pill">查看详情</button>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <!-- 账户设置 -->
              <div class="tab-pane fade" id="settings">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title mb-4">账户设置</h4>
                    <form @submit.prevent="handlePasswordUpdate">
                      <div class="mb-3">
                        <label class="form-label">修改密码</label>
                        <input type="password" class="form-control" v-model="passwordForm.currentPassword" placeholder="当前密码">
                      </div>
                      <div class="mb-3">
                        <input type="password" class="form-control" v-model="passwordForm.newPassword" placeholder="新密码">
                      </div>
                      <div class="mb-3">
                        <input type="password" class="form-control" v-model="passwordForm.confirmPassword" placeholder="确认新密码">
                      </div>
                      <button type="submit" class="btn btn-primary rounded-pill">更新密码</button>
                    </form>
                    
                    <hr class="my-4">
                    
                    <h5 class="mb-3">隐私设置</h5>
                    <div class="form-check form-switch mb-3">
                      <input class="form-check-input" type="checkbox" id="privacy1" v-model="privacySettings.recommendations">
                      <label class="form-check-label" for="privacy1">允许系统根据我的浏览记录推荐房源</label>
                    </div>
                    <div class="form-check form-switch mb-3">
                      <input class="form-check-input" type="checkbox" id="privacy2" v-model="privacySettings.priceAlerts">
                      <label class="form-check-label" for="privacy2">接收价格变动提醒</label>
                    </div>
                    <div class="form-check form-switch mb-3">
                      <input class="form-check-input" type="checkbox" id="privacy3" v-model="privacySettings.marketing">
                      <label class="form-check-label" for="privacy3">接收营销信息</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary rounded-pill" @click="savePrivacySettings">保存设置</button>
                  </div>
                </div>
              </div>
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
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserCenter',
  components: {
    Navbar,
    AIChatButton
  },
  setup() {
    const userStore = useUserStore()
    const { user } = storeToRefs(userStore)
    return { userStore, user }
  },
  data() {
    return {
      profileForm: {
        username: '',
        realName: '',
        phone: '',
        email: '',
        intention: '改善',
        area: '朝阳区'
      },
      favoriteProperties: [
        {
          id: 1,
          title: '现代简约三居室',
          price: '¥380万',
          location: '朝阳区 · 三里屯',
          image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
          badge: 'VR看房',
          features: ['120㎡', '3室2厅', '南北通透'],
          detailUrl: '#property-detail'
        },
        {
          id: 2,
          title: '豪华江景两居室',
          price: '¥450万',
          location: '浦东新区 · 陆家嘴',
          image: 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
          badge: 'AI推荐',
          features: ['89㎡', '2室2厅', '江景房'],
          detailUrl: '#property-detail'
        }
      ],
      viewings: [
        {
          id: 1,
          property: '现代简约三居室 - 朝阳区三里屯',
          time: '2023-06-15 上午',
          status: '已确认'
        },
        {
          id: 2,
          property: '豪华江景两居室 - 浦东新区陆家嘴',
          time: '2023-06-18 下午',
          status: '待确认'
        }
      ],
      messages: [
        {
          id: 1,
          title: '新房源推荐',
          content: '根据您的浏览记录，为您推荐5套新上架房源。',
          time: '2023-06-10 11:45'
        },
        {
          id: 2,
          title: '看房预约确认',
          content: '您预约的三里屯北小区看房已确认，时间为2023-06-15上午。',
          time: '2023-06-12 09:30'
        },
        {
          id: 3,
          title: '价格变动提醒',
          content: '您关注的工体西路小区房源价格已下调5万元。',
          time: '2023-06-08 16:20'
        }
      ],
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      privacySettings: {
        recommendations: true,
        priceAlerts: true,
        marketing: false
      }
    }
  },
  methods: {
    async handleProfileUpdate() {
      try {
        // TODO: 调用API更新个人资料
        ElMessage.success('个人资料更新成功')
      } catch (error) {
        ElMessage.error('更新失败，请重试')
      }
    },
    async handlePasswordUpdate() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        ElMessage.error('两次输入的密码不一致')
        return
      }
      try {
        // TODO: 调用API更新密码
        ElMessage.success('密码更新成功')
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      } catch (error) {
        ElMessage.error('密码更新失败，请重试')
      }
    },
    async savePrivacySettings() {
      try {
        // TODO: 调用API保存隐私设置
        ElMessage.success('隐私设置保存成功')
      } catch (error) {
        ElMessage.error('保存失败，请重试')
      }
    },
    async removeFavorite(propertyId) {
      try {
        // TODO: 调用API移除收藏
        this.favoriteProperties = this.favoriteProperties.filter(p => p.id !== propertyId)
        ElMessage.success('已取消收藏')
      } catch (error) {
        ElMessage.error('操作失败，请重试')
      }
    },
    async cancelViewing(viewingId) {
      try {
        // TODO: 调用API取消预约
        this.viewings = this.viewings.filter(v => v.id !== viewingId)
        ElMessage.success('预约已取消')
      } catch (error) {
        ElMessage.error('取消失败，请重试')
      }
    }
  },
  created() {
    // 获取用户资料
    if (this.user) {
      this.profileForm = {
        username: this.user.username || '',
        realName: this.user.realName || '',
        phone: this.user.phone || '',
        email: this.user.email || '',
        intention: this.user.intention || '改善',
        area: this.user.area || '朝阳区'
      }
    }
  }
}
</script>

<style scoped>
.page-section {
  padding: 1rem 0;
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - 76px);
  width: 80vw;
}

.container {
  max-width: 2000px !important;
  margin: 0 auto;
  padding: 0 2rem;
}

.row {
  margin: 0 -0.5rem;
  padding: 0;
  width: 100%;
  display: flex;
  align-items: stretch;
}

.col-lg-4, .col-lg-8 {
  padding: 0 0.5rem;
  display: flex;
  flex-direction: column;
}

.card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: none;
  background: white;
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.section-title {
  position: relative;
  margin-bottom: 2rem;
  margin-top: 0;
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

.property-features span {
  background-color: rgba(58, 134, 255, 0.1);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.price-tag {
  background: var(--gradient-primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 700;
  display: inline-block;
}

.user-profile {
  text-align: center;
  padding: 2rem;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 1rem;
  border: 4px solid white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.nav-pills .nav-link.active {
  background: var(--gradient-primary);
}

.form-control, .form-select {
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(58, 134, 255, 0.25);
}

.btn-primary {
  background: var(--gradient-primary);
  border: none;
  box-shadow: 0 4px 15px rgba(58, 134, 255, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(58, 134, 255, 0.4);
}

.btn-outline-primary {
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .page-section {
    padding: 3rem 0;
  }
  
  .card-body {
    padding: 2rem !important;
  }
  
  .user-profile {
    padding: 1rem;
  }
  
  .user-avatar {
    width: 80px;
    height: 80px;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
}

.sticky-top {
  position: relative;
  top: 0;
}
</style>
