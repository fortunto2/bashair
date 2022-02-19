from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from back.models.node import *

#
# class SensorInline(admin.TabularInline):
#     model = Sensor
#     max_num = 5
#     extra = 0


@admin.register(Node)
class NodeAdmin(admin.OSMGeoAdmin):
    pnt = Point(55.9144493, 53.6248106, srid=4326)  # notice how it's first long then lat
    pnt.transform(900913)
    default_lon, default_lat = pnt.coords
    default_zoom = 13

    search_fields = ['uid', 'description']
    list_display = ['uid', 'owner', 'name', 'city', 'created']

    list_filter = ['city', 'owner', 'inactive', 'industry_in_area', 'oven_in_area', 'traffic_in_area']
    # inlines = [
    #     SensorInline,
    # ]


# @admin.register(Sensor)
# class SensorAdmin(admin.ModelAdmin):
#     search_fields = ['node__uid', 'description']
#     list_display = ['node', 'pin', 'sensor_type',
#                     'description', 'created', 'modified']
#     list_filter = ['node__owner', 'sensor_type']

#
# @admin.register(SensorLocation)
# class SensorLocationAdmin(admin.ModelAdmin):
#     search_fields = ['point', ]
#     list_display = ['point', 'city', 'indoor', 'owner', 'description', 'created']
#     list_filter = ['indoor', 'owner', 'city']

#
# @admin.register(SensorType)
# class SensorTypeAdmin(admin.ModelAdmin):
#     search_fields = ['uid', 'name', 'manufacturer', 'description']
#     list_display = ['uid', 'name', 'manufacturer',
#                     'description', 'created', 'modified']
