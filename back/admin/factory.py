from django.contrib.gis.geos import Point
from leaflet.admin import LeafletGeoAdmin

from back.admin import MemberCityAdminAbstract
from back.models.factory import Factory

from django.contrib.gis import admin


@admin.register(Factory)
class FactoryAdmin(LeafletGeoAdmin, MemberCityAdminAbstract):

    search_fields = ['name', 'phone', 'email', 'city', 'factory_type', 'point']
    list_display = ['name', 'phone', 'email', 'city', 'factory_type', 'point']
