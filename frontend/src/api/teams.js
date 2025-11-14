import api from './index'

export const teamsAPI = {
  getAll: () => api.get('/teams/'),
  getById: (id) => api.get(`/teams/${id}/`),
  getStandings: () => api.get('/teams/standings/')
}
