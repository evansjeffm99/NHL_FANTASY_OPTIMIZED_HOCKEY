/**
 * Form validation utilities.
 */

/**
 * Validate email format.
 */
export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

/**
 * Validate password strength.
 */
export const validatePassword = (password) => {
  const errors = []

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long')
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number')
  }

  return {
    isValid: errors.length === 0,
    errors,
  }
}

/**
 * Validate required field.
 */
export const validateRequired = (value, fieldName = 'Field') => {
  if (!value || (typeof value === 'string' && value.trim() === '')) {
    return `${fieldName} is required`
  }
  return null
}

/**
 * Validate number range.
 */
export const validateRange = (value, min, max) => {
  const num = Number(value)
  if (isNaN(num)) {
    return 'Must be a valid number'
  }
  if (num < min || num > max) {
    return `Must be between ${min} and ${max}`
  }
  return null
}
