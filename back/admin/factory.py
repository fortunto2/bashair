
from back.models.factory import Factory

from django.contrib.gis import admin


@admin.register(Factory)
class FactoryAdmin(admin.OSMGeoAdmin):
    search_fields = ['name', 'phone', 'email', 'address', 'city', 'factory_type', 'location']
    list_display = ['name', 'phone', 'email', 'address', 'city', 'factory_type', 'location']
