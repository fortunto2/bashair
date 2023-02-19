from django.contrib.gis import admin
from django.contrib.gis.geos import Point
from leaflet.admin import LeafletGeoAdmin

from back.admin import MemberCityAdminAbstract
from back.admin.sensor import MemberCityFilter
from back.models.signal import *


class SignalMediaInline(admin.TabularInline):
    model = SignalMedia
    max_num = 5
    extra = 0


@admin.register(Signal)
class SignalAdmin(LeafletGeoAdmin, MemberCityAdminAbstract):

    search_fields = ['text', 'point', 'owner']
    list_display = ['owner', 'text', 'point', 'status', 'city', 'created']
    list_filter = [MemberCityFilter, 'status']
    inlines = [
        SignalMediaInline,
    ]


@admin.register(SignalProperties)
class SignalPropertiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'group']


# @admin.register(SignalMedia)
# class SignalMediaAdmin(admin.ModelAdmin):
#     search_fields = ['signal']
#     list_display = ['signal', 'file']


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'email', 'address', 'city', 'report_url']
    list_display = ['name', 'address', 'phone', 'city', 'phone']


class SignalToInstanceMediaInline(admin.TabularInline):
    model = SignalToInstanceMedia
    max_num = 5
    extra = 0


@admin.register(SignalToInstance)
class SignalToInstanceAdmin(admin.ModelAdmin):
    search_fields = ['text', 'signal', 'instance', 'response']
    list_display = ['text', 'instance', 'time_of_report', 'created']
    list_filter = ['status']
    inlines = [
        SignalToInstanceMediaInline,
    ]
