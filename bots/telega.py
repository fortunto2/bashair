import sys
from pprint import pprint

sys.path.append('../')
sys.path.append('.')

from config.envs import envs

import logging

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
from back.time_series.air import InfluxAir

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=envs.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    txt = """
Привет! Я бот для мониторинга воздуха в Башкирии.
Подпишись на меня и я буду присылать уведомления в случае превышения показателей воздуха.
Подробнее на сайте bashair.ru и группе https://vk.com/vozduh_str 
"""
    await message.reply(txt)


@dp.message_handler(commands=['air', 'vozduh'])
async def get_air(message: types.Message):
    pprint(message.from_user.__dict__)
    pprint(message.chat.__dict__)

    influx = InfluxAir(filters={'city_id':1}, last=True, mean=True)
    metrics = influx.get_metrics()

    txt = \
"""
Средние данные за час воздуха в Стерлитамаке: 
PM2.5: {pm25}
PM10: {pm10}
AQI: {aqi}
TEMP: {temperature}
Подробнее на карте https://aircms.online/#/d/11545355
""".format(**metrics.dict())

    await message.reply(txt)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
