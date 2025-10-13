import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { SessionStore } from '../session-store.js';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const { token } = body;

    if (!token) {
      return json({ success: false, message: 'Token is required' }, { status: 400 });
    }

    // Hapus sesi
    SessionStore.delete(token);

    return json({
      success: true
    });
  } catch (error) {
    console.error('Invalidate session error:', error);
    return json({ success: false, message: 'Server error' }, { status: 500 });
  }
};
