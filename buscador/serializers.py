from rest_framework import serializers
from .models import RepuestoGlobal, Vehiculo, Categoria

# Definimos un serializador para el modelo Vehiculo
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'anio']

# Definimos un serializador para el modelo Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

# Serializador principal para RepuestoGlobal, que incluirá
# los datos de Vehiculos y Categorias relacionados.
class RepuestoGlobalSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(many=True, read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = RepuestoGlobal
        # Campos que queremos exponer en la API
        fields = ['id', 'nombre', 'descripcion', 'categoria', 'vehiculo']
