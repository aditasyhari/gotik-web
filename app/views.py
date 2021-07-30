import numpy as np
from datetime import datetime
import datetime
from math import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from PIL import Image

from .models import Toko, Sejarah, Berita
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.contrib import messages

from tensorflow.keras.models import load_model
import efficientnet.tfkeras


# Predict
# parameters
input_size = (224, 224)
channel = (3,)
input_shape = input_size + channel
labels = ['beras kutah', 'gajah oling', 'kopi sembur', 'lainnya', 'mata ikan', 'sekar jagad']

# prepocessing function
def preprocess(img, input_size):
    nimg = img.convert('RGB').resize(input_size, resample = 0)
    img_arr = (np.array(nimg)) / 255
    return img_arr

def reshape(imgs_arr):
    return np.stack(imgs_arr, axis = 0)

# Load Model
MODEL_PATH = './models/gemastik_model20.h5'
model = load_model(MODEL_PATH, compile = False)


def home(request):
    return render(request, 'frontend/home.html')

def scan(request):
    if request.method == 'POST':
        print(request)
        print(request.POST.dict())

        fileObj = request.FILES['filePath']
        fs = FileSystemStorage(location='core/static/images/'+datetime.date.today().isoformat())
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(datetime.date.today().isoformat()+'/'+filePathName)
        testimage = './core/static/images'+filePathName

        # predict the image
        img = Image.open(testimage)
        X = preprocess(img, input_size)
        X = reshape([X])
        y = model.predict(X)

        predictedLabel = labels[np.argmax(y)]
        predictedAcc = np.max(y)*100

        acc = floor(predictedAcc)

        sejarah = Sejarah.objects.filter(kategori=predictedLabel).first()

        context = {'filePathName':filePathName,'predictedLabel':predictedLabel,'acc':acc, 'sejarah':sejarah}
        return render(request,'frontend/scan.html',context)

    return render(request, 'frontend/scan.html')

def toko_batik(request):
    toko = Toko.objects.all()
    paginator = Paginator(toko, 6)
    page = request.GET.get('page')
    try:
        toko = paginator.page(page)
    except PageNotAnInteger:
        toko = paginator.page(1)
    except EmptyPage:
        toko = paginator.page(paginator.num_pages)

    return render(request, 'frontend/toko-batik.html', {'toko': toko})

def toko_batik_detail(request, slug):
    toko = Toko.objects.get(slug=slug)
    return render(request, 'frontend/detail-toko.html', {'toko': toko})

def berita(request):
    berita = Berita.objects.all()
    paginator = Paginator(berita, 3)
    page = request.GET.get('page')
    try:
        berita = paginator.page(page)
    except PageNotAnInteger:
        berita = paginator.page(1)
    except EmptyPage:
        berita = paginator.page(paginator.num_pages)

    return render(request, 'frontend/berita.html', {'berita': berita})

def berita_detail(request, slug):
    berita = Berita.objects.get(slug=slug)
    return render(request, 'frontend/detail-berita.html', {'berita': berita})

@login_required(login_url="/login/")
def dashboard(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'admin/index.html' )
    return HttpResponse(html_template.render(context, request))

# Admin Berita
@login_required(login_url="/login/")
def admin_berita(request):
    if request.method == 'POST':
        fileObj = request.FILES['thumbnail']
        fs = FileSystemStorage(location='core/static/berita/thumbnail/')
        filePathName = fs.save(str(datetime.now())+'_'+fileObj.name, fileObj)
        filePathName = fs.url('/static/berita/thumbnail/'+filePathName)

        berita = Berita(
            judul=request.POST['judul'],
            isi=request.POST['isi'],
            thumbnail=filePathName
        )
        try:
            berita.full_clean()
        except ValidationError as e:
            pass
        berita.save()
        messages.success(request, 'Berita berhasil ditambahkan!')
        return redirect('admin_berita')

    berita = Berita.objects.all()
    context = {}
    # context['form'] = form
    context['segment'] = 'admin_berita'
    context['berita'] = berita
    html_template = loader.get_template( 'admin/berita/index.html' )

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def admin_berita_detail(request, slug):
    berita = Berita.objects.get(slug=slug)
    context = {'berita': berita}
    return render(request, 'admin/berita/detail.html', context)

@login_required(login_url="/login/")
def admin_berita_edit(request, slug):
    berita = Berita.objects.get(slug=slug)
    context = {'berita': berita}
    return render(request, 'admin/berita/edit.html', context)

