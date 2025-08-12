from django.contrib import admin
from .models import Store, Branch, Professional
from leaflet.admin import LeafletGeoAdmin

@admin.register(Store)
class StoreAdmin(LeafletGeoAdmin):
    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'address')

@admin.register(Branch)
class BranchAdmin(LeafletGeoAdmin):
    list_display = ('name', 'store', 'address', 'phone_number', 'has_delivery')
    list_filter = ('store', 'has_delivery')
    search_fields = ('name', 'address')

@admin.register(Professional)
class ProfessionalAdmin(LeafletGeoAdmin):
    list_display = ('workshop_name', 'head_mechanic_name', 'service_type', 'contact_phone', 'is_featured')
    list_filter = ('service_type', 'is_featured')
    search_fields = ('workshop_name', 'head_mechanic_name', 'address')