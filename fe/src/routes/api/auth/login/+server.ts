import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
  try {
    console.log('=== MOCK API LOGIN DISABLED ===');
    const body = await request.json();
    const { username } = body;
    console.log('Mock login attempt rejected for:', username);

    // MOCK API DINONAKTIFKAN UNTUK MEMAKSA PENGGUNAAN SUPERUSER DJANGO
    // Kembalikan respons error untuk semua login attempt
    return json({
      success: false,
      message: 'Fitur mock login dinonaktifkan. Gunakan akun superuser Django asli.'
    }, { status: 403 });

  } catch (error) {
    console.error('Login API error:', error);
    return json({
      success: false, 
      message: 'Server error. Gunakan akun superuser Django asli.'
    }, { status: 500 });
  }
};
