import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { SessionStore } from '../session-store.js';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const { token, userId, expiresAt } = body;

    if (!token || !userId || !expiresAt) {
      return json({ success: false, message: 'Missing required fields' }, { status: 400 });
    }

    // Simpan sesi baru
    const session = {
      id: token,
      userId,
      expiresAt
    };

    SessionStore.set(token, session);

    return json({
      success: true,
      session: {
        id: token,
        expiresAt
      }
    });
  } catch (error) {
    console.error('Create session error:', error);
    return json({ success: false, message: 'Server error' }, { status: 500 });
  }
};
