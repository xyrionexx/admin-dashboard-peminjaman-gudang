from rest_framework import serializers
from .models import Barang
from .models import Siswa
from .models import Guru
from .models import Peminjaman
from .models import DetailPeminjaman
from .models import Pegawai
import base64



class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'

class SiswaSerializer(serializers.ModelSerializer):
    kartu_pelajar = serializers.SerializerMethodField()  # custom field

    class Meta:
        model = Siswa
        fields = '__all__'

    def get_kartu_pelajar(self, obj):
        if obj.kartu_pelajar:
            # encode bytea menjadi base64 dan buat data URL
            return f"data:image/png;base64,{base64.b64encode(obj.kartu_pelajar).decode()}"
        return None

class GuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guru
        fields = '__all__'
class PegawaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pegawai
        fields = '__all__'

class PeminjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peminjaman
        fields = '__all__'

class DetailPeminjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPeminjaman
        fields = '__all__'

class DetailPeminjamanFlatSerializer(serializers.Serializer):
    kode_pinjam = serializers.CharField()
    nama_peminjam = serializers.CharField()
    jenis_peminjam = serializers.CharField()
    nama_barang = serializers.CharField()
    jumlah_dipinjam = serializers.IntegerField()
    status_barang = serializers.CharField()
    tanggal_pinjam = serializers.DateField()
    tanggal_kembali = serializers.DateField()
    batas_ambil = serializers.DateField()
    kode_detail = serializers.CharField()
    status_peminjaman = serializers.CharField()