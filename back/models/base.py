from django.contrib.gis.db import models as geomodel
from django.db import models
from django.db.models import DateTimeField

from back.models.city import City
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point


class LocationModel(models.Model):
    """
    Location

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    point = geomodel.PointField(null=True)

    # заполняется автоматом на основе координат
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)

    street_name = models.CharField(null=True, blank=True, max_length=200)
    street_number = models.CharField(null=True, blank=True, max_length=10)
    postalcode = models.CharField(null=True, blank=True, max_length=6)

    def save(self, *args, **kwargs):

        if not self.point:
            self.point = Point(self.longitude, self.latitude)

        self.latitude = self.point.y
        self.longitude = self.point.x
        super(LocationModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CreationDateTimeField(DateTimeField):
    """
    CreationDateTimeField

    By default, sets editable=False, blank=True, auto_now_add=True
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('auto_now_add', True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.editable is not False:
            kwargs['editable'] = True
        if self.blank is not True:
            kwargs['blank'] = False
        if self.auto_now_add is not False:
            kwargs['auto_now_add'] = True
        return name, path, args, kwargs


class ModificationDateTimeField(CreationDateTimeField):
    """
    ModificationDateTimeField

    By default, sets editable=False, blank=True, auto_now=True

    Sets value to now every time the object is saved.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_now', True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now is not False:
            kwargs['auto_now'] = True
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if not getattr(model_instance, 'update_modified', True):
            return getattr(model_instance, self.attname)
        return super().pre_save(model_instance, add)


class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    # def save(self, **kwargs):
    #     #  fix TypeError: save() got an unexpected keyword argument 'force_insert'
    #     if 'force_insert' in kwargs:
    #         kwargs.pop('force_insert')
    #     if 'force_update' in kwargs:
    #         kwargs.pop('force_update')
    #     if 'update_fields' in kwargs:
    #         kwargs.pop('update_fields')
    #     if 'using' in kwargs:
    #         kwargs.pop('using')
    #     self.update_modified = kwargs.pop('update_modified', getattr(self, 'update_modified', True))
    #     super().save(**kwargs)

    class Meta:
        get_latest_by = 'modified'
        abstract = True
