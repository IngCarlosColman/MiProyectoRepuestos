"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Esta línea ahora se encarga de la ruta principal.
    # Le dice a Django que use las URLs de tu aplicación 'buscador'
    # para la ruta raíz, lo que cargará tu aplicación de React.
    path('', include('buscador.urls')),

    # Mantenemos la ruta para el panel de administración de Django.
    path('admin/', admin.site.urls),
]
