# buscador/views.py
from django.shortcuts import render
from django.db import models # ¡Importante! Necesitamos importar 'models' para usar Q
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
        # Obtener todos los repuestos como punto de partida.
        queryset = RepuestoGlobal.objects.all()
        
        # Obtener los parámetros de la URL para filtrar.
        search_term = self.request.query_params.get('search', None)
        marca_filter = self.request.query_params.get('marca', None)
        modelo_filter = self.request.query_params.get('modelo', None)
        anio_filter = self.request.query_params.get('anio', None)
        categoria_filter = self.request.query_params.get('categoria_id', None)

        if search_term:
            queryset = queryset.filter(
                models.Q(nombre__icontains=search_term) |
                models.Q(descripcion__icontains=search_term)
            )

        # Filtros de compatibilidad:
        # Corregimos el nombre del campo a 'compatibilidad' para que coincida con el modelo.
        if marca_filter:
            queryset = queryset.filter(compatibilidad__marca__icontains=marca_filter)
        if modelo_filter:
            queryset = queryset.filter(compatibilidad__modelo__icontains=modelo_filter)
        if anio_filter:
            queryset = queryset.filter(compatibilidad__anio=anio_filter)
        
        # Filtro de categoría:
        # El nombre del campo aquí es correcto.
        if categoria_filter:
            queryset = queryset.filter(categoria=categoria_filter)
        
        # Usamos distinct() al final para evitar duplicados si se aplican múltiples filtros.
        return queryset.distinct()
