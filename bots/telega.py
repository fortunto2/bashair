import sys
from pprint import pprint

sys.path.append('../')
sys.path.append('.')

from config import settings

import logging

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
from db.influx import client, get_air_values_mean

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_TOKEN)
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
    txt = \
f"""
Средние данные за час воздуха в Стерлитамаке: 
PM2.5: {get_air_values_mean(field='pm25')}
PM10: {get_air_values_mean(field='pm10')}
AQI: {get_air_values_mean(field='aqi')}
TEMP: {get_air_values_mean(field='temperature')}
Подробнее на карте https://maps.sensor.community/?nowind#12/53.6582/55.9335
"""

    await message.reply(txt)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)