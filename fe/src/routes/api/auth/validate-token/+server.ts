import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { SessionStore } from '../session-store.js';

// Simulasi admin user untuk testing
const ADMIN_USERS = [
  {
    id: '1',
    username: 'admin',
    password: 'admin123',
    is_admin: true
  },
  {
    id: '2',
    username: 'user',
    password: 'user123',
    is_admin: false
  }
];

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const { token } = body;

    if (!token) {
      return json({ valid: false }, { status: 401 });
    }

    // Cek apakah token ada di sessions
    const session = SessionStore.get(token);
    if (!session) {
      return json({ valid: false }, { status: 401 });
    }

    // Cek apakah sesi sudah kedaluwarsa
    if (new Date(session.expiresAt) < new Date()) {
      SessionStore.delete(token);
      return json({ valid: false, message: 'Session expired' }, { status: 401 });
    }

    // Cari data user
    const user = ADMIN_USERS.find(u => u.id === session.userId);
    if (!user) {
      return json({ valid: false }, { status: 401 });
    }

    // Sesi valid, kembalikan data
    return json({
      valid: true,
      user: {
        id: user.id,
        username: user.username,
        is_admin: user.is_admin
      },
      expiresAt: session.expiresAt
    });
  } catch (error) {
    console.error('Validate token error:', error);
    return json({ valid: false, message: 'Server error' }, { status: 500 });
  }
};
