import { useState } from 'react'
import { Card, Button, Form, Input, Table } from 'antd'
import { optimizersAPI } from '../api/optimizers'

const ScheduleAnalyzer = () => {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const onAnalyze = async (values) => {
    setLoading(true)
    try {
      const response = await optimizersAPI.analyzeSchedule(values)
      setResults(response.data)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Schedule Analyzer</h1>
      <Card>
        <Form onFinish={onAnalyze} layout="inline">
          <Form.Item name="season" label="Season" rules={[{ required: true }]}>
            <Input placeholder="2024-2025" />
          </Form.Item>
          <Form.Item name="week" label="Week">
            <Input type="number" placeholder="1" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Analyze
            </Button>
          </Form.Item>
        </Form>

        {results && (
          <div style={{ marginTop: 24 }}>
            <h3>Analysis Results</h3>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </div>
        )}
      </Card>
    </div>
  )
}

export default ScheduleAnalyzer
