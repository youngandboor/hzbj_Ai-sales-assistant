import axios from 'axios'
import { ElMessage } from 'element-plus'

// 获取 CSRF token
const getCsrfToken = async () => {
  try {
    const response = await axios.get('/api/auth/csrf/', {
      withCredentials: true,
      headers: {
        'Accept': 'application/json'
      }
    })
    return response.data.csrfToken
  } catch (error) {
    console.error('获取 CSRF token 失败:', error)
    throw error
  }
}

const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  async config => {
    // 如果是 POST、PUT、DELETE 请求，需要添加 CSRF token
    if (['post', 'put', 'delete'].includes(config.method?.toLowerCase())) {
      try {
        const csrfToken = await getCsrfToken()
        config.headers['X-CSRFToken'] = csrfToken
      } catch (error) {
        console.error('获取 CSRF token 失败:', error)
      }
    }
    return config
  },
  error => {
    ElMessage.error('请求发送失败，请重试')
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    let errorMessage = '请求失败，请重试'
    
    if (error.response) {
      switch (error.response.status) {
        case 400:
          errorMessage = error.response.data.error || '请求参数错误'
          break
        case 401:
          errorMessage = '请先登录'
          break
        case 403:
          errorMessage = '没有权限访问'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 500:
          errorMessage = '服务器错误，请稍后重试'
          break
        default:
          errorMessage = error.response.data?.error || '请求失败，请重试'
      }
    } else if (error.request) {
      errorMessage = '网络连接失败，请检查网络设置'
    }
    
    ElMessage.error(errorMessage)
    return Promise.reject(error)
  }
)

export default api 