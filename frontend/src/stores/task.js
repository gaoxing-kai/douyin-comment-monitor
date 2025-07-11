import { defineStore } from 'pinia'
import axios from 'axios'

export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: [],
    currentTask: null
  }),
  
  actions: {
    async getTaskList(params) {
      try {
        const response = await axios.get('/api/tasks', { params })
        return response.data
      } catch (error) {
        console.error('获取任务列表失败:', error)
        throw error
      }
    },
    
    async getTaskDetail(id) {
      try {
        const response = await axios.get(`/api/tasks/${id}`)
        this.currentTask = response.data
        return response.data
      } catch (error) {
        console.error('获取任务详情失败:', error)
        throw error
      }
    },
    
    async createTask(data) {
      try {
        const response = await axios.post('/api/tasks', data)
        return response.data
      } catch (error) {
        console.error('创建任务失败:', error)
        throw error
      }
    },
    
    async updateTask(id, data) {
      try {
        const response = await axios.put(`/api/tasks/${id}`, data)
        return response.data
      } catch (error) {
        console.error('更新任务失败:', error)
        throw error
      }
    },
    
    async deleteTask(id) {
      try {
        await axios.delete(`/api/tasks/${id}`)
      } catch (error) {
        console.error('删除任务失败:', error)
        throw error
      }
    },
    
    async startTask(id) {
      try {
        const response = await axios.post(`/api/tasks/${id}/start`)
        return response.data
      } catch (error) {
        console.error('启动任务失败:', error)
        throw error
      }
    },
    
    async pauseTask(id) {
      try {
        const response = await axios.post(`/api/tasks/${id}/pause`)
        return response.data
      } catch (error) {
        console.error('暂停任务失败:', error)
        throw error
      }
    }
  }
})
    