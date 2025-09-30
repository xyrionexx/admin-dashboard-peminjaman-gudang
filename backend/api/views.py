# barang/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Barang,Siswa,Guru,Peminjaman,DetailPeminjaman ,Pegawai
from django.db.models import Sum, Count
from .serializers import BarangSerializer , SiswaSerializer , GuruSerializer , PeminjamanSerializer , DetailPeminjamanSerializer ,PegawaiSerializer

@api_view(['GET'])
def get_barang(request):
    barang = Barang.objects.all()
    serializer = BarangSerializer(barang, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_siswa(request):
    siswa = Siswa.objects.all()
    serializer = SiswaSerializer(siswa, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_guru(request):
    guru = Guru.objects.all()
    serializer = GuruSerializer(guru, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_pegawai(request):
    pegawai = Pegawai.objects.all()
    serializer = PegawaiSerializer(pegawai, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_Peminjaman(request):
    peminjaman = Peminjaman.objects.all()
    serializer = PeminjamanSerializer(peminjaman, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_detail_peminjaman(request):
    detailPeminjaman = DetailPeminjaman.objects.all()
    serializer = DetailPeminjamanSerializer(detailPeminjaman, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_barang(request , id):
    try:
        barang = Barang.objects.get(id_barang=id)
        barang.delete()
        return JsonResponse({'message': 'Barang berhasil dihapus'}, status=200)
    except Barang.DoesNotExist:
        return JsonResponse({'error': 'Barang tidak ditemukan'}, status=404)
    
@api_view(['DELETE'])
def delete_siswa(request, id):
   if request.method == "DELETE":
        siswa = get_object_or_404(Siswa, nis=id)  
        siswa.delete()
        return JsonResponse({"message": "Siswa berhasil dihapus"}, status=200)
   return JsonResponse({"error": "Method not allowed"}, status=405)
    
@csrf_exempt   
def delete_guru(request, id):
    if request.method == "DELETE":
        try:
            guru = get_object_or_404(Guru, pk=id)
            guru.delete()
            return JsonResponse({"message": "Guru berhasil dihapus"})
        except Guru.DoesNotExist:
            return JsonResponse({"error": "Guru tidak ditemukan"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt   
def delete_pegawai(request, id):
    if request.method == "DELETE":
        try:
            pegawai = get_object_or_404(Pegawai, pk=id)
            pegawai.delete()
            return JsonResponse({"message": "Pegawai berhasil dihapus"})
        except Pegawai.DoesNotExist:
            return JsonResponse({"error": "Guru tidak ditemukan"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)
    
@api_view(['POST'])
def tambah_barang (request):
  breakpoint
  if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
  required_data = ["id_barang", "nama_barang", "jumlah", "kategori" , "deskripsi"]
  data_barang = {data: request.POST.get(data) for data in required_data}

  img = request.FILES.get("img")
  if not img:
    return JsonResponse({"error": "photo ga ada"}, status=400)
  data_barang["img"] = img.read()

  Barang.objects.create(
        id_barang = data_barang["id_barang"],
        nama_barang = data_barang["nama_barang"],
        jumlah = data_barang["jumlah"],
        kategori = data_barang["kategori"],
        deskripsi = data_barang["deskripsi"],
        img = data_barang["img"]
   )

  return JsonResponse({"message": "Siswa berhasil ditambahkan"})

@api_view(['POST'])
def tambah_pegawai (request):
    serializer = PegawaiSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def tambah_siswa(request):
    breakpoint
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    required_data = ["nis", "nama_siswa", "kelas", "no_telp","email","password"]
    data_siswa = {data: request.POST.get(data) for data in required_data}

    foto_kartuPelajar = request.FILES.get("kartu_pelajar")
    if not foto_kartuPelajar:
        return JsonResponse({"error": "eta foto na mana ey!"}, status=400)
    data_siswa["foto_kartuPelajar"] = foto_kartuPelajar.read()

    Siswa.objects.create(
        nis = data_siswa["nis"],
        nama_siswa = data_siswa["nama_siswa"],
        kelas = data_siswa["kelas"],
        no_telp = data_siswa["no_telp"],
        email = data_siswa["email"],
        password = data_siswa["password"],
        kartu_pelajar = data_siswa["foto_kartuPelajar"]
    )

    return JsonResponse({"message": "Siswa berhasil ditambahkan"})

    # if request.method == "POST":
    #     nis = request.POST.get("nis")
    #     nama_siswa = request.POST.get("nama_siswa")
    #     kelas = request.POST.get("kelas")
    #     no_telp = request.POST.get("no_telp")

    #     file = request.FILES.get("kartu_pelajar")
    #     kartu_pelajar_data = None
    #     if file:
    #         kartu_pelajar_data = file.read()  # baca file jadi biner

    #     siswa = Siswa.objects.create(
    #         nis=nis,
    #         nama_siswa=nama_siswa,
    #         kelas=kelas,
    #         no_telp=no_telp,
    #         kartu_pelajar=kartu_pelajar_data
    #     )

    #     return JsonResponse({"message": "Siswa berhasil ditambahkan"})
    # return JsonResponse({"error": "Invalid request"}, status=400)

@api_view(['POST'])
def tambah_guru (request):
    serializer =  GuruSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def detail_barang(request, id):
    try:
        barang = Barang.objects.get(pk=id)
    except Barang.DoesNotExist:
        return Response({'error': 'Barang tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BarangSerializer(barang)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BarangSerializer(barang, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        barang = Barang.objects.get(pk=id)
    except Barang.DoesNotExist:
        return Response({'error': 'Barang tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BarangSerializer(barang)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BarangSerializer(barang, data=request.data, partial=True)  # partial=True agar bisa update sebagian
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def detail_user(request, kategori , id):

    if kategori == "Pegawai":
        try:
            pegawai = Pegawai.objects.get(pk=id)
        except Pegawai.DoesNotExist:
            return Response({'error': 'Barang tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = PegawaiSerializer(pegawai)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = PegawaiSerializer(pegawai, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif kategori == "Guru":
        try:
            guru = Guru.objects.get(pk=id)
        except Guru.DoesNotExist:
            return Response({'error': 'Barang tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = GuruSerializer(guru)
            return Response(serializer.data)
    
        elif request.method == 'PUT':
            serializer = GuruSerializer(guru, data=request.data, partial=True)  # partial=True agar bisa update sebagian
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif kategori == "Siswa":
        try:
            siswa = Siswa.objects.get(pk=id)
        except Siswa.DoesNotExist:
            return Response({'error': 'Barang tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = SiswaSerializer(siswa)
            return Response(serializer.data)
    
        elif request.method == 'PUT':
            serializer =  SiswaSerializer(siswa, data=request.data, partial=True)  # partial=True agar bisa update sebagian
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def get_summary_barang(request):
    data = Barang.objects.aggregate(
        total_stok=Sum('jumlah'),     # total stok semua barang
        total_barang=Count('id_barang')      # total jenis barang
    )
    return JsonResponse(data)

def det_detail_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, pk=id)
    data = {
        "kode_pinjam": peminjaman.kode_pinjam,
        "tanggal_pinjam":  (
            peminjaman.tanggal_pinjam.isoformat() + "Z"
            if peminjaman.tanggal_pinjam else ""
        ),
        "tanggal_kembali":  (
            peminjaman.tanggal_kembali.isoformat() + "Z"
            if peminjaman.tanggal_kembali else ""
        ),
        "status_pinjam": peminjaman.status_pinjam,
        "nis": peminjaman.nis_id,       # langsung ID
        "nuptk": peminjaman.nuptk_id,   # langsung ID
        "id_pegawai": peminjaman.id_pegawai_id,  # langsung ID
    }
    return JsonResponse(data)

def det_detail_detail_peminjaman(request, id):
    detailPeminjaman = get_object_or_404(DetailPeminjaman, pk=id)
    data = {
        "kode_detail": detailPeminjaman.kode_detail,
        "id_peminjaman": detailPeminjaman.id_peminjaman_id,  # pk dari peminjaman
        "id_barang": detailPeminjaman.id_barang_id,     
        "jumlah": detailPeminjaman.jumlah,
        "waktu_pengambilan":  (
            detailPeminjaman.waktu_pengambilan.isoformat() + "Z"
            if detailPeminjaman.waktu_pengambilan else ""
        ),
        "batas_ambil": (
            detailPeminjaman.batas_ambil.isoformat() + "Z"
            if detailPeminjaman.batas_ambil else ""
        ),       # langsung ID
        "status_pengambilan": detailPeminjaman.status_pengambilan,   # langsung ID
    }
    return JsonResponse(data)

@api_view(['POST'])
def update_status(request):
    kode_pinjam = request.data.get("kode_pinjam")

    if not kode_pinjam:
        return Response({"success": False, "message": "Kode pinjam wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        peminjaman = Peminjaman.objects.get(kode_pinjam=kode_pinjam)
    except Peminjaman.DoesNotExist:
        return Response({"success": False, "message": "Peminjaman tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

    # ✅ hanya bisa ubah kalau status = "Sedang Diambil"
    if peminjaman.status_pinjam != "Sedang Diambil":
        return Response({
            "success": False,
            "message": f"Tidak bisa ubah status, status sekarang: {peminjaman.status_pinjam}"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update status peminjaman
    peminjaman.status_pinjam = "Masih Dipinjam"
    peminjaman.save()

    # Ambil detail peminjaman terkait
    details = DetailPeminjaman.objects.filter(id_peminjaman=peminjaman)

    barang_updated = []
    for detail in details:
        # Set waktu pengambilan
        detail.waktu_pengambilan = timezone.now()
        detail.save()

        # Kurangi stok barang dari field id_barang
        barang = detail.id_barang  # ini FK ke Barang
        if barang:
            barang.jumlah -= detail.jumlah
            if barang.jumlah < 0:
                barang.jumlah = 0
            barang.save()

            barang_updated.append({
                "id_barang": barang.id_barang,
                "nama_barang": barang.nama_barang,
                "jumlah_dipinjam": detail.jumlah,
                "sisa_stok": barang.jumlah
            })

    return Response({
        "success": True,
        "message": f"Status berhasil diubah menjadi {peminjaman.status_pinjam}",
        "detail": barang_updated
    })


@api_view(['POST'])
def scan_pengembalian(request):
    kode_detail = request.data.get("kode_detail")

    try:
        detail = DetailPeminjaman.objects.get(kode_detail=kode_detail)
        peminjaman = detail.id_peminjaman  

        # waktu scan sekarang (aware)
        waktu_scan = timezone.now()

        # pastikan tanggal_kembali dari peminjaman juga aware
        tgl_kembali_peminjaman = peminjaman.tanggal_kembali
        if tgl_kembali_peminjaman and timezone.is_naive(tgl_kembali_peminjaman):
            tgl_kembali_peminjaman = timezone.make_aware(tgl_kembali_peminjaman)

        # isi tanggal_kembali di detail
        detail.tanggal_kembali = waktu_scan  

        # cek keterlambatan
        if tgl_kembali_peminjaman:
            if waktu_scan > tgl_kembali_peminjaman:
                detail.status_pengambilan = "Terlambat"
            else:
                detail.status_pengambilan = "Sudah Dikembalikan"
        else:
            detail.status_pengambilan = "Sudah Dikembalikan"

        detail.save()

        # update stok barang
        barang = detail.id_barang
        barang.jumlah += detail.jumlah
        barang.save()

        # cek apakah masih ada barang yang belum dikembalikan
        masih_dipinjam = peminjaman.detailpeminjaman_set.filter(
            status_pengambilan="Belum Dikembalikan"
        ).exists()

        peminjaman.status_pinjam = "Masih Dipinjam" if masih_dipinjam else "Selesai"
        peminjaman.save()

        return Response({
            "message": "Scan berhasil diproses",
            "status_detail": detail.status_pengambilan,
            "status_peminjaman": peminjaman.status_pinjam,
            "tanggal_kembali_detail": waktu_scan,
            "tanggal_kembali_peminjaman": tgl_kembali_peminjaman
        })

    except DetailPeminjaman.DoesNotExist:
        return Response({"error": "Detail peminjaman tidak ditemukan"}, status=404)
