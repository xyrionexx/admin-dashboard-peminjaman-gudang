# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Barang(models.Model):
    id_barang = models.CharField(primary_key=True, max_length=20)
    nama_barang = models.CharField(max_length=49)
    jumlah = models.IntegerField()
    kategori = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'barang'


class Guru(models.Model):
    nuptk = models.CharField(primary_key=True, max_length=20)
    nama_guru = models.CharField(max_length=50)
    bidang = models.CharField(max_length=10)
    no_telp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guru'


class Peminjaman(models.Model):
    kode_pinjam = models.CharField(primary_key=True, max_length=50)
    id_peminjam = models.CharField(max_length=20)
    tanggal_pinjam = models.DateTimeField()
    tanggal_ngambil = models.DateTimeField()
    surat_kegiatan = models.BinaryField(blank=True, null=True)
    kategori_pinjam = models.CharField(max_length=20)
    status_pinjam = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'peminjaman'


class Pengambilan(models.Model):
    kode_pengambilan = models.CharField(primary_key=True, max_length=50)
    id_peminjam = models.CharField(max_length=20)
    tgl_pengembalian = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pengambilan'


class Pengembalian(models.Model):
    kode_pengembalian = models.CharField(primary_key=True, max_length=40)
    kode_pinjam = models.CharField(max_length=50)
    tgl_pengembalian = models.DateTimeField()
    status_pinjam = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'pengembalian'


class Siswa(models.Model):
    nis = models.CharField(primary_key=True, max_length=20)
    nama_siswa = models.CharField(max_length=50)
    kelas = models.CharField(max_length=10)
    kartu_pelajar = models.BinaryField()
    no_telp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'siswa'
