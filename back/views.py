import json
from pprint import pprint

from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from back.models.factory import Factory


class MapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(serialize("geojson", Factory.objects.filter().only('name', 'point')))
        pprint(context)
        return context
