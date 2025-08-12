from django.db import models
from django.contrib.gis.db import models as gis_models

class Store(models.Model):
    """Modelo para representar la tienda principal."""
    name = models.CharField(max_length=200, verbose_name="Nombre de la Tienda")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    website = models.URLField(blank=True, verbose_name="Sitio Web")
    location = gis_models.PointField(srid=4326, verbose_name="Ubicación GPS")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tienda Principal"
        verbose_name_plural = "Tiendas Principales"

class Branch(models.Model):
    """Modelo para representar una sucursal de la tienda."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="branches", verbose_name="Tienda Principal")
    name = models.CharField(max_length=200, verbose_name="Nombre de la Sucursal")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    location = gis_models.PointField(srid=4326, verbose_name="Ubicación GPS")
    has_delivery = models.BooleanField(default=False, verbose_name="Ofrece Delivery")

    def __str__(self):
        return f"{self.name} - {self.store.name}"

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

class Professional(models.Model):
    """Modelo para el clasificado de profesionales del sector automotriz."""
    SERVICE_CHOICES = [
        ('Taller', 'Taller'),
        ('Autoeléctrica', 'Autoeléctrica'),
        ('Tornería', 'Tornería'),
        ('Gomería', 'Gomería'),
        ('Chapería y Pintura', 'Chapería y Pintura'),
        ('Otro', 'Otro'),
    ]

    workshop_name = models.CharField(max_length=200, verbose_name="Nombre del Taller/Empresa")
    head_mechanic_name = models.CharField(max_length=100, verbose_name="Nombre del Profesional")
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="Tipo de Servicio")
    contact_phone = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    working_hours = models.CharField(max_length=255, verbose_name="Días y Horarios de Trabajo")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    location = gis_models.PointField(srid=4326, verbose_name="Ubicación GPS")
    is_featured = models.BooleanField(default=False, verbose_name="Es Anuncio Destacado")

    def __str__(self):
        return self.workshop_name

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"