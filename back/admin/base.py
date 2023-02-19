from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.gis.admin import OSMGeoAdmin

from back.models.city import City
from back.models.user import Member


class OSMGeoAdminCustom(OSMGeoAdmin):
    map_template = "admin_osm.html"
    num_zoom = 13



class MemberCityFilter(SimpleListFilter):
    title = 'City'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        member = Member.objects.select_related('user').get(user=request.user)
        return [(city.id, city.name) for city in member.cities.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city__id=self.value())
        else:
            return queryset


class MemberCityAdminAbstract(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        self.request = None
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        try:
            member = Member.objects.select_related('user').get(user=user)
            return qs.filter(city__in=member.cities.all())
        except Member.DoesNotExist:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city':
            if request.user.is_superuser:
                kwargs['queryset'] = City.objects.all()
            else:
                member = Member.objects.select_related('user').get(user=request.user)
                kwargs['queryset'] = member.cities.all()
        elif db_field.name == 'owner' and not request.user.is_superuser:
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request  # pass the request object to the form
        return form


        # def save_model(self, request, obj, form, change):
        #     if not obj.pk:
        #         # set the owner to the current user when creating a new node
        #         obj.owner = request.user
        #     super().save_model(request, obj, form, change)
