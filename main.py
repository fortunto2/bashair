from fastapi import FastAPI, Body, HTTPException
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from bots.telega import bot
from config import settings
from db.influx import client
from db.schemas.influx_warning import InfluxWarning
from db.schemas.sensor_measurement import SensorMeasurement, SensorData
from fastapi import Request

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post('/upload_measurement')
async def upload_measurement(data: SensorData):
    # print(data)

    NAME_MAP = {
        "Max_cycle": "max_micro",
        "Samples": "samples",
        "Min_cycle": "min_micro",
        "Signal": "signal",
        "SDS_P1": "pm10",
        "SDS_P2": "pm25",
        "BME280_temperature": "temperature",
        "BME280_humidity": "humidity",
        "BME280_pressure": "pressure",
    }

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value
        data_points[NAME_MAP.get(dp.value_type, dp.value_type)] = dp.value

    try:
        sensor_measurement = SensorMeasurement(**data_points)
    except Exception as e:
        print(data.node_tag, e)
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e))

    sensor_measurement.aqi = sensor_measurement.get_aqi_value
    sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

    # print(sensor_measurement.dict())

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = Point.from_dict({
        "measurement": settings.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag
        },
    })

    write_api.write(bucket=settings.MEASUREMENT_NAME, record=p)

    return sensor_measurement.dict()


@app.post('/notify')
async def influx_notify(payload: dict = Body(...)):

    new_payload = {}
    # remove kew with like '_start' to 'start'
    for key, value in payload.items():
        if key[0] == '_':
            key = key[1:]
        new_payload[key] = value

    influx_warning = InfluxWarning(**new_payload)
    print(influx_warning.dict(exclude_unset=True))

    txt=f"""
Тревога: {influx_warning.check_name}!
Уровень: {influx_warning.level}
Датчик: {influx_warning.node}
Время: {influx_warning.stop}
---
   """

    await bot.send_message(chat_id=121250082, text=txt)
    return influx_warning.dict(exclude_unset=True)


@app.post('/test')
async def test(request: Request):
    print(await request.body())
    return await request.body()

if __name__ == "__main__":
    import uvicorn

    # loop = asyncio.get_event_loop()
    # config = uvicorn.Config("main:app", host='0.0.0.0', port=8000, loop=loop, reload=True)
    # server = uvicorn.Server(config)
    # loop.run_until_complete(server.serve())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
