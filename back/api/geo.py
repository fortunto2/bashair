import json
from typing import Optional, Dict

from django.core.serializers import serialize
from fastapi import APIRouter
from geojson_pydantic import Feature, FeatureCollection, Point

from back.models.factory import Factory
from back.models.node import Node
from back.utils.exceptions import NotFound

router = APIRouter(tags=["geo"], prefix="/geo")


@router.get('', response_model=FeatureCollection)
def get_geomap(city_id: Optional[int] = None):

    try:
        if city_id:
            factories = Factory.objects.filter(city_id=city_id)
        else:
            factories = Factory.objects.all()
    except Factory.DoesNotExist:
        raise NotFound

    factory_geojson = serialize("geojson", factories, geometry_field='polygon', fields=('name', 'id'))
    nodes_geojson = serialize("geojson", Node.objects.all(), geometry_field='point', fields=('name', 'id'))

    f = json.loads(factory_geojson)
    n = json.loads(nodes_geojson)

    f['features'] = n['features'] + f['features']

    return f
