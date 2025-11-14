import api from './index'

export const optimizersAPI = {
  analyzeSchedule: (data) => api.post('/optimizers/schedule-analysis/analyze/', data),
  runMonteCarlo: (data) => api.post('/optimizers/schedule-analysis/monte_carlo/', data)
}
