import json
from typing import Optional, Dict

from django.core.serializers import serialize
from fastapi import APIRouter
from geojson_pydantic import Feature, FeatureCollection, Point, MultiPolygon

from back.api.node import create_node_response
from back.models.factory import Factory
from back.models.node import Node
from back.schemas.factory import FactoryGet
from back.schemas.node import NodePointGet
from back.utils.exceptions import NotFound

router = APIRouter(tags=["geo"], prefix="/geo")


@router.get('', response_model=FeatureCollection)
def get_geomap(city_id: Optional[int] = None):

    try:
        if city_id:
            factories = Factory.objects.filter(city_id=city_id)
            nodes = Node.objects.filter(city_id=city_id)
        else:
            factories = Factory.objects.all()
            nodes = Node.objects.all()
    except Factory.DoesNotExist:
        raise NotFound

    features = []

    for node in nodes:

        feature = Feature(
            geometry=Point(coordinates=node.point.coords),
            id=f'node_{node.id}'
        )

        node_point: NodePointGet = create_node_response(node)

        if not node_point:
            # todo: show offline nodes
            continue

        feature.properties = node_point.dict()

        features.append(feature)

    for factory in factories:

        feature = Feature(
            geometry=MultiPolygon(coordinates=factory.polygon.coords),
            id=f'factory_{factory.id}'
        )

        factory_model = FactoryGet(**factory.__dict__)

        feature.properties = factory_model.dict()

        features.append(feature)

    return FeatureCollection(features=features)
