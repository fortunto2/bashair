from fastapi import APIRouter

router = APIRouter(tags=["instance"], prefix="/instance")


@router.get('/')
async def get_instances():
    pass
