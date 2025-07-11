import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  
  // 是否认证
  const isAuthenticated = computed(() => !!token.value)
  
  // 设置token
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  // 清除token
  const clearToken = () => {
    token.value = null
    localStorage.removeItem('token')
  }
  
  // 用户注册
  const register = async (username, email, password) => {
    try {
      const response = await axios.post('/auth/register', {
        username,
        email,
        password
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || '注册失败' }
    }
  }
  
  // 用户登录
  const login = async (username, password) => {
    try {
      const response = await axios.post('/auth/login', {
        username,
        password
      })
      
      setToken(response.data.token)
      user.value = response.data.user
      
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || '登录失败' }
    }
  }
  
  // 退出登录
  const logout = () => {
    clearToken()
    user.value = null
  }
  
  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await axios.get('/auth/user')
      user.value = response.data.user
      return response.data.user
    } catch (error) {
      clearToken()
      throw error
    }
  }
  
  // 激活卡密
  const activateCard = async (cardCode) => {
    try {
      const response = await axios.post('/auth/activate_card', {
        card_code: cardCode
      })
      
      return { success: true, message: response.data.message }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || '激活失败' }
    }
  }
  
  return {
    token,
    user,
    isAuthenticated,
    setToken,
    clearToken,
    register,
    login,
    logout,
    fetchUserInfo,
    activateCard
  }
})