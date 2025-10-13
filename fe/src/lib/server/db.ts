// Simple mock DB for authentication
const users = [
  { id: '1', username: 'admin', password: 'admin123', isAdmin: true },
  { id: '2', username: 'user', password: 'user123', isAdmin: false }
];

export const db = {
  users,
  sessions: new Map()
};
