from fastapi import FastAPI, Body
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from config import settings
from db.influx import client
from db.schemas.influx_warning import InfluxWarning
from db.schemas.sensor_measurement import SensorMeasurement, SensorData

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post('/upload_measurement')
async def upload_measurement(data: SensorData):
    # print(data)

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value

    sensor_measurement = SensorMeasurement(
        pm10=data_points['SDS_P1'],
        pm25=data_points['SDS_P2'],
        temperature=data_points['BME280_temperature'],
        pressure=data_points['BME280_pressure'],
        humidity=data_points['BME280_humidity'],
        samples=data_points['samples'],
        min_micro=data_points['min_micro'],
        max_micro=data_points['max_micro'],
        signal=data_points['signal'],
    )

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
    }
    )

    write_api.write(bucket=settings.MEASUREMENT_NAME, record=p)

    return sensor_measurement.dict()


@app.post('/notify')
async def influx_notify(payload: InfluxWarning):
    print(payload)
    return payload


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
