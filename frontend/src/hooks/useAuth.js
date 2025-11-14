/**
 * Custom hook for authentication operations.
 */
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../api/auth'
import { setUser, logout as logoutAction } from '../store/authSlice'

export const useAuth = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { user, isAuthenticated } = useSelector((state) => state.auth)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Load user on mount if token exists
    const token = localStorage.getItem('access_token')
    if (token && !user) {
      loadUser()
    }
  }, [])

  const loadUser = async () => {
    try {
      setLoading(true)
      const response = await authAPI.getCurrentUser()
      dispatch(setUser(response.data))
    } catch (err) {
      console.error('Failed to load user:', err)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials) => {
    try {
      setLoading(true)
      setError(null)
      const response = await authAPI.login(credentials)
      const { access, refresh, user } = response.data

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      dispatch(setUser(user))

      navigate('/')
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Login failed'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const register = async (data) => {
    try {
      setLoading(true)
      setError(null)
      await authAPI.register(data)
      navigate('/login')
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Registration failed'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      authAPI.logout(refreshToken).catch(console.error)
    }

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    dispatch(logoutAction())
    navigate('/login')
  }

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    loadUser,
  }
}
