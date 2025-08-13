# locations/models.py

from django.contrib.gis.db import models as gis_models
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from multiselectfield import MultiSelectField

DAYS_OF_WEEK = (
    ('LUN', 'Lunes'),
    ('MAR', 'Martes'),
    ('MIE', 'Miércoles'),
    ('JUE', 'Jueves'),
    ('VIE', 'Viernes'),
    ('SAB', 'Sábado'),
    ('DOM', 'Domingo')
)

class Store(models.Model):
    """
    Modelo principal de la tienda (Matriz).
    Contiene la información central de la marca, incluyendo ubicación y horarios.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre de la Tienda")
    logo = ThumbnailerImageField(upload_to='logos/', blank=True, null=True,verbose_name="Logo")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono")
    email = models.EmailField(max_length=254, blank=True, verbose_name="Correo Electrónico")
    location = gis_models.PointField(verbose_name="Ubicación")
    opening_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Apertura")
    closing_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Cierre")
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK, max_length=100, blank=True, verbose_name="Días de Atención")

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"

    def __str__(self):
        return self.name

class StoreImage(models.Model):
    """
    Imágenes específicas de la tienda principal para el carrusel.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='images')
    image = ThumbnailerImageField(upload_to='store_images/')

    def __str__(self):
        return f"Imagen para {self.store.name}"

class Branch(models.Model):
    """
    Modelo de una sucursal, relacionado a una tienda (Matriz).
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='branches', verbose_name="Tienda Matriz")
    name = models.CharField(max_length=100, verbose_name="Nombre de la Sucursal")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono")
    has_delivery = models.BooleanField(default=False, verbose_name="Tiene Delivery")
    location = gis_models.PointField(verbose_name="Ubicación")
    opening_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Apertura")
    closing_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Cierre")
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK, max_length=100, blank=True, verbose_name="Días de Atención")

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return f"{self.name} ({self.store.name})"

class BranchImage(models.Model):
    """
    Imágenes específicas de una sucursal para el carrusel.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='images')
    image = ThumbnailerImageField(upload_to='branch_images/')

    def __str__(self):
        return f"Imagen para {self.branch.name}"

class Professional(models.Model):
    """
    Modelo independiente para talleres y profesionales.
    """
    SERVICE_TYPES = (
        ('MECANICA', 'Mecánica'),
        ('CHAPERIA', 'Chapería'),
        ('PINTURA', 'Pintura'),
        ('ELECTRICIDAD', 'Electricidad'),
    )
    
    workshop_name = models.CharField(max_length=100, verbose_name="Nombre del Taller")
    head_mechanic_name = models.CharField(max_length=100, blank=True, verbose_name="Nombre del Jefe de Taller")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Número de Contacto")
    service_types = MultiSelectField(choices=SERVICE_TYPES, verbose_name="Tipo de Servicio", blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    location = gis_models.PointField(verbose_name="Ubicación")
    logo = ThumbnailerImageField(upload_to='professional_logos/', blank=True, null=True, verbose_name="Logotipo")
    opening_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Apertura")
    closing_time = models.TimeField(blank=True, null=True, verbose_name="Hora de Cierre")
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK, max_length=100, blank=True, verbose_name="Días de Atención")

    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"

    def __str__(self):
        return self.workshop_name

class ProfessionalImage(models.Model):
    """
    Imágenes específicas de un taller o profesional para el carrusel.
    """
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='images')
    image = ThumbnailerImageField(upload_to='professional_images/')

    def __str__(self):
        return f"Imagen para {self.professional.workshop_name}"

# --- Modelos de stock ---

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    part_number = models.CharField(max_length=50, blank=True, verbose_name="Número de Parte")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

# locations/models.py
# ... (el resto del código sigue igual)

class Stock(models.Model):
    """
    Modelo para gestionar el stock de productos en cada sucursal o tienda.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sucursal")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tienda")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad")

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        # Usamos una lista para definir múltiples restricciones de unicidad
        unique_together = [
            ('branch', 'product'),
            ('store', 'product'),
        ]
        # Esta restricción asegura que un registro de stock esté asociado
        # solo a una sucursal o a una tienda, no a ambas.
        constraints = [
            models.CheckConstraint(
                check=models.Q(branch__isnull=False, store__isnull=True) | models.Q(branch__isnull=True, store__isnull=False),
                name='one_location_type_for_stock'
            )
        ]

    def __str__(self):
        if self.branch:
            return f"{self.product.name} en {self.branch.name}"
        if self.store:
            return f"{self.product.name} en {self.store.name}"
        return f"Inventario de {self.product.name}"