from django.contrib.gis import admin
from django.contrib.gis.geos import Point
from leaflet.admin import LeafletGeoAdmin

from back.models.city import City

#
# @admin.register(City)
# class CityAdmin(LeafletGeoAdmin):
#     pass

    #
    # pnt = Point(55.9144493, 53.6248106, srid=4326)  # notice how it's first long then lat
    # pnt.transform(900913)
    # default_lon, default_lat = pnt.coords
    # default_zoom = 13

