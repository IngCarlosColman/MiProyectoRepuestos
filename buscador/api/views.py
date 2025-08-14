# buscador/api/views.py
# Este archivo contiene las vistas de la API para los diferentes modelos.
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_drf
from ..models import RepuestoGlobal, Tienda, Vehiculo, Categoria, RepuestoSucursal, Sucursal
from .serializers import (
    RepuestoGlobalSerializer, TiendaSerializer, RepuestoGlobalConInventarioSerializer,
    SucursalSerializer, CategoriaSerializer, VehiculoSerializer, RepuestoSucursalSerializer
)

# --- Filtros Personalizados ---
class RepuestoGlobalFilter(filters_drf.FilterSet):
    """
    Filtro personalizado para el modelo RepuestoGlobal.
    Permite filtrar por marca, modelo y año del vehículo compatible,
    y por categoría del repuesto.
    """
    # Filtro por marca del vehículo.
    marca = filters_drf.CharFilter(
        field_name='compatibilidad__marca',
        lookup_expr='iexact'
    )
    # Filtro por modelo del vehículo.
    modelo = filters_drf.CharFilter(
        field_name='compatibilidad__modelo',
        lookup_expr='iexact'
    )
    # Filtro por año del vehículo.
    anio = filters_drf.NumberFilter(
        field_name='compatibilidad__anio'
    )
    # Filtro por categoría del repuesto.
    categoria_id = filters_drf.NumberFilter(
        field_name='categoria__id'
    )

    class Meta:
        model = RepuestoGlobal
        fields = ['marca', 'modelo', 'anio', 'categoria_id']

# --- Vistas para Tiendas ---
class TiendaList(generics.ListCreateAPIView):
    """
    Vista para listar todas las tiendas o crear una nueva.
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class TiendaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar una tienda específica.
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

# --- Vistas para Sucursales ---
class SucursalList(generics.ListCreateAPIView):
    """
    Vista para listar todas las sucursales o crear una nueva.
    """
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class SucursalDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar una sucursal específica.
    """
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

# --- Vistas para Categorías ---
class CategoriaList(generics.ListCreateAPIView):
    """
    Vista para listar todas las categorías o crear una nueva.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar una categoría específica.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# --- Vistas para Vehículos ---
class VehiculoList(generics.ListCreateAPIView):
    """
    Vista para listar todos los vehículos o crear uno nuevo.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar un vehículo específico.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

# --- Vistas para Repuestos Globales ---
class RepuestoGlobalList(generics.ListAPIView):
    """
    Vista que devuelve una lista de todos los repuestos globales.
    Soporta búsqueda y filtrado por nombre, categoría, marca, modelo y año.
    """
    # Consulta base para obtener todos los repuestos.
    queryset = RepuestoGlobal.objects.all()
    # Serializador que convierte los objetos de Django a JSON.
    serializer_class = RepuestoGlobalSerializer

    # Filtros de búsqueda y ordenación de la API.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Clase de filtro personalizada.
    filterset_class = RepuestoGlobalFilter

    # Campos por los que se puede realizar una búsqueda de texto libre.
    search_fields = ['nombre', 'descripcion', 'compatibilidad__marca', 'compatibilidad__modelo']

class RepuestoGlobalDetail(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un repuesto, incluyendo el inventario en todas las sucursales.
    """
    queryset = RepuestoGlobal.objects.all()
    serializer_class = RepuestoGlobalConInventarioSerializer
    lookup_field = 'pk'

# --- Vistas para Repuestos por Sucursal ---
class RepuestoSucursalList(generics.ListCreateAPIView):
    """
    Vista para listar todos los repuestos por sucursal o crear uno nuevo.
    """
    queryset = RepuestoSucursal.objects.all()
    serializer_class = RepuestoSucursalSerializer

class RepuestoSucursalDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar un repuesto de sucursal específico.
    """
    queryset = RepuestoSucursal.objects.all()
    serializer_class = RepuestoSucursalSerializer
