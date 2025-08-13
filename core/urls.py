"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Redirecciona la URL base ('/') a la lista de repuestos de la API.
    path('', RedirectView.as_view(url='api/repuestos/', permanent=True)),

    path('admin/', admin.site.urls),
    # Incluye las URLs de la API desde tu aplicación 'buscador'
    path('api/', include('buscador.api.urls')),
]
