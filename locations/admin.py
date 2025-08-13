# locations/admin.py

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin # <-- CAMBIAR A LeafletGeoAdmin
from .models import (
    Store,
    StoreImage,
    Branch,
    BranchImage,
    Professional,
    ProfessionalImage,
    Product,
    Stock
)

# Inline para las imágenes de la Tienda Principal
class StoreImageInline(admin.TabularInline):
    model = StoreImage
    extra = 1

# Inline para las imágenes de Sucursales
class BranchImageInline(admin.TabularInline):
    model = BranchImage
    extra = 1

# Inline para las imágenes de Talleres/Profesionales
class ProfessionalImageInline(admin.TabularInline):
    model = ProfessionalImage
    extra = 1

# --- Administradores para los modelos ---

@admin.register(Store)
class StoreAdmin(LeafletGeoAdmin): # <-- CAMBIAMOS GISModelAdmin por LeafletGeoAdmin
    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'address')
    inlines = [StoreImageInline]

@admin.register(Branch)
class BranchAdmin(LeafletGeoAdmin): # <-- CAMBIAMOS GISModelAdmin por LeafletGeoAdmin
    list_display = ('name', 'store', 'address', 'phone_number', 'has_delivery')
    search_fields = ('name', 'address')
    list_filter = ('store', 'has_delivery')
    inlines = [BranchImageInline]

@admin.register(Professional)
class ProfessionalAdmin(LeafletGeoAdmin): # <-- CAMBIAMOS GISModelAdmin por LeafletGeoAdmin
    list_display = ('workshop_name', 'address', 'contact_phone', 'is_featured')
    search_fields = ('workshop_name', 'address')
    list_filter = (
        'is_featured',
        'service_types',
    )
    fieldsets = (
        (None, {
            'fields': (
                'workshop_name',
                'head_mechanic_name',
                'address',
                'location',
                'contact_phone',
                'logo',
                'is_featured',
                'service_types',
            )
        }),
        ('Horario de atención', {
            'fields': (
                'days_of_week',
                'opening_time',
                'closing_time',
            )
        }),
    )
    inlines = [ProfessionalImageInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number')
    search_fields = ('name', 'part_number')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'branch', 'quantity')
    list_filter = ('store', 'branch', 'product')
    search_fields = ('product__name', 'store__name', 'branch__name')