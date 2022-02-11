from django.contrib import admin
from back.models.signal import *


class SignalMediaInline(admin.TabularInline):
    model = SignalMedia
    max_num = 5
    extra = 0


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    search_fields = ['text', 'location', 'owner']
    list_display = ['owner', 'text', 'location', 'status', 'created']
    list_filter = ['status']
    inlines = [
        SignalMediaInline,
    ]


@admin.register(SignalProperties)
class SignalPropertiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'group']


@admin.register(SignalMedia)
class SignalMediaAdmin(admin.ModelAdmin):
    search_fields = ['signal']
    list_display = ['signal', 'file']


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'email', 'address', 'report_url']
    list_display = ['name', 'address']


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