# core/urls.py
"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Esta línea dirige la ruta principal a tu aplicación 'buscador'.
    path('', include('buscador.urls')),

    # Mantenemos la ruta para el panel de administración de Django.
    path('admin/', admin.site.urls),
    
    # Esta línea es la que estábamos esperando.
    # Incluye las URLs de la API que definiste en 'buscador.api.urls'
    # bajo el prefijo '/api/'.
    path('api/', include('buscador.api.urls')),
]
