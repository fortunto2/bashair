from fastapi import APIRouter

from back.schemas.instance import InstanceGet
from back.models.instance import Instance as InstanceModel
from back.utils.exceptions import NotFound

router = APIRouter(tags=["instance"], prefix="/instance")


@router.get('/{city_id}', response_model=InstanceGet)
def get_instance(city_id: int):
    """
     Инстанции для жалобы в конкретном городе, типа ЕДДС
    """

    try:
        instance = InstanceModel.objects.get(id=city_id)
    except InstanceModel.DoesNotExist:
        raise NotFound
    return instance
