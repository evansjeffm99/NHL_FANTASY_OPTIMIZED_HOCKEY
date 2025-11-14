/**
 * WebSocket message handlers.
 */

/**
 * Handle NHL data updates.
 */
export const handleNHLUpdate = (data) => {
  console.log('Received NHL update:', data)

  // Dispatch to appropriate handlers based on message type
  switch (data.type) {
    case 'game_update':
      handleGameUpdate(data.payload)
      break
    case 'standings_update':
      handleStandingsUpdate(data.payload)
      break
    case 'player_stats_update':
      handlePlayerStatsUpdate(data.payload)
      break
    default:
      console.log('Unknown message type:', data.type)
  }
}

/**
 * Handle game updates.
 */
const handleGameUpdate = (payload) => {
  console.log('Game update:', payload)
  // Update Redux store or trigger refetch
}

/**
 * Handle standings updates.
 */
const handleStandingsUpdate = (payload) => {
  console.log('Standings update:', payload)
  // Update Redux store or trigger refetch
}

/**
 * Handle player stats updates.
 */
const handlePlayerStatsUpdate = (payload) => {
  console.log('Player stats update:', payload)
  // Update Redux store or trigger refetch
}

export default {
  handleNHLUpdate,
  handleGameUpdate,
  handleStandingsUpdate,
  handlePlayerStatsUpdate,
}
