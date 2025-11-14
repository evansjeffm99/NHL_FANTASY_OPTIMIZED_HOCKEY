import api from './index'

export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (data) => api.post('/auth/register/', data),
  getCurrentUser: () => api.get('/auth/me/'),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh: refreshToken })
}
