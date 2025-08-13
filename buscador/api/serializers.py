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

class RepuestoSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepuestoSucursal
        fields = ['precio', 'stock', 'stock_minimo']

class RepuestoGlobalSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    compatibilidad = VehiculoSerializer(many=True, read_only=True)

    class Meta:
        model = RepuestoGlobal
        fields = ['id', 'nombre', 'descripcion', 'categoria', 'imagen_url', 'compatibilidad']

class SucursalSerializer(serializers.ModelSerializer):
    # Relación uno a muchos: cada sucursal tiene un conjunto de repuestos
    # Aquí mostramos los repuestos específicos de esta sucursal
    repuestos_en_sucursal = RepuestoSucursalSerializer(source='repuestosucursal_set', many=True, read_only=True)

    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono', 'ubicacion', 'repuestos_en_sucursal']

class TiendaSerializer(serializers.ModelSerializer):
    # Relación uno a muchos: una tienda puede tener varias sucursales
    sucursales = SucursalSerializer(many=True, read_only=True, source='sucursales')

    class Meta:
        model = Tienda
        fields = ['id', 'nombre', 'logo_url', 'email', 'telefono', 'dias_atencion', 'tiene_delivery', 'sucursales']
