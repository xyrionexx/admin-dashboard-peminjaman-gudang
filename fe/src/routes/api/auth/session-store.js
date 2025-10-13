// Session storage in memory
const sessions = new Map();

export const SessionStore = {
  /**
   * Store a new session
   * @param {string} token - Session token
   * @param {Object} session - Session data
   */
  set(token, session) {
    sessions.set(token, session);
  },

  /**
   * Get a session by token
   * @param {string} token - Session token
   * @returns {Object|undefined} Session data or undefined if not found
   */
  get(token) {
    return sessions.get(token);
  },

  /**
   * Delete a session
   * @param {string} token - Session token
   * @returns {boolean} True if session was deleted, false if not found
   */
  delete(token) {
    return sessions.delete(token);
  },

  /**
   * Check if session exists
   * @param {string} token - Session token
   * @returns {boolean} True if session exists
   */
  has(token) {
    return sessions.has(token);
  }
};
