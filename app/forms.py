# forms.py
from django import forms
from .models import *
  
class BeritaForm(forms.ModelForm):
  
    class Meta:
        model = Berita
        fields = ['thumbnail', 'judul', 'isi', 'durasi']