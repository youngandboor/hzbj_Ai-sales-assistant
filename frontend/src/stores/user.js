import { defineStore } from 'pinia'
import api from '../api'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),

  getters: {
    userProfile: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/auth/login/', credentials)
        if (response.data.message === '登录成功') {
          this.isAuthenticated = true
          await this.fetchUserProfile()
          return response
        }
        throw new Error(response.data.error || '登录失败')
      } catch (error) {
        this.isAuthenticated = false
        throw error
      }
    },

    async register(userData) {
      try {
        const response = await api.post('/auth/register/', userData)
        return response
      } catch (error) {
        throw error
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout/')
        this.isAuthenticated = false
        this.user = null
      } catch (error) {
        throw error
      }
    },

    async fetchUserProfile() {
      try {
        const response = await api.get('/auth/profile/')
        this.user = response.data
        return response.data
      } catch (error) {
        this.user = null
        throw error
      }
    },

    async updateProfile(profileData) {
      try {
        const response = await api.put('/auth/profile/', profileData)
        this.user = response.data
        return response.data
      } catch (error) {
        throw error
      }
    },

    async verifyPhone(code) {
      try {
        const response = await api.post('/auth/verify-phone/', { code })
        return response
      } catch (error) {
        throw error
      }
    }
  }
}) 