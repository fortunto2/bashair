from django.contrib import admin

from back.models.node import *


class SensorInline(admin.TabularInline):
    model = Sensor
    max_num = 5
    extra = 0


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    search_fields = ['uid', 'description']
    list_display = ['uid', 'owner', 'location',
                    'description', 'created', 'modified']
    list_filter = ['owner', 'location']
    inlines = [
        SensorInline,
    ]


# @admin.register(Sensor)
# class SensorAdmin(admin.ModelAdmin):
#     search_fields = ['node__uid', 'description']
#     list_display = ['node', 'pin', 'sensor_type',
#                     'description', 'created', 'modified']
#     list_filter = ['node__owner', 'sensor_type']


@admin.register(SensorLocation)
class SensorLocationAdmin(admin.ModelAdmin):
    search_fields = ['location', ]
    list_display = ['location', 'city', 'indoor', 'owner', 'description', 'created']
    list_filter = ['indoor', 'owner', 'city']


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    search_fields = ['uid', 'name', 'manufacturer', 'description']
    list_display = ['uid', 'name', 'manufacturer',
                    'description', 'created', 'modified']
