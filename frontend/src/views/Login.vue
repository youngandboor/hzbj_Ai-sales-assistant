<template>
  <div>
    <Navbar />
    <!-- 登录注册区域 -->
    <section class="login-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="card">
              <div class="card-body p-5">
                <!-- 切换按钮 -->
                <ul class="nav nav-pills nav-fill mb-4" role="tablist">
                  <li class="nav-item" role="presentation">
                    <button class="nav-link active text-dark" data-bs-toggle="pill" data-bs-target="#login-tab">登录</button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button class="nav-link text-dark" data-bs-toggle="pill" data-bs-target="#register-tab">注册</button>
                  </li>
                </ul>
                
                <!-- 表单内容 -->
                <div class="tab-content">
                  <!-- 登录表单 -->
                  <div class="tab-pane fade show active" id="login-tab">
                    <form @submit.prevent="handleLogin">
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-person"></i>
                          </span>
                          <input 
                            type="text" 
                            class="form-control border-start-0" 
                            v-model="loginForm.username"
                            placeholder="用户名/手机号/邮箱"
                            required
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-lock"></i>
                          </span>
                          <input 
                            type="password" 
                            class="form-control border-start-0" 
                            v-model="loginForm.password"
                            placeholder="密码"
                            required
                          >
                        </div>
                      </div>
                      <div class="mb-4 d-flex justify-content-between">
                        <div class="form-check">
                          <input type="checkbox" class="form-check-input" id="remember-me" v-model="loginForm.remember">
                          <label class="form-check-label" for="remember-me">记住我</label>
                        </div>
                        <a href="#" class="text-primary text-decoration-none">忘记密码？</a>
                      </div>
                      <div class="d-grid">
                        <button type="submit" class="btn btn-primary rounded-pill py-3" :disabled="loading">
                          {{ loading ? '登录中...' : '登录' }}
                        </button>
                      </div>
                    </form>
                  </div>
                  
                  <!-- 注册表单 -->
                  <div class="tab-pane fade" id="register-tab">
                    <form @submit.prevent="handleRegister">
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-person"></i>
                          </span>
                          <input 
                            type="text" 
                            class="form-control border-start-0" 
                            v-model="registerForm.username"
                            placeholder="用户名"
                            required
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-phone"></i>
                          </span>
                          <input 
                            type="tel" 
                            class="form-control border-start-0" 
                            v-model="registerForm.phone"
                            placeholder="手机号码"
                            required
                            pattern="[0-9]{11}"
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-envelope"></i>
                          </span>
                          <input 
                            type="email" 
                            class="form-control border-start-0" 
                            v-model="registerForm.email"
                            placeholder="电子邮箱"
                            required
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-lock"></i>
                          </span>
                          <input 
                            type="password" 
                            class="form-control border-start-0" 
                            v-model="registerForm.password"
                            placeholder="设置密码"
                            required
                            minlength="6"
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="input-group">
                          <span class="input-group-text bg-transparent border-end-0">
                            <i class="bi bi-lock-fill"></i>
                          </span>
                          <input 
                            type="password" 
                            class="form-control border-start-0" 
                            v-model="registerForm.confirmPassword"
                            placeholder="确认密码"
                            required
                            minlength="6"
                          >
                        </div>
                      </div>
                      <div class="mb-4">
                        <div class="form-check">
                          <input type="checkbox" class="form-check-input" id="agree-terms" v-model="registerForm.agreeTerms" required>
                          <label class="form-check-label" for="agree-terms">
                            我已阅读并同意 <a href="#" class="text-primary">服务条款</a> 和 <a href="#" class="text-primary">隐私政策</a>
                          </label>
                        </div>
                      </div>
                      <div class="d-grid">
                        <button type="submit" class="btn btn-primary rounded-pill py-3" :disabled="loading">
                          {{ loading ? '注册中...' : '注册' }}
                        </button>
                      </div>
                    </form>
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
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'Login',
  components: {
    Navbar,
    AIChatButton
  },
  data() {
    return {
      loading: false,
      error: null,
      loginForm: {
        username: '',
        password: '',
        remember: false
      },
      registerForm: {
        username: '',
        phone: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false
      }
    }
  },
  methods: {
    validateLoginForm() {
      if (!this.loginForm.username || !this.loginForm.password) {
        ElMessage.error('请填写所有必填字段')
        return false
      }
      return true
    },
    validateRegisterForm() {
      if (!this.registerForm.username || !this.registerForm.phone || 
          !this.registerForm.email || !this.registerForm.password || 
          !this.registerForm.confirmPassword) {
        ElMessage.error('请填写所有必填字段')
        return false
      }
      
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        ElMessage.error('两次输入的密码不一致')
        return false
      }
      
      if (!this.registerForm.agreeTerms) {
        ElMessage.error('请阅读并同意服务条款和隐私政策')
        return false
      }
      
      return true
    },
    async handleLogin() {
      try {
        if (!this.validateLoginForm()) return
        
        this.loading = true
        this.error = null
        
        const userStore = useUserStore()
        await userStore.login({
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        
        if (this.loginForm.remember) {
          localStorage.setItem('username', this.loginForm.username)
        }
        
        ElMessage.success('登录成功')
        this.$router.push('/')
      } catch (error) {
        if (error.response) {
          switch (error.response.status) {
            case 400:
              this.error = error.response.data.error || '用户名或密码错误'
              break
            case 401:
              this.error = '账号已被禁用'
              break
            case 404:
              this.error = '用户不存在'
              break
            case 500:
              this.error = '服务器错误，请稍后重试'
              break
            default:
              this.error = error.response.data?.error || '登录失败，请重试'
          }
        } else if (error.request) {
          this.error = '网络连接失败，请检查网络设置'
        } else {
          this.error = error.message || '登录失败，请重试'
        }
        ElMessage.error(this.error)
      } finally {
        this.loading = false
      }
    },
    async handleRegister() {
      try {
        if (!this.validateRegisterForm()) return
        
        this.loading = true
        this.error = null
        
        const userStore = useUserStore()
        await userStore.register({
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
          phone: this.registerForm.phone
        })
        
        ElMessage.success('注册成功，正在登录...')
        await this.handleLogin()
      } catch (error) {
        if (error.response) {
          switch (error.response.status) {
            case 400:
              if (error.response.data?.username) {
                this.error = '用户名已存在'
              } else if (error.response.data?.email) {
                this.error = '邮箱已被注册'
              } else if (error.response.data?.phone) {
                this.error = '手机号已被注册'
              } else {
                this.error = error.response.data?.message || '注册信息有误，请检查'
              }
              break
            case 500:
              this.error = '服务器错误，请稍后重试'
              break
            default:
              this.error = error.response.data?.message || '注册失败，请重试'
          }
        } else if (error.request) {
          this.error = '网络连接失败，请检查网络设置'
        } else {
          this.error = '注册失败，请重试'
        }
        ElMessage.error(this.error)
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    // 检查是否有保存的用户名
    const savedUsername = localStorage.getItem('username')
    if (savedUsername) {
      this.loginForm.username = savedUsername
      this.loginForm.remember = true
    }
  }
}
</script>

<style scoped>
.login-section {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 5rem 0;
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - 76px);
  width: 100%;
}

.container {
  width: 100%;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 1rem !important;
}

.row {
  margin: 0 -0.5rem;
  padding: 0;
  width: 100%;
}

/* 调整登录卡片宽度 */
.col-md-6 {
  flex: 0 0 100%;
  max-width: 100%;
  padding: 0 0.5rem;
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
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.form-control {
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(58, 134, 255, 0.25);
}

.input-group-text {
  border-radius: 50px 0 0 50px;
  border: 2px solid #e9ecef;
  border-right: none;
  padding: 0.75rem 1.5rem;
}

.input-group .form-control {
  border-radius: 0 50px 50px 0;
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

.nav-pills .nav-link {
  border-radius: 50px;
  padding: 0.75rem 2rem;
  color: #212529;
  transition: all 0.3s ease;
}

.nav-pills .nav-link.active {
  background: var(--gradient-primary);
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-section {
    padding: 3rem 0;
  }
  
  .card-body {
    padding: 2rem !important;
  }
  
  .nav-pills .nav-link {
    padding: 0.5rem 1rem;
  }
}
</style>
