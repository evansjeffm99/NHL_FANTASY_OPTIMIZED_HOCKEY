import { Layout, Button } from 'antd'
import { useNavigate } from 'react-router-dom'
import { LogoutOutlined } from '@ant-design/icons'

const { Header: AntHeader } = Layout

const Header = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <AntHeader style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>
        NHL Fantasy Optimizer
      </div>
      <Button icon={<LogoutOutlined />} onClick={handleLogout}>
        Logout
      </Button>
    </AntHeader>
  )
}

export default Header
