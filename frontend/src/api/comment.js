import request from '@/utils/request';

/**
 * 获取评论列表
 * @param {string} taskId - 任务ID
 * @returns {Promise<Array>} - 评论列表
 */
export const fetchComments = (taskId) => {
  return request.get(`/api/tasks/${taskId}/comments`);
};

/**
 * 生成语音
 * @param {string} commentId - 评论ID
 * @returns {Promise<string>} - 语音文件URL
 */
export const generateVoice = (commentId) => {
  return request.post(`/api/comments/${commentId}/voice`);
};    