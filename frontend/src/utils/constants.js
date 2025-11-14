/**
 * Application constants.
 */

export const NHL_TEAMS = {
  TOR: { name: 'Toronto Maple Leafs', color: '#003E7E' },
  MTL: { name: 'Montreal Canadiens', color: '#AF1E2D' },
  BOS: { name: 'Boston Bruins', color: '#FFB81C' },
  NYR: { name: 'New York Rangers', color: '#0038A8' },
  // Add more teams as needed
}

export const POSITIONS = {
  C: 'Center',
  LW: 'Left Wing',
  RW: 'Right Wing',
  D: 'Defense',
  G: 'Goalie',
}

export const GAME_STATUSES = {
  SCHEDULED: 'scheduled',
  LIVE: 'live',
  FINAL: 'final',
  POSTPONED: 'postponed',
}

export const FANTASY_SCORING = {
  GOAL: 3,
  ASSIST: 2,
  PLUS_MINUS: 1,
  POWER_PLAY_GOAL: 1,
  SHORT_HANDED_GOAL: 2,
  GAME_WINNING_GOAL: 1,
  SHOT_ON_GOAL: 0.2,
}

export const GRID_CONFIG = {
  COLUMNS: 12,
  GUTTER: 24,
  BASE_WIDTH: 1440,
  BASE_HEIGHT: 900,
}
