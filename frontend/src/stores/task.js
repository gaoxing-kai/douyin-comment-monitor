import { defineStore } from 'pinia';
import { fetchTask, createTask, startTask, stopTask, deleteTask } from '@/api/task';

export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: [],
    currentTask: null,
    loading: false,
    error: null
  }),

  actions: {
    /**
     * 获取任务详情
     * @param {string} taskId - 任务ID
     * @returns {Promise<Object>} - 任务详情
     */
    async fetchTask(taskId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetchTask(taskId);
        this.currentTask = response.data;
        return this.currentTask;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 创建任务
     * @param {Object} data - 任务数据
     * @returns {Promise<Object>} - 创建的任务
     */
    async createTask(data) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await createTask(data);
        this.tasks.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 启动任务
     * @param {string} taskId - 任务ID
     * @returns {Promise<boolean>} - 操作结果
     */
    async startTask(taskId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await startTask(taskId);
        if (response.data.success && this.currentTask && this.currentTask.id === taskId) {
          this.currentTask.status = 'running';
        }
        return response.data.success;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 停止任务
     * @param {string} taskId - 任务ID
     * @returns {Promise<boolean>} - 操作结果
     */
    async stopTask(taskId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await stopTask(taskId);
        if (response.data.success && this.currentTask && this.currentTask.id === taskId) {
          this.currentTask.status = 'stopped';
        }
        return response.data.success;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * 删除任务
     * @param {string} taskId - 任务ID
     * @returns {Promise<boolean>} - 操作结果
     */
    async deleteTask(taskId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await deleteTask(taskId);
        if (response.data.success) {
          this.tasks = this.tasks.filter(task => task.id !== taskId);
          if (this.currentTask && this.currentTask.id === taskId) {
            this.currentTask = null;
          }
        }
        return response.data.success;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});    