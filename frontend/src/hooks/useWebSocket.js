/**
 * Custom hook for WebSocket connections.
 */
import { useState, useEffect, useCallback, useRef } from 'react'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const useWebSocket = (channel) => {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const [error, setError] = useState(null)
  const wsRef = useRef(null)

  const connect = useCallback(() => {
    try {
      const token = localStorage.getItem('access_token')
      const url = `${WS_URL}/ws/${channel}/`

      wsRef.current = new WebSocket(url)

      // Send auth token after connection
      wsRef.current.onopen = () => {
        setIsConnected(true)
        setError(null)
        console.log(`WebSocket connected: ${channel}`)

        // Send authentication
        if (token) {
          wsRef.current.send(JSON.stringify({
            type: 'auth',
            token: token
          }))
        }
      }

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          setLastMessage(data)
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err)
        }
      }

      wsRef.current.onerror = (err) => {
        console.error('WebSocket error:', err)
        setError('WebSocket connection error')
      }

      wsRef.current.onclose = () => {
        setIsConnected(false)
        console.log(`WebSocket disconnected: ${channel}`)
      }
    } catch (err) {
      console.error('Failed to connect WebSocket:', err)
      setError(err.message)
    }
  }, [channel])

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])

  const send = useCallback((data) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])

  return {
    isConnected,
    lastMessage,
    error,
    send,
    connect,
    disconnect,
  }
}
