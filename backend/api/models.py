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
    nama_barang = models.CharField(max_length=20)
    jumlah = models.IntegerField()
    kategori = models.CharField(max_length=20, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    img = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'barang'


class DetailPeminjaman(models.Model):
    kode_detail = models.CharField(primary_key=True, max_length=50)
    id_peminjaman = models.ForeignKey('Peminjaman', models.DO_NOTHING, db_column='id_peminjaman')
    id_barang = models.ForeignKey(Barang, models.DO_NOTHING, db_column='id_barang')
    jumlah = models.IntegerField()
    waktu_pengambilan = models.DateTimeField(blank=True, null=True)
    batas_ambil = models.DateTimeField(blank=True, null=True)
    status_pengambilan = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'detail_peminjaman'

class Guru(models.Model):
    nuptk = models.CharField(primary_key=True, max_length=20)
    nama_guru = models.CharField(max_length=30)
    bidang = models.CharField(max_length=20, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'guru'


class Pegawai(models.Model):
    id_pegawai = models.CharField(primary_key=True, max_length=20)
    nama_pegawai = models.CharField(max_length=30)
    bidang = models.CharField(max_length=20, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pegawai'

class Siswa(models.Model):
    nis = models.CharField(primary_key=True, max_length=20)
    nama_siswa = models.CharField(max_length=30)
    kelas = models.CharField(max_length=15, blank=True, null=True)
    kartu_pelajar = models.BinaryField(blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'siswa'


class Peminjaman(models.Model):
    kode_pinjam = models.CharField(primary_key=True, max_length=50)
    nis = models.ForeignKey('Siswa', models.DO_NOTHING, db_column='nis', blank=True, null=True)
    nuptk = models.ForeignKey(Guru, models.DO_NOTHING, db_column='nuptk', blank=True, null=True)
    id_pegawai = models.ForeignKey(Pegawai, models.DO_NOTHING, db_column='id_pegawai', blank=True, null=True)
    tanggal_pinjam = models.DateTimeField()
    tanggal_kembali = models.DateTimeField(blank=True, null=True)
    status_pinjam = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'peminjaman'



