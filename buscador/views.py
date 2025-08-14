from django.shortcuts import render
from rest_framework import generics
from .models import RepuestoGlobal, Categoria, Vehiculo
from .serializers import RepuestoGlobalSerializer

# -------------------------------------------------------------
# Vista para servir la aplicación de React
# -------------------------------------------------------------
def index(request):
    """
    Esta vista simplemente renderiza el template index.html que contiene
    la aplicación de React compilada.
    """
    return render(request, 'index.html')


# -------------------------------------------------------------
# Vistas de la API
# -------------------------------------------------------------
class RepuestoGlobalList(generics.ListAPIView):
    """
    Vista de la API para listar repuestos.
    Permite filtrar por términos de búsqueda y otros campos.
    """
    serializer_class = RepuestoGlobalSerializer
    
    def get_queryset(self):
        queryset = RepuestoGlobal.objects.all()
        
        search_term = self.request.query_params.get('search', None)
        marca_filter = self.request.query_params.get('marca', None)
        modelo_filter = self.request.query_params.get('modelo', None)
        anio_filter = self.request.query_params.get('anio', None)
        categoria_filter = self.request.query_params.get('categoria_id', None)

        if search_term:
            queryset = queryset.filter(
                models.Q(nombre__icontains=search_term) |
                models.Q(descripcion__icontains=search_term)
            ).distinct()

        # Filtros de compatibilidad
        if marca_filter:
            queryset = queryset.filter(vehiculo__marca__icontains=marca_filter)
        if modelo_filter:
            queryset = queryset.filter(vehiculo__modelo__icontains=modelo_filter)
        if anio_filter:
            queryset = queryset.filter(vehiculo__anio=anio_filter)
        
        # Filtro de categoría
        if categoria_filter:
            queryset = queryset.filter(categoria=categoria_filter)

        return queryset.distinct()

