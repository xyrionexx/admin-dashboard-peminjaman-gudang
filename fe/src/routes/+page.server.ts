import type { ServerLoad } from '@sveltejs/kit';

export const load: ServerLoad = async ({ locals }: { locals: App.Locals }) => {
  // User data sudah disediakan oleh hooks.server.ts
  return {
    user: locals.user
  };
};
