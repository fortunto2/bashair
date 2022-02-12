from fastapi import APIRouter

from back.models.community import Community as CommunityModel
from back.schemas.community import Community
from back.utils.exceptions import NotFound

router = APIRouter(tags=["community"], prefix="/community")


@router.get('/{city_id}', response_model=Community)
def get_community(city_id: int):
    """
     Сообщества городское, которое модерирует данные по городу
    """

    try:
        community = CommunityModel.objects.get(id=city_id)
    except CommunityModel.DoesNotExist:
        raise NotFound
    return community
