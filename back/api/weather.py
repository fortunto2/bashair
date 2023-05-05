from config.owm import weather_manager


def get_weather(latitude, longitude):
    """
    Получаем данные через апи погоды https://openweathermap.org/api
    """

    result = {}

    if latitude is not None and longitude is not None:
        try:
            response = weather_manager.weather_at_coords(
                lat=float(latitude),
                lon=float(longitude)
            )
            result = response.weather.wnd
        except Exception as e:
            print(f'WARNING! Error weather API: {e}')

    return result
