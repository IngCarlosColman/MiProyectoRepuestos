# buscador/api/urls.py
# Este archivo mapea las URLs de la API a las vistas correspondientes.
from django.urls import path
from .views import (
    TiendaList, TiendaDetail, SucursalList, SucursalDetail,
    CategoriaList, CategoriaDetail, VehiculoList, VehiculoDetail,
    RepuestoGlobalList, RepuestoGlobalDetail, RepuestoSucursalList,
    RepuestoSucursalDetail
)

urlpatterns = [
    # URLs para Tiendas
    path('tiendas/', TiendaList.as_view(), name='tienda-list'),
    path('tiendas/<int:pk>/', TiendaDetail.as_view(), name='tienda-detail'),

    # URLs para Sucursales
    path('sucursales/', SucursalList.as_view(), name='sucursal-list'),
    path('sucursales/<int:pk>/', SucursalDetail.as_view(), name='sucursal-detail'),

    # URLs para Categorías
    path('categorias/', CategoriaList.as_view(), name='categoria-list'),
    path('categorias/<int:pk>/', CategoriaDetail.as_view(), name='categoria-detail'),

    # URLs para Vehículos
    path('vehiculos/', VehiculoList.as_view(), name='vehiculo-list'),
    path('vehiculos/<int:pk>/', VehiculoDetail.as_view(), name='vehiculo-detail'),

    # URLs para RepuestosGlobales
    path('repuestos-globales/', RepuestoGlobalList.as_view(), name='repuesto-global-list'),
    path('repuestos-globales/<int:pk>/', RepuestoGlobalDetail.as_view(), name='repuesto-global-detail'),

    # URLs para RepuestosSucursales
    path('repuestos-sucursales/', RepuestoSucursalList.as_view(), name='repuesto-sucursal-list'),
    path('repuestos-sucursales/<int:pk>/', RepuestoSucursalDetail.as_view(), name='repuesto-sucursal-detail'),
]
