import json
from pprint import pprint

from django.views.generic.base import TemplateView

from back.api.geo import get_geomap_features

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


# create a view for get_geomap function

class GeoMapView(TemplateView):
    """Markers map view."""

    template_name = "simple.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)

        # markers = serialize("geojson", Factory.objects.all(), geometry_field='polygon', fields=('name',))
        # get markers and run get_geomap witn async_to_sync
        markers = get_geomap_features()

        context["markers"] = markers.features
        pprint(context)
        return context

