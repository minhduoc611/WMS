from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('KhoNVL/', include('KhoNVL.urls')),
    path('KhoThanhPham/', include('KhoThanhPham.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/KhoNVL/', permanent=True)),  
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
