import { redirect } from '@sveltejs/kit';
import type { ServerLoad } from '@sveltejs/kit';

export const load: ServerLoad = async ({ locals, url }: { locals: App.Locals, url: URL }) => {
  // Jika user belum login dan mencoba mengakses halaman selain login
  if (!locals.user && url.pathname !== '/login') {
    throw redirect(303, '/login');
  }
  
  // Jika user sudah login tapi bukan admin, tolak akses ke dashboard
  if (locals.user && !locals.user.isAdmin && url.pathname !== '/login') {
    throw redirect(303, '/login');
  }
  
  // Jika user sudah login dan mencoba mengakses halaman login
  if (locals.user && url.pathname === '/login') {
    throw redirect(303, '/');
  }
  
  return {
    user: locals.user
  };
};
