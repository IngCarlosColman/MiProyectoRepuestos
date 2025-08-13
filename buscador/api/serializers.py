# buscador/api/serializers.py

from rest_framework import serializers
from ..models import RepuestoGlobal, Tienda, Sucursal, Vehiculo, RepuestoSucursal, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'marca', 'modelo', 'anio']

class RepuestoGlobalSerializer(serializers.ModelSerializer):
    # Relación ManyToMany de compatibilidad
    compatibilidad = VehiculoSerializer(many=True, read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = RepuestoGlobal
        fields = ['id', 'nombre', 'descripcion', 'categoria', 'imagen_url', 'compatibilidad']

class RepuestoSucursalSerializer(serializers.ModelSerializer):
    # Aquí enlazamos los datos del repuesto global para no tener que hacer otra petición
    repuesto_global = RepuestoGlobalSerializer(read_only=True)

    class Meta:
        model = RepuestoSucursal
        fields = ['precio', 'stock', 'stock_minimo', 'repuesto_global']

class SucursalSerializer(serializers.ModelSerializer):
    # Relación ManyToMany de repuestos_en_sucursal
    inventario = RepuestoSucursalSerializer(many=True, read_only=True, source='repuestosucursal_set')
    
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono', 'ubicacion', 'inventario']

class TiendaSerializer(serializers.ModelSerializer):
    # Relación de tiendas con sucursales
    sucursales = SucursalSerializer(many=True, read_only=True)

    class Meta:
        model = Tienda
        fields = ['id', 'nombre', 'logo_url', 'email', 'telefono', 'dias_atencion', 'tiene_delivery', 'sucursales']

class RepuestoGlobalConInventarioSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar los detalles de un repuesto, incluyendo
    el inventario en todas las sucursales.
    """
    categoria = CategoriaSerializer(read_only=True)
    compatibilidad = VehiculoSerializer(many=True, read_only=True)
    # Obtiene todos los objetos RepuestoSucursal relacionados con este repuesto.
    inventario_sucursales = RepuestoSucursalSerializer(many=True, read_only=True, source='repuestosucursal_set')
    
    class Meta:
        model = RepuestoGlobal
        fields = ['id', 'nombre', 'descripcion', 'categoria', 'imagen_url', 'compatibilidad', 'inventario_sucursales']
