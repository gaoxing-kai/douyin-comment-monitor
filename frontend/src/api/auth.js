import request from '@/utils/request'

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise<Object>} - 包含token的响应
 */
export const login = (username, password) => {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

/**
 * 用户登出
 * @returns {Promise<void>}
 */
export const logout = () => {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

/**
 * 获取用户信息
 * @returns {Promise<Object>} - 用户信息
 */
export const getUserInfo = () => {
  return request({
    url: '/api/auth/userinfo',
    method: 'get'
  })
}    