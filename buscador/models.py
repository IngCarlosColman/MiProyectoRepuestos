from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

# =================================================================
# Modelo Base (Abstracto)
# Contiene campos comunes a todos los modelos para evitar repetición.
# =================================================================
class BaseModel(models.Model):
    """
    Modelo base abstracto para incluir campos comunes como la fecha de
    creación, actualización y un estado activo.
    """
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        abstract = True
        verbose_name = "Modelo Base"
        verbose_name_plural = "Modelos Base"


# =================================================================
# Modelos de Tiendas y Sucursales
# =================================================================
class Tienda(BaseModel):
    """
    Representa una tienda o empresa de repuestos.
    """
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre de la Tienda",
        unique=True
    )
    logo_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL del Logo de la Tienda"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo Electrónico"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    dias_atencion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Días y horarios de atención"
    )
    tiene_delivery = models.BooleanField(
        default=False,
        verbose_name="Ofrece servicio de Delivery"
    )

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Sucursal(BaseModel):
    """
    Representa una sucursal o punto de venta de una tienda.
    Incluye un campo de geolocalización usando PostGIS para el mapa interactivo.
    """
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        related_name='sucursales',
        verbose_name="Tienda"
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre de la Sucursal"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    # Campo de geolocalización usando PostGIS.
    ubicacion = gis_models.PointField(
        verbose_name="Ubicación (Lat, Lng)",
        help_text="Punto geográfico de la sucursal."
    )

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['tienda', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.tienda.nombre})"


# =================================================================
# Modelos de Catálogo
# =================================================================
class Categoria(BaseModel):
    """
    Representa las categorías de repuestos (ej. 'Motor', 'Frenos', 'Suspensión').
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la Categoría"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Vehiculo(BaseModel):
    """
    Representa la información de un vehículo (marca, modelo, año).
    Este modelo es la clave para manejar la compatibilidad de forma robusta.
    """
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca"
    )
    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo"
    )
    anio = models.IntegerField(
        verbose_name="Año"
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        unique_together = ('marca', 'modelo', 'anio')
        ordering = ['marca', 'modelo', 'anio']

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"


# =================================================================
# Repuestos
# =================================================================
class RepuestoGlobal(BaseModel):
    """
    Representa un repuesto genérico en el sistema. Es el catálogo maestro.
    Contiene la información global del repuesto, sin datos de precio o stock.
    """
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre del Repuesto"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Categoría"
    )
    imagen_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL de la Imagen"
    )
    
    # Nuevo campo: Relación ManyToMany con el modelo Vehiculo para manejar la compatibilidad.
    compatibilidad = models.ManyToManyField(
        Vehiculo,
        related_name='repuestos_compatibles',
        verbose_name="Vehículos compatibles"
    )

    class Meta:
        verbose_name = "Repuesto Global"
        verbose_name_plural = "Repuestos Globales"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# =================================================================
# Relación de Repuestos con Sucursales (Stock y Precio)
# =================================================================
class RepuestoSucursal(BaseModel):
    """
    Modelo intermedio que define el stock y precio de un repuesto específico
    en una sucursal en particular.
    """
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        verbose_name="Sucursal"
    )
    repuesto_global = models.ForeignKey(
        RepuestoGlobal,
        on_delete=models.CASCADE,
        verbose_name="Repuesto Global"
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio"
    )
    stock = models.IntegerField(
        default=0,
        verbose_name="Stock disponible"
    )
    stock_minimo = models.IntegerField(
        default=0,
        verbose_name="Stock Mínimo"
    )

    class Meta:
        verbose_name = "Repuesto por Sucursal"
        verbose_name_plural = "Repuestos por Sucursal"
        unique_together = ('sucursal', 'repuesto_global')

    def __str__(self):
        return f"{self.repuesto_global.nombre} en {self.sucursal.nombre}"
