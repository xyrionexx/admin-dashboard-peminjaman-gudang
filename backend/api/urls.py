from django.urls import path
import api.views as v 

urlpatterns = [
    # autentikasi
    path('register/', v.auth, {'authType': 'register'}, name='register'),
    path('login/', v.auth, {'authType': 'login'}, name='login'),
    
    # ambil data
    path('barang/', v.get_barang, name='get_barang'),
    path('siswa/', v.get_siswa, name='get_siswa'),
    path('guru/', v.get_guru, name='get_guru'),
    path('pegawai/', v.get_pegawai, name='get_pegawai'),
    path('peminjaman/', v.get_Peminjaman, name='get_peminjaman'),
    path('detail/peminjaman', v.get_detail_peminjaman, name='get_detail_peminjaman'),
    path('barang/summary/', v.get_summary_barang, name='get_summary_barang'),

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