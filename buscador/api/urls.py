from django.urls import path
from .views import RepuestoGlobalList, TiendaList

urlpatterns = [
    # Ruta para obtener la lista de repuestos globales.
    # Usaremos una vista basada en clases de Django REST Framework.
    path('repuestos/', RepuestoGlobalList.as_view(), name='repuestos_globales'),

    # Ruta para obtener la lista de tiendas.
    path('tiendas/', TiendaList.as_view(), name='tiendas_list'),
]
