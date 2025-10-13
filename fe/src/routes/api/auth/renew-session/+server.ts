import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { SessionStore } from '../session-store.js';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const { token, expiresAt } = body;

    if (!token || !expiresAt) {
      return json({ success: false, message: 'Missing required fields' }, { status: 400 });
    }

    // Cek apakah sesi ada
    const session = SessionStore.get(token);
    if (!session) {
      return json({ success: false, message: 'Session not found' }, { status: 404 });
    }

    // Update tanggal kedaluwarsa sesi
    session.expiresAt = expiresAt;
    SessionStore.set(token, session);

    return json({
      success: true
    });
  } catch (error) {
    console.error('Renew session error:', error);
    return json({ success: false, message: 'Server error' }, { status: 500 });
  }
};
