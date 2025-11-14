import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import Layout from './components/layout/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ScheduleAnalyzer from './pages/ScheduleAnalyzer'
import ProtectedRoute from './components/auth/ProtectedRoute'

function App() {
  return (
    <ConfigProvider theme={{ token: { colorPrimary: '#1890ff' } }}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/schedule-analyzer" element={<ScheduleAnalyzer />} />
          </Route>
        </Route>
      </Routes>
    </ConfigProvider>
  )
}

export default App
