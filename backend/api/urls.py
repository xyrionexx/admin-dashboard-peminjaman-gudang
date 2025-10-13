from django.urls import path
import api.views as v 
import api.handle_auth as auth_handlers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

# Endpoint untuk mendapatkan CSRF token
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


urlpatterns = [
    # CSRF token endpoint
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    
    # autentikasi
    path('register/', v.auth, {'authType': 'register'}, name='register'),
    path('login/', v.auth, {'authType': 'login'}, name='login'),
    path('logout/', v.logout, name='logout'),
    path('api/admin/login/', v.admin_login_view),
    
    # Session management untuk aplikasi frontend
    path('api/auth/validate-token/', auth_handlers.validate_token, name='validate_token'),
    path('api/auth/create-session/', auth_handlers.create_session, name='create_session'),
    path('api/auth/renew-session/', auth_handlers.renew_session, name='renew_session'),
    path('api/auth/invalidate-session/', auth_handlers.invalidate_session, name='invalidate_session'),

    # ambil data
    path('csrf/', v.csrf),
    path('user/', v.getUserSession, name='getUserSession'),
    path('barang/', v.get_barang, name='get_barang'),
    path('guru/', v.get_guru, name='get_guru'),
    path('pegawai/', v.get_pegawai, name='get_pegawai'),
    path('peminjaman/', v.get_Peminjaman, name='get_peminjaman'),
    path('detail/peminjaman', v.get_detail_peminjaman, name='get_detail_peminjaman'),
    path('barang/summary/', v.get_summary_barang, name='get_summary_barang'),
    path('detail/peminjaman/list', v.detail_peminjaman_list, name='detail_peminjaman_list'),

    # Delete
    path('barang/delete/<str:id>/', v.delete_barang, name='delete_barang'),
    path('siswa/delete/<str:id>/', v.delete_siswa, name='delete_siswa'),
    path('guru/delete/<str:id>/', v.delete_guru, name='delete_guru'),
    path('pegawai/delete/<str:id>/', v.delete_pegawai, name='delete_pegawai'),

    # Tambah
    path('barang/tambah_barang/', v.tambah_barang, name='tambah_barang'),
    path('user/tambah_siswa', v.tambah_siswa, name='tambah_siswa'),
    path('user/tambah_guru', v.tambah_guru, name='tambah_guru'),
    path('user/tambah_pegawai', v.tambah_pegawai, name='tambah_pegawai'),

    # Detail
    path('barang/<str:id>/', v.detail_barang, name='detail_barang'),
    path('peminjaman/<str:id>/', v.det_detail_peminjaman, name='det_detail_peminjaman'),
    path('detailpeminjaman/<str:id>/', v.det_detail_detail_peminjaman, name='det_detail_detail_peminjaman'),
    path('update/<str:kategori>/<str:id>/', v.detail_user, name='detail_user'),
    path("detail/update-status/", v.update_status, name="update_status"),
    path("detail/detail-update-status/", v.scan_pengembalian, name="update_status"),
]