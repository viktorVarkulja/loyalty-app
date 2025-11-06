/**
 * Decode JWT token without verification (client-side only)
 * @param {string} token - JWT token to decode
 * @returns {object|null} - Decoded payload or null if invalid
 */
export function decodeJWT(token) {
  if (!token) return null

  try {
    // JWT structure: header.payload.signature
    const parts = token.split('.')
    if (parts.length !== 3) return null

    // Decode the payload (second part)
    const payload = parts[1]
    // Replace URL-safe characters and add padding if needed
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const padding = '='.repeat((4 - (base64.length % 4)) % 4)
    const decoded = atob(base64 + padding)

    return JSON.parse(decoded)
  } catch (error) {
    console.error('Error decoding JWT:', error)
    return null
  }
}

/**
 * Check if a JWT token is expired
 * @param {string} token - JWT token to check
 * @returns {boolean} - True if expired, false if valid
 */
export function isTokenExpired(token) {
  const decoded = decodeJWT(token)
  if (!decoded || !decoded.exp) return true

  // exp is in seconds, Date.now() is in milliseconds
  const expirationTime = decoded.exp * 1000
  const currentTime = Date.now()

  return currentTime >= expirationTime
}

/**
 * Get the time remaining until token expiration in milliseconds
 * @param {string} token - JWT token
 * @returns {number} - Milliseconds until expiration, or 0 if expired/invalid
 */
export function getTokenTimeRemaining(token) {
  const decoded = decodeJWT(token)
  if (!decoded || !decoded.exp) return 0

  const expirationTime = decoded.exp * 1000
  const currentTime = Date.now()
  const timeRemaining = expirationTime - currentTime

  return timeRemaining > 0 ? timeRemaining : 0
}

/**
 * Get the expiration date of a JWT token
 * @param {string} token - JWT token
 * @returns {Date|null} - Expiration date or null if invalid
 */
export function getTokenExpirationDate(token) {
  const decoded = decodeJWT(token)
  if (!decoded || !decoded.exp) return null

  return new Date(decoded.exp * 1000)
}
