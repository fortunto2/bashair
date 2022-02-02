from fastapi import Body, APIRouter
from back.models.sensors import Node, SensorLocation

router = APIRouter()


@router.get('/nodes')
async def nodes(payload: dict = Body(...)):

    nodes: List[Node] = await sync_to_async(Node.objects.all())
    if not nodes:
        raise HTTPException(status_code=404, detail="Nodes not found.")

    return nodes