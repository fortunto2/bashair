from django.contrib import admin

from back.models.factory import Factory


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'email', 'address', 'city', 'factory_type']
    list_display = ['name', 'phone', 'email', 'address', 'city', 'factory_type']
