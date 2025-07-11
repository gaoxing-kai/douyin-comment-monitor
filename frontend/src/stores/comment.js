import { defineStore } from 'pinia';
import { fetchComments, generateVoice } from '@/api/comment';

export const useCommentStore = defineStore('comment', {
  state: () => ({
    comments: [],
    loading: false,
    error: null
  }),

  actions: {
    /**
     * 获取评论列表
     * @param {string} taskId - 任务ID
     * @returns {Promise<Array>} - 评论列表
     */
    async fetchComments(taskId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetchComments(taskId);
        this.comments = response.data;
        return this.comments;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 生成语音
     * @param {string} commentId - 评论ID
     * @returns {Promise<string>} - 语音文件URL
     */
    async generateVoice(commentId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await generateVoice(commentId);
        return response.data.url;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 添加新评论
     * @param {Object} comment - 评论对象
     */
    addComment(comment) {
      this.comments.unshift(comment);
      // 限制评论数量，避免内存溢出
      if (this.comments.length > 100) {
        this.comments.pop();
      }
    },

    /**
     * 更新评论分析结果
     * @param {Array} analyzedComments - 分析后的评论列表
     */
    updateCommentAnalysis(analyzedComments) {
      analyzedComments.forEach(analyzedComment => {
        const index = this.comments.findIndex(c => c.id === analyzedComment.id);
        if (index !== -1) {
          this.comments[index] = { ...this.comments[index], ...analyzedComment };
        }
      });
    }
  }
});    