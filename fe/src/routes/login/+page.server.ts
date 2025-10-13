import { fail, redirect } from '@sveltejs/kit';
import type { Actions, RequestEvent } from '@sveltejs/kit';
import type { ServerLoad } from '@sveltejs/kit';
import * as auth from '$lib/server/auth.js';

// Jika user sudah login dan mengakses halaman login,
// redirect ke halaman utama
export const load: ServerLoad = async ({ locals }: { locals: App.Locals }) => {
  if (locals.user) {
    throw redirect(302, '/');
  }
  
  return {};
};

export const actions: Actions = {
  login: async ({ request, cookies, fetch }: RequestEvent) => {
    const formData = await request.formData();
    const username = formData.get('username')?.toString();
    const password = formData.get('password')?.toString();

    if (!username || !password) {
      return fail(400, {
        message: 'Username dan password harus diisi'
      });
    }

    try {
      console.log('====== LOGIN ATTEMPT ======');
      console.log('Username:', username);
      
      // Langkah 1: Dapatkan CSRF token terlebih dahulu
      console.log('Getting CSRF token first...');
      const csrfResponse = await fetch('http://localhost:8000/api/get-csrf-token/', {
        method: 'GET',
        credentials: 'include',  // Penting untuk menerima cookie
        mode: 'cors',
      });
      
      // Ekstrak CSRF token dari cookies
      let csrfToken = '';
      const cookiesHeader = cookies.getAll();
      console.log('All cookies:', cookiesHeader);
      
      // Cari cookie csrftoken
      for (const cookie of cookiesHeader) {
        if (cookie.name.toLowerCase() === 'csrftoken') {
          csrfToken = cookie.value;
          console.log('Found CSRF token in cookies:', csrfToken);
          break;
        }
      }
      
      // Verifikasi CSRF token berhasil diset
      if (!csrfResponse.ok) {
        console.error('Failed to get CSRF token:', csrfResponse.status);
      } else {
        console.log('CSRF token response:', await csrfResponse.json());
      }
      
      // Langkah 2: Gunakan Django untuk autentikasi
      console.log('Using Django backend authentication');
      
      // URL ke backend Django admin login (perhatikan ada 'api' dua kali karena URL patterns di Django)
      const djangoUrl = 'http://localhost:8000/api/api/admin/login/';
      console.log('Connecting to Django backend at:', djangoUrl);
      
      // Kirim request ke Django API
      const response = await fetch(djangoUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', // Membantu Django mengenali request AJAX
          'Accept': 'application/json',
          'X-CSRFToken': csrfToken, // Tambahkan CSRF token ke header
        },
        body: JSON.stringify({ username, password }),
        redirect: 'follow', // Ikuti redirect secara otomatis
        credentials: 'include', // Termasuk cookies untuk autentikasi
        mode: 'cors', // Aktifkan CORS
      });

      if (!response.ok) {
        console.error('Django login failed with status:', response.status);
        const errorText = await response.text();
        console.error('Error response body from Django:', errorText);
        
        // Parse error message if possible
        let errorMessage = 'Username atau password salah';
        try {
          const errorData = JSON.parse(errorText);
          if (errorData.error) {
            errorMessage = errorData.error;
          }
        } catch (e) {
          // Ignore parsing errors
        }
        
        // Login gagal - TIDAK menggunakan mock API lagi
        // Hanya superuser Django yang bisa login
        return fail(401, {
          message: errorMessage
        });
      }

      const data = await response.json();
      console.log('Login response from Django:', data);
      
      // Format dari Django admin_login_view berbeda dari Mock API
      // Django mengembalikan data langsung (id, username, is_staff, is_superuser)
      // tanpa nesting dalam user object atau success flag
      
      // Jika ada error dalam response
      if (data.error) {
        return fail(403, {
          message: data.error
        });
      }
      
      // Verifikasi bahwa user adalah admin/superuser
      if (!data.is_staff && !data.is_superuser) {
        return fail(403, {
          message: 'Akses ditolak. Hanya admin yang diizinkan masuk.'
        });
      }

      // Create a session for the user
      const token = auth.generateSessionToken();
      
      const user: auth.User = {
        id: data.id.toString(),
        username: data.username,
        isAdmin: data.is_staff || data.is_superuser
      };
      
      console.log('Created user object from Django response:', user);
      
      const session = await auth.createSession(token, user);
      
      // Set the session cookie
      auth.setSessionTokenCookie({ cookies } as any, token, session.expiresAt);
      
      return { success: true };
    } catch (error) {
      console.error('Login error details:', error);
      // Tampilkan detail error jika tersedia
      const errorMessage = error instanceof Error ? 
        `Terjadi kesalahan saat login: ${error.message}` : 
        'Terjadi kesalahan saat login';
      
      return fail(500, {
        message: errorMessage
      });
    }
  }
};
