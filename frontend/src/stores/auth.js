import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async login(username, password) {
      try {
        // 模拟登录请求
        const response = await axios.post('/api/auth/login', {
          username,
          password
        })
        
        const { token, user } = response.data
        
        // 保存token到localStorage和state
        localStorage.setItem('token', token)
        this.token = token
        this.user = user
        
        // 设置axios默认请求头
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        return user
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },
    
    logout() {
      // 清除token和用户信息
      localStorage.removeItem('token')
      this.token = null
      this.user = null
      
      // 清除axios默认请求头
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
    