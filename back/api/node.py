from django.contrib.auth.models import User
from django.db.models import Q
from fastapi import APIRouter, Depends

from back.depends.user import get_current_active_user
from back.models.node import Node
from back.schemas.node import NodePointGet, SensorLocationPointGet
from back.utils.exceptions import NotFound, PermissionDenied

router = APIRouter(tags=["node"], prefix="/node")


@router.get('/all')
def get_nodes():
    nodes_query = Node.objects.select_related('location').only(
        'id', 'uid', 'location__longitude', 'location__latitude'
    ).filter(
        location__longitude__isnull=False,
        location__latitude__isnull=False,
    )
    nodes = []
    for node in nodes_query:
        node_schema = NodePointGet.from_orm(node)
        nodes.append(node_schema.dict())
    return nodes


@router.get('/{node_id}/', response_model=NodePointGet)
def get_node(node_id: int):
    """
    Данные по датчику
    todo: рефакторить
    """

    try:
        node = Node.objects.get(id=node_id)
        print(node)
        result = NodePointGet(**node.__dict__)
        print(result)
        metrics = node.get_metrics()
        result.aqi = metrics.aqi
        result.aqi_category = metrics.aqi_category
        result.pm25 = metrics.pm25
        result.pm10 = metrics.pm10
        result.humidity = metrics.humidity
        result.temperature = metrics.temperature
        result.pressure = metrics.pressure
        result.wind = node.wind
        result.city = node.city
        location = SensorLocationPointGet(longitude=node.location.longitude, latitude=node.location.latitude)
        result.location = location

    except Node.DoesNotExist:
        raise NotFound

    return result


@router.get('/{node_id}/history/')
def get_node_history(node_id: int):
    try:
        node = Node.objects.get(id=node_id)
    except Node.DoesNotExist:
        raise NotFound
    return node.history


@router.post('/')
def create_node(user: User = Depends(get_current_active_user)):
    if not user.is_staff:
        raise PermissionDenied
    pass
