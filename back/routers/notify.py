from fastapi import Body, APIRouter

from back.schemas.influx import InfluxWarning
from bots.telega import bot

router = APIRouter()


@router.post('/notify')
async def influx_notify(payload: dict = Body(...)):

    new_payload = {}
    # remove kew with like '_start' to 'start'
    for key, value in payload.items():
        if key[0] == '_':
            key = key[1:]
        new_payload[key] = value

    influx_warning = InfluxWarning(**new_payload)
    print(influx_warning.dict(skip_defaults=True))

    txt=f"""
Тревога: {influx_warning.check_name}!
Уровень: {influx_warning.level}
Датчик: {influx_warning.node}
Время: {influx_warning.stop}
---
   """

    bot.send_message(chat_id=121250082, text=txt)
    return influx_warning.dict(skip_defaults=True)
