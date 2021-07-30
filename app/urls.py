
from django.urls import path, re_path
from app import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    # The home page
    # path('', views.home, name='home'),

    path('dashboard',views.dashboard,name='dashboard'),

    path('dashboard/berita', views.admin_berita, name='admin_berita'),
    path('dashboard/berita/<slug:slug>', views.admin_berita_detail, name='admin_berita_detail'),
    path('dashboard/berita/edit/<slug:slug>', views.admin_berita_edit, name='admin_berita_edit'),
    path('dashboard/berita/edit/<slug:slug>/update', views.admin_berita_update, name='admin_berita_update'),
    path('dashboard/berita/delete/<slug:slug>', views.admin_berita_delete, name='admin_berita_delete'),

    path('dashboard/toko', views.admin_toko, name='admin_toko'),
    path('dashboard/toko/<slug:slug>', views.admin_toko_detail, name='admin_toko_detail'),
    path('dashboard/toko/edit/<slug:slug>', views.admin_toko_edit, name='admin_toko_edit'),
    path('dashboard/toko/edit/<slug:slug>/update', views.admin_toko_update, name='admin_toko_update'),
    path('dashboard/toko/delete/<slug:slug>', views.admin_toko_delete, name='admin_toko_delete'),

    path('dashboard/sejarah', views.admin_sejarah, name='admin_sejarah'),
    path('dashboard/sejarah/<slug:slug>', views.admin_sejarah_detail, name='admin_sejarah_detail'),
    path('dashboard/sejarah/edit/<slug:slug>', views.admin_sejarah_edit, name='admin_sejarah_edit'),
    path('dashboard/sejarah/edit/<slug:slug>/update', views.admin_sejarah_update, name='admin_sejarah_update'),
    path('dashboard/sejarah/delete/<slug:slug>', views.admin_sejarah_delete, name='admin_sejarah_delete'),

    path('toko-batik',views.toko_batik,name='toko_batik'),
    path('toko-batik/<slug:slug>',views.toko_batik_detail,name='toko_batik_detail'),
    
    path('berita',views.berita,name='berita'),
    path('berita/<slug:slug>',views.berita_detail,name='berita_detail'),

    url(r'^$',views.home,name='home'),
    url('scan',views.scan,name='scan'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

