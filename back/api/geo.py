import json
from typing import Optional, Dict

from django.core.serializers import serialize
from fastapi import APIRouter
from geojson_pydantic import Feature, FeatureCollection, Point, MultiPolygon

from back.api.node import create_node_response
from back.models.factory import Factory
from back.models.node import Node
from back.schemas.factory import FactoryGet
from back.schemas.node import NodePointGet, NodePointGeo
from back.schemas.signal import SignalGet
from back.utils.exceptions import NotFound
from datetime import datetime, timedelta
from back.models.signal import Signal, SignalToInstance, SignalProperties
router = APIRouter(tags=["geo"], prefix="/geo")
from fastapi_cache.decorator import cache


@router.get('', response_model=FeatureCollection)
@cache(expire=60)
def get_geomap(city_id: Optional[int] = None):
    time_threshold = datetime.now() - timedelta(hours=24)

    try:
        if city_id:
            factories = Factory.objects.filter(city_id=city_id)
            nodes = Node.objects.filter(city_id=city_id)
            signals = Signal.objects.filter(created__gte=time_threshold, city_id=city_id)
        else:
            factories = Factory.objects.all()
            nodes = Node.objects.all()
            signals = Signal.objects.filter(created__gte=time_threshold)
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
            node_point = NodePointGeo(**node.__dict__)

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

    for signal in signals:

        feature = Feature(
            geometry=Point(coordinates=signal.point.coords),
            id=f'signal_{signal.id}'
        )

        signal_point = SignalGet(**signal.__dict__)

        feature.properties = signal_point.dict()

        features.append(feature)

    return FeatureCollection(features=features)

