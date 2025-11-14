import { Layout, Menu } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import { DashboardOutlined, CalendarOutlined } from '@ant-design/icons'

const { Sider } = Layout

const Sidebar = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
    { key: '/schedule-analyzer', icon: <CalendarOutlined />, label: 'Schedule Analyzer' }
  ]

  return (
    <Sider width={200}>
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        style={{ height: '100%', borderRight: 0 }}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
      />
    </Sider>
  )
}

export default Sidebar
