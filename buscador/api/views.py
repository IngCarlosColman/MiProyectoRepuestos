from rest_framework import generics
from ..models import RepuestoGlobal, Tienda
from .serializers import RepuestoGlobalSerializer, TiendaSerializer

class RepuestoGlobalList(generics.ListAPIView):
    """
    Vista que devuelve una lista de todos los repuestos globales.
    """
    queryset = RepuestoGlobal.objects.all()
    serializer_class = RepuestoGlobalSerializer

class TiendaList(generics.ListAPIView):
    """
    Vista que devuelve una lista de todas las tiendas.
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
