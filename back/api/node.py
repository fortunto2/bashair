from django.db.models import Q
from fastapi import APIRouter

from back.models.node import Node
from back.schemas.node import NodePointGet

router = APIRouter(tags=["node"], prefix="/node")


@router.get('/')
def get_nodes():
    # список всех датчиков, id, локация, направление ветра, текущее значение
    nodes_query = Node.objects.select_related('location').only(
        'id', 'uid', 'location__longitude', 'location__latitude'
    ).filter(
        location__longitude__isnull=False,
        location__latitude__isnull=False,
    )
    nodes = []
    for node in nodes_query:
        node = NodePointGet.from_orm(node)
        nodes.append(node.dict())
    return nodes


@router.get('/{node_id}/')
def get_node(node_id: int):
    # данные по датчику
    pass


@router.get('/{node_id}/history/')
def get_node_history(node_id: int):
    # график из инфлюкса
    pass


@router.post('/')
def create_node():
    # Добавить проверку на админа
    pass
