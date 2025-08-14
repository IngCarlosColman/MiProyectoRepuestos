import os
import sys
import django
from django.db import transaction
from django.contrib.gis.geos import Point

# CONFIGURACIÓN DEL ENTORNO DE DJANGO
# ============================================================================
# Agrega la ruta raíz de tu proyecto al sys.path para que Python pueda encontrar 'core'.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Esta línea le dice a Django dónde encontrar la configuración de tu proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
# ============================================================================


from buscador.models import (
    Tienda,
    Categoria,
    Vehiculo,
    Sucursal,
    RepuestoGlobal,
    RepuestoSucursal,
)

def borrar_datos_existentes():
    """Elimina todos los datos de las tablas del proyecto."""
    print("Eliminando datos existentes...")
    with transaction.atomic():
        RepuestoSucursal.objects.all().delete()
        RepuestoGlobal.objects.all().delete()
        Sucursal.objects.all().delete()
        Vehiculo.objects.all().delete()
        Categoria.objects.all().delete()
        Tienda.objects.all().delete()
    print("Datos eliminados correctamente.")

def crear_datos_de_ejemplo():
    """Crea datos de ejemplo para las tablas del proyecto."""
    print("Creando datos de ejemplo...")

    # Crear tiendas
    tiendas = [
        Tienda(nombre="Tienda A"),
        Tienda(nombre="Tienda B"),
        Tienda(nombre="Tienda C"),
    ]
    Tienda.objects.bulk_create(tiendas)
    print(f"Creadas {len(tiendas)} tiendas.")

    # Crear categorías
    categorias = [
        Categoria(nombre="Motor"),
        Categoria(nombre="Frenos"),
        Categoria(nombre="Suspension"),
        Categoria(nombre="Transmision"),
        Categoria(nombre="Electrico"),
    ]
    Categoria.objects.bulk_create(categorias)
    print(f"Creadas {len(categorias)} categorías.")

    # Crear vehículos - Se corrigió el nombre del campo a 'anio'
    vehiculos = [
        Vehiculo(marca="Toyota", modelo="Corolla", anio=2020),
        Vehiculo(marca="Ford", modelo="Focus", anio=2018),
        Vehiculo(marca="Nissan", modelo="Sentra", anio=2021),
    ]
    Vehiculo.objects.bulk_create(vehiculos)
    print(f"Creados {len(vehiculos)} vehículos.")

    # Crear sucursales - Se agregó un punto de ubicación de ejemplo
    sucursales = [
        Sucursal(
            nombre="Sucursal Norte",
            direccion="Calle 123, Ciudad A",
            telefono="123456789",
            tienda=tiendas[0],
            ubicacion=Point(-58.3816, -34.6037)  # Coordenadas de ejemplo
        ),
        Sucursal(
            nombre="Sucursal Centro",
            direccion="Avenida 456, Ciudad A",
            telefono="987654321",
            tienda=tiendas[0],
            ubicacion=Point(-58.3810, -34.6050)
        ),
        Sucursal(
            nombre="Sucursal Este",
            direccion="Ruta 789, Ciudad B",
            telefono="112233445",
            tienda=tiendas[1],
            ubicacion=Point(-58.3750, -34.6000)
        ),
        Sucursal(
            nombre="Sucursal Oeste",
            direccion="Calle 101, Ciudad C",
            telefono="556677889",
            tienda=tiendas[2],
            ubicacion=Point(-58.3900, -34.6100)
        ),
    ]
    Sucursal.objects.bulk_create(sucursales)
    print(f"Creadas {len(sucursales)} sucursales.")

    # Crear repuestos globales y asignar a categorías - Se corrigió el campo 'numero_parte' a 'codigo'
    repuestos_globales = [
        RepuestoGlobal(nombre="Filtro de Aceite", codigo="FA-123", categoria=categorias[0], cantidad=50),
        RepuestoGlobal(nombre="Pastilla de Freno", codigo="PF-456", categoria=categorias[1], cantidad=100),
        RepuestoGlobal(nombre="Amortiguador", codigo="AM-789", categoria=categorias[2], cantidad=75),
        RepuestoGlobal(nombre="Bujia", codigo="BU-101", categoria=categorias[0], cantidad=200),
    ]
    RepuestoGlobal.objects.bulk_create(repuestos_globales)
    print(f"Creados {len(repuestos_globales)} repuestos globales.")

    # Asignar compatibilidad - Se corrigió el campo a 'compatibilidad'
    repuestos_globales[0].compatibilidad.set([vehiculos[0], vehiculos[1]])
    repuestos_globales[1].compatibilidad.set([vehiculos[1], vehiculos[2]])
    repuestos_globales[2].compatibilidad.set([vehiculos[0]])
    repuestos_globales[3].compatibilidad.set([vehiculos[2]])

    # Crear registros de stock por sucursal - Se agregó el campo 'precio'
    repuestos_sucursales = [
        RepuestoSucursal(
            repuesto_global=repuestos_globales[0], sucursal=sucursales[0], stock=10, precio=15.50
        ),
        RepuestoSucursal(
            repuesto_global=repuestos_globales[0], sucursal=sucursales[1], stock=5, precio=14.99
        ),
        RepuestoSucursal(
            repuesto_global=repuestos_globales[1], sucursal=sucursales[2], stock=20, precio=45.00
        ),
        RepuestoSucursal(
            repuesto_global=repuestos_globales[2], sucursal=sucursales[3], stock=15, precio=89.90
        ),
        RepuestoSucursal(
            repuesto_global=repuestos_globales[3], sucursal=sucursales[0], stock=8, precio=5.25
        ),
    ]
    RepuestoSucursal.objects.bulk_create(repuestos_sucursales)
    print(f"Creados {len(repuestos_sucursales)} registros de stock por sucursal.")

    print("\n¡Todos los datos de ejemplo han sido creados exitosamente!")

# Ejecutar el script
if __name__ == '__main__':
    borrar_datos_existentes()
    crear_datos_de_ejemplo()
