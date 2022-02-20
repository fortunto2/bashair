import json
from pprint import pprint

from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from back.models.factory import Factory
from back.models.node import Node


class MapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

    # def get_context_data(self, **kwargs):
    #     """Return the view context data."""
    #     context = super().get_context_data(**kwargs)
    #
    #     # markers = serialize("geojson", Factory.objects.all(), geometry_field='polygon', fields=('name',))
    #     markers = serialize("geojson", Node.objects.all(), geometry_field='point', fields=('name',))

    #     context["markers"] = json.loads(markers)
    #     pprint(context)
    #     return context
