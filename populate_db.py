import os
import django
from django.contrib.gis.geos import Point

# Configura el entorno de Django para que el script pueda acceder a los modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Importa los modelos que hemos creado
from buscador.models import (
    Vehiculo,
    Categoria,
    Tienda,
    Sucursal,
    RepuestoGlobal,
    RepuestoSucursal,
)

print("Iniciando script para poblar la base de datos...")

# --- Limpiar los datos existentes para evitar duplicados ---
RepuestoSucursal.objects.all().delete()
RepuestoGlobal.objects.all().delete()
Sucursal.objects.all().delete()
Tienda.objects.all().delete()
Vehiculo.objects.all().delete()
Categoria.objects.all().delete()

print("Datos existentes limpiados.")

# --- Crear Categorías ---
print("Creando categorías...")
categoria_frenos = Categoria.objects.create(nombre="Frenos")
categoria_motor = Categoria.objects.create(nombre="Motor")
categoria_suspension = Categoria.objects.create(nombre="Suspensión")
categoria_electronica = Categoria.objects.create(nombre="Electrónica")

# --- Crear Vehículos ---
print("Creando vehículos...")
vehiculo_corolla_2010 = Vehiculo.objects.create(marca="Toyota", modelo="Corolla", anio=2010)
vehiculo_corolla_2015 = Vehiculo.objects.create(marca="Toyota", modelo="Corolla", anio=2015)
vehiculo_focus_2012 = Vehiculo.objects.create(marca="Ford", modelo="Focus", anio=2012)
vehiculo_focus_2018 = Vehiculo.objects.create(marca="Ford", modelo="Focus", anio=2018)

# --- Crear Tiendas y Sucursales ---
print("Creando tiendas y sucursales...")
tienda_principal = Tienda.objects.create(
    nombre="Repuestos Central",
    email="contacto@repuestocentral.com",
    tiene_delivery=True,
    dias_atencion="Lunes a Sábado",
    telefono="987654321"
)
sucursal_asuncion = Sucursal.objects.create(
    tienda=tienda_principal,
    nombre="Sucursal Asunción",
    direccion="Calle Palma 123, Asunción",
    telefono="987654321",
    ubicacion=Point(-25.2965, -57.6479, srid=4326) # Coordenadas de Asunción
)
tienda_zona_sur = Tienda.objects.create(
    nombre="Repuestos del Sur",
    email="sur@repuestos.com",
    tiene_delivery=False,
    dias_atencion="Lunes a Viernes",
    telefono="123456789"
)
sucursal_san_lorenzo = Sucursal.objects.create(
    tienda=tienda_zona_sur,
    nombre="Sucursal San Lorenzo",
    direccion="Ruta 2, km 15, San Lorenzo",
    telefono="123456789",
    ubicacion=Point(-25.3400, -57.5000, srid=4326) # Coordenadas de San Lorenzo
)

# --- Crear Repuestos Globales ---
print("Creando repuestos globales...")
pastillas_freno = RepuestoGlobal.objects.create(
    nombre="Pastillas de Freno Delanteras",
    descripcion="Pastillas de freno de cerámica para un rendimiento óptimo.",
    categoria=categoria_frenos
)
pastillas_freno.compatibilidad.add(vehiculo_corolla_2010, vehiculo_focus_2012)

disco_freno = RepuestoGlobal.objects.create(
    nombre="Disco de Freno",
    descripcion="Disco de freno ventilado de alto rendimiento.",
    categoria=categoria_frenos
)
disco_freno.compatibilidad.add(vehiculo_corolla_2015)

filtro_aceite = RepuestoGlobal.objects.create(
    nombre="Filtro de Aceite",
    descripcion="Filtro de aceite de larga duración.",
    categoria=categoria_motor
)
filtro_aceite.compatibilidad.add(vehiculo_corolla_2010, vehiculo_focus_2012, vehiculo_corolla_2015, vehiculo_focus_2018)

# --- Crear Inventario para las Sucursales ---
print("Creando inventario...")
RepuestoSucursal.objects.create(
    sucursal=sucursal_asuncion,
    repuesto_global=pastillas_freno,
    precio=150000.00,
    stock=10,
    stock_minimo=2
)
RepuestoSucursal.objects.create(
    sucursal=sucursal_asuncion,
    repuesto_global=filtro_aceite,
    precio=50000.00,
    stock=25,
    stock_minimo=5
)
RepuestoSucursal.objects.create(
    sucursal=sucursal_san_lorenzo,
    repuesto_global=pastillas_freno,
    precio=145000.00,
    stock=8,
    stock_minimo=3
)
RepuestoSucursal.objects.create(
    sucursal=sucursal_san_lorenzo,
    repuesto_global=disco_freno,
    precio=250000.00,
    stock=5,
    stock_minimo=1
)

print("Base de datos poblada con éxito. Puedes verificarlo en el panel de administración o en tu API.")
