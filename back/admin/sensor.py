from django.contrib.gis import admin
from django import forms
from leaflet.forms.widgets import LeafletWidget

from back.admin.base import MemberCityAdminAbstract, MemberCityFilter, OSMGeoAdminCustom
from back.models.node import Node
from leaflet.admin import LeafletGeoAdmin


class NodeAdminForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = '__all__'
        widgets = {
            'uid': forms.TextInput(attrs={'placeholder': 'esp8266-'}),
            'city': forms.Select(),
            # 'point': forms.HiddenInput()
            'point': LeafletWidget(attrs={
                'settings_overrides': {
                    'DEFAULT_CENTER': (6.0, 45.0),
                }
            })
        }


#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and not self.instance.pk:
#             self.fields['uid'].initial = 'esp8266-'
#
#         if self.request:
#             self.fields['owner'].initial = self.request.user
#
#         self.fields['name'].required = True


@admin.register(Node)
class NodeAdmin(MemberCityAdminAbstract, LeafletGeoAdmin):

    search_fields = ['uid', 'description']
    list_display = ['uid', 'owner', 'name', 'city', 'created']
    list_filter = [MemberCityFilter, 'owner', 'inactive', 'industry_in_area', 'oven_in_area', 'traffic_in_area']
    # formfield_overrides = FORMFIELD_OVERRIDES
    # form = NodeAdminForm
    settings_overrides = {
       'DEFAULT_CENTER': (55.0, 45.0),
    }




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
