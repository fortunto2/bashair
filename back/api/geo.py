import json
from typing import Optional, Dict

from django.core.serializers import serialize
from fastapi import APIRouter
from geojson_pydantic import Feature, FeatureCollection, Point

from back.api.node import create_node_response
from back.models.factory import Factory
from back.models.node import Node
from back.schemas.node import NodePointGet
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
    f = FeatureCollection(**json.loads(factory_geojson))

    nodes_features = []

    for node in Node.objects.all():

        feature = Feature(geometry=Point(coordinates=node.point.coords))

        node_point: NodePointGet = create_node_response(node)

        if node_point:
            feature.properties = node_point.dict()

        nodes_features.append(feature)


    # f.features = n.features + f.features

    return FeatureCollection(features=nodes_features)