@login_required(login_url="/login/")
def admin_berita_update(request, slug):
    berita = Berita.objects.get(slug=slug)
    context = {'berita':berita}
    if request.method == 'POST':
        berita = Berita(
            judul=request.POST['judul'],
            isi=request.POST['isi']
            
        )
        berita.save()
        messages.success(request, 'Berita berhasil diupdate!')
        return redirect('admin_berita')
    
    return render(request, 'admin/berita/edit.html', context)

@login_required(login_url="/login/")
def admin_berita_delete(request, slug):
    berita = Berita.objects.get(slug=slug)
    berita.delete()
    messages.error(request, 'Berita berhasil dihapus!')
    return redirect('admin_berita')

# End Admin Berita


# Admin Toko
@login_required(login_url="/login/")
def admin_toko(request):
    if request.method == 'POST':
        toko = Toko(
            nama_toko=request.POST['nama_toko'],
            alamat=request.POST['alamat'],
            telp=request.POST['telp'],
            frame_maps=request.POST['frame_maps']
        )
        try:
            toko.full_clean()
        except ValidationError as e:
            pass
        toko.save()
        messages.success(request, 'Toko berhasil ditambahkan!')
        return redirect('admin_toko')

    toko = Toko.objects.all()
    context = {}
    context['segment'] = 'admin_toko'
    context['toko'] = toko
    html_template = loader.get_template('admin/toko/index.html')

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def admin_toko_detail(request, slug):
    toko = Toko.objects.get(slug=slug)
    context = {'toko': toko}
    return render(request, 'admin/toko/detail.html', context)

@login_required(login_url="/login/")
def admin_toko_edit(request, slug):
    toko = Toko.objects.get(slug=slug)
    context = {'toko': toko}
    return render(request, 'admin/toko/edit.html', context)

@login_required(login_url="/login/")
def admin_toko_update(request, slug):
    toko = Toko.objects.get(slug=slug)
    context = {'toko':toko}
    if request.method == 'POST':
        toko = Toko(
            nama_toko=request.POST['nama_toko'],
            alamat=request.POST['alamat'],
            telp=request.POST['telp'],
            frame_maps=request.POST['frame_maps']
        )
        toko.save()
        messages.success(request, 'Toko berhasil diupdate!')
        return redirect('admin_toko')
    
    return render(request, 'admin/toko/edit.html', context)

@login_required(login_url="/login/")
def admin_toko_delete(request, slug):
    toko = Toko.objects.get(slug=slug)
    toko.delete()
    messages.error(request, 'Toko berhasil dihapus!')
    return redirect('admin_toko')

# End Admin Toko


# Admin Sejarah
@login_required(login_url="/login/")
def admin_sejarah(request):
    if request.method == 'POST':
        sejarah = Sejarah(
            judul=request.POST['judul'],
            kategori=request.POST['kategori'],
            isi=request.POST['isi']
        )
        try:
            sejarah.full_clean()
        except ValidationError as e:
            pass
        sejarah.save()
        messages.success(request, 'Sejarah berhasil ditambahkan!')
        return redirect('admin_sejarah')

    sejarah = Sejarah.objects.all()
    context = {}
    context['segment'] = 'admin_sejarah'
    context['sejarah'] = sejarah
    html_template = loader.get_template('admin/sejarah/index.html')

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def admin_sejarah_detail(request, slug):
    sejarah = Sejarah.objects.get(slug=slug)
    context = {'sejarah': sejarah}
    return render(request, 'admin/sejarah/detail.html', context)

@login_required(login_url="/login/")
def admin_sejarah_edit(request, slug):
    sejarah = Sejarah.objects.get(slug=slug)
    context = {'sejarah': sejarah}
    return render(request, 'admin/sejarah/edit.html', context)

@login_required(login_url="/login/")
def admin_sejarah_update(request, slug):
    sejarah = Sejarah.objects.get(slug=slug)
    context = {'sejarah':sejarah}
    if request.method == 'POST':
        sejarah = Sejarah(
            judul=request.POST['judul'],
            kategori=request.POST['kategori'],
            isi=request.POST['isi']
        )
        sejarah.save()
        messages.success(request, 'Sejarah berhasil diupdate!')
        return redirect('admin_sejarah')
    
    return render(request, 'admin/sejarah/edit.html', context)

@login_required(login_url="/login/")
def admin_sejarah_delete(request, slug):
    sejarah = Sejarah.objects.get(slug=slug)
    sejarah.delete()
    messages.error(request, 'Sejarah berhasil dihapus!')
    return redirect('admin_sejarah')

# End Admin Sejarah


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     try:
        
#         load_template      = request.path.split('/')[-1]
#         context['segment'] = load_template
        
#         html_template = loader.get_template( load_template )
#         return HttpResponse(html_template.render(context, request))
        
#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))

#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))
