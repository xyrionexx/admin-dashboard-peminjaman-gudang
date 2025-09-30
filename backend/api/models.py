from django.db import models

class Barang(models.Model):
    id_barang = models.AutoField(primary_key=True)
    nama_barang = models.CharField(max_length=20)
    jumlah = models.IntegerField()
    kategori = models.CharField(max_length=20, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    img = models.BinaryField(blank=True, null=True)

    class Meta:
        db_table = 'barang'

class Guru(models.Model):
    id = models.AutoField(primary_key=True)  # ganti nuptk jadi PK auto
    nuptk = models.CharField(max_length=20, unique=True)  # jadikan kolom unik biasa
    nama_guru = models.CharField(max_length=30)
    bidang = models.CharField(max_length=20, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'guru'


class Pegawai(models.Model):
    id = models.AutoField(primary_key=True)  # ganti id_pegawai jadi PK auto
    id_pegawai = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nama_pegawai = models.CharField(max_length=30)
    bidang = models.CharField(max_length=20, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'pegawai'


class Siswa(models.Model):
    id = models.AutoField(primary_key=True)  # ganti nis jadi PK auto
    nis = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nama_siswa = models.CharField(max_length=30)
    kelas = models.CharField(max_length=15, blank=True, null=True)
    kartu_pelajar = models.BinaryField(blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'siswa'


class Peminjaman(models.Model):
    id = models.AutoField(primary_key=True)  # ganti kode_pinjam jadi PK auto
    kode_pinjam = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nis = models.ForeignKey(Siswa, models.DO_NOTHING, db_column='nis', blank=True, null=True)
    nuptk = models.ForeignKey(Guru, models.DO_NOTHING, db_column='nuptk', blank=True, null=True)
    id_pegawai = models.ForeignKey(Pegawai, models.DO_NOTHING, db_column='id_pegawai', blank=True, null=True)
    tanggal_pinjam = models.DateTimeField()
    tanggal_kembali = models.DateTimeField(blank=True, null=True)
    status_pinjam = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'peminjaman'


class DetailPeminjaman(models.Model):
    id = models.AutoField(primary_key=True)  # ganti kode_detail jadi PK auto
    kode_detail = models.CharField(max_length=50, unique=True, blank=True, null=True)
    id_peminjaman = models.ForeignKey(Peminjaman, models.DO_NOTHING, db_column='id_peminjaman')
    id_barang = models.ForeignKey(Barang, models.DO_NOTHING, db_column='id_barang')
    jumlah = models.IntegerField()
    waktu_pengambilan = models.DateTimeField(blank=True, null=True)
    batas_ambil = models.DateTimeField(blank=True, null=True)
    status_pengambilan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'detail_peminjaman'
