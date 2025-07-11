import request from '@/utils/request';

/**
 * 获取任务详情
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} - 任务详情
 */
export const fetchTask = (taskId) => {
  return request.get(`/api/tasks/${taskId}`);
};

/**
 * 创建任务
 * @param {Object} data - 任务数据
 * @returns {Promise<Object>} - 创建的任务
 */
export const createTask = (data) => {
  return request.post('/api/tasks', data);
};

/**
 * 启动任务
 * @param {string} taskId - 任务ID
 * @returns {Promise<boolean>} - 操作结果
 */
export const startTask = (taskId) => {
  return request.post(`/api/tasks/${taskId}/start`);
};

/**
 * 停止任务
 * @param {string} taskId - 任务ID
 * @returns {Promise<boolean>} - 操作结果
 */
export const stopTask = (taskId) => {
  return request.post(`/api/tasks/${taskId}/stop`);
};

/**
 * 删除任务
 * @param {string} taskId - 任务ID
 * @returns {Promise<boolean>} - 操作结果
 */
export const deleteTask = (taskId) => {
  return request.delete(`/api/tasks/${taskId}`);
};    