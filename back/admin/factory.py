from django.contrib.gis.geos import Point

from back.models.factory import Factory

from django.contrib.gis import admin



@admin.register(Factory)
class FactoryAdmin(admin.OSMGeoAdmin):

    pnt = Point(55.9144493, 53.6248106, srid=4326)  # notice how it's first long then lat
    pnt.transform(900913)
    default_lon, default_lat = pnt.coords
    default_zoom = 13

    search_fields = ['name', 'phone', 'email', 'city', 'factory_type', 'point']
    list_display = ['name', 'phone', 'email', 'city', 'factory_type', 'point']
