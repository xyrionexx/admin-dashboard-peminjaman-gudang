import { redirect } from '@sveltejs/kit';
import type { RequestHandler, RequestEvent } from '@sveltejs/kit';
import * as auth from '$lib/server/auth.js';

export const GET: RequestHandler = async ({ cookies, locals }: RequestEvent) => {
  if (locals.session) {
    await auth.invalidateSession(locals.session.id); // Logout dari sesi yang aktif
  }
  
  auth.deleteSessionTokenCookie({ cookies } as any);
  
  // Redirect to login page
  throw redirect(303, '/login');
};
