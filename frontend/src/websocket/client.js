/**
 * WebSocket client for real-time NHL data updates.
 */

class WebSocketClient {
  constructor() {
    this.ws = null
    this.subscribers = new Map()
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
  }

  connect(url, token) {
    try {
      this.ws = new WebSocket(url)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0

        // Send authentication
        if (token) {
          this.send({ type: 'auth', token })
        }
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.notifySubscribers(data)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.attemptReconnect(url, token)
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.subscribers.clear()
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  subscribe(channel, callback) {
    if (!this.subscribers.has(channel)) {
      this.subscribers.set(channel, [])
    }
    this.subscribers.get(channel).push(callback)

    // Return unsubscribe function
    return () => {
      const callbacks = this.subscribers.get(channel)
      if (callbacks) {
        const index = callbacks.indexOf(callback)
        if (index > -1) {
          callbacks.splice(index, 1)
        }
      }
    }
  }

  notifySubscribers(data) {
    const channel = data.channel || 'default'
    const callbacks = this.subscribers.get(channel)
    if (callbacks) {
      callbacks.forEach((callback) => callback(data))
    }
  }

  attemptReconnect(url, token) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)

      console.log(`Attempting to reconnect in ${delay}ms...`)
      setTimeout(() => {
        this.connect(url, token)
      }, delay)
    } else {
      console.error('Max reconnection attempts reached')
    }
  }
}

export default new WebSocketClient()
