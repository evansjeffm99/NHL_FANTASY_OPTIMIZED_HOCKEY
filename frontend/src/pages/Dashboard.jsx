import { Card, Row, Col, Statistic } from 'antd'

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic title="Active Teams" value={32} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Players Tracked" value={750} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Games Today" value={12} />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard
