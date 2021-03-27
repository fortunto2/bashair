from fastapi import FastAPI, Body

from bots.telega import bot
from back.schemas.influx import InfluxWarning


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post('/notify')
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


@app.post('/test')
async def test(payload: dict = Body(...)):
    print(payload)
    return payload


if __name__ == "__main__":
    import uvicorn

    # loop = asyncio.get_event_loop()
    # config = uvicorn.Config("main:app", host='0.0.0.0', port=8000, loop=loop, reload=True)
    # server = uvicorn.Server(config)
    # loop.run_until_complete(server.serve())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
