from pyowm.owm import OWM

from config.envs import envs

owm = OWM(envs.OWM_KEY)
weather_manager = owm.weather_manager()
