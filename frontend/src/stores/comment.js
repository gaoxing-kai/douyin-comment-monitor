import { defineStore } from 'pinia'
import axios from 'axios'

export const useCommentStore = defineStore('comment', {
  state: () => ({
    comments: [],
    total: 0
  }),
  
  actions: {
    async getCommentsByTask(params) {
      try {
        const response = await axios.get('/api/comments', { params })
        this.comments = response.data.items
        this.total = response.data.total
        return response.data
      } catch (error) {
        console.error('获取评论列表失败:', error)
        throw error
      }
    }
  }
})
    