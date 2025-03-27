import axios from 'axios'

const baseURL = 'http://localhost:3000/api'

// 获取房源列表
export const getProperties = async (params) => {
  try {
    const response = await axios.get(`${baseURL}/properties`, { params })
    return response.data
  } catch (error) {
    console.error('获取房源列表失败:', error)
    throw error
  }
}

// 获取热门房源（随机获取8个房源）
export const getFeaturedProperties = async () => {
  try {
    const response = await axios.get(`${baseURL}/properties/featured`, {
      params: {
        limit: 8,
        random: true
      }
    })
    return response.data
  } catch (error) {
    console.error('获取热门房源失败:', error)
    throw error
  }
} 