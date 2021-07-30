from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Berita(models.Model):
    thumbnail = models.ImageField(upload_to='core/static/berita/thumbnail', blank=True, null=True)
    judul = models.CharField("Judul", max_length=255, unique=True)
    isi = models.TextField()
    penulis = models.CharField(max_length=255, blank=True, null=True)
    durasi = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = slugify(self.judul)
        super(Berita, self).save()

    def __str__(self):
        return self.judul

class Toko(models.Model):
    thumbnail = models.ImageField(upload_to='toko/thumbnail', blank=True, null=True)
    nama_toko = models.CharField("Judul", max_length=255)
    alamat = models.TextField(blank=True, null=True)
    telp = models.CharField(max_length=15, blank=True, null=True)
    frame_maps = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = slugify(self.nama_toko)
        super(Toko, self).save()

    def __str__(self):
        return self.nama_toko

class Sejarah(models.Model):
    thumbnail = models.ImageField(upload_to='sejarah/thumbnail', blank=True, null=True)
    judul = models.CharField("Judul", max_length=255)
    isi = models.TextField(blank=True, null=True)
    kategori = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = slugify(self.judul)
        super(Sejarah, self).save()

    def __str__(self):
        return self.judul