/**
 * Utility helper functions.
 */

/**
 * Format a date to a readable string.
 */
export const formatDate = (date, format = 'YYYY-MM-DD') => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')

  if (format === 'YYYY-MM-DD') {
    return `${year}-${month}-${day}`
  }
  if (format === 'MMM DD, YYYY') {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return `${monthNames[d.getMonth()]} ${day}, ${year}`
  }
  return date
}

/**
 * Calculate fantasy points for a player.
 */
export const calculateFantasyPoints = (stats) => {
  const { goals = 0, assists = 0, plus_minus = 0 } = stats
  return (goals * 3) + (assists * 2) + plus_minus
}

/**
 * Get team color by abbreviation.
 */
export const getTeamColor = (abbreviation) => {
  const colors = {
    TOR: '#003E7E',
    MTL: '#AF1E2D',
    BOS: '#FFB81C',
    // Add more teams
  }
  return colors[abbreviation] || '#000000'
}

/**
 * Format large numbers with commas.
 */
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Truncate text to specified length.
 */
export const truncate = (text, length = 50) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

/**
 * Debounce function for input handlers.
 */
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}
