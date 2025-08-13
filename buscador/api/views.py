# buscador/api/views.py

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_drf
from ..models import RepuestoGlobal, Tienda, Vehiculo, Categoria, RepuestoSucursal
from .serializers import RepuestoGlobalSerializer, TiendaSerializer, RepuestoGlobalConInventarioSerializer

# Filtros personalizados para la API
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

class TiendaList(generics.ListAPIView):
    """
    Vista que devuelve una lista de todas las tiendas.
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

class RepuestoDetalle(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un repuesto, incluyendo el inventario en todas las sucursales.
    """
    queryset = RepuestoGlobal.objects.all()
    serializer_class = RepuestoGlobalConInventarioSerializer
    lookup_field = 'pk'
