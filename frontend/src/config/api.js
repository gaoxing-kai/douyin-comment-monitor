// API基础配置
export default {
  baseURL: import.meta.env.VITE_API_BASE_URL,
  
  // API端点
  endpoints: {
    auth: {
      login: '/api/auth/login',
      logout: '/api/auth/logout',
      userinfo: '/api/auth/userinfo'
    },
    comment: {
      list: '/api/comments',
      analyze: '/api/comments/analyze',
      download: '/api/comments/download'
    },
    task: {
      list: '/api/tasks',
      create: '/api/tasks',
      detail: '/api/tasks/{id}',
      update: '/api/tasks/{id}',
      delete: '/api/tasks/{id}'
    },
    voice: {
      generate: '/api/voice/generate',
      list: '/api/voice'
    }
  }
}    