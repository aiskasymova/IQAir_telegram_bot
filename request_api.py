import requests

from Functions import buttons_after_req, print_pollution
from Globals import (bot, return_url_api)


def aqi_api(city_name, user_id):
    keyboard = buttons_after_req()
    url_api = return_url_api(city_name)
    try:
        response = requests.get(url_api)
        pollution = response.json()

        city_name = pollution['data']['city']
        city_aqi = pollution['data']['current']['pollution']['aqius']
        air_status = 'empty'
        if city_aqi < 51:
            air_status = 'Good'
        elif city_aqi < 101:
            air_status = 'Moderate'
        elif city_aqi < 151:
            air_status = 'Unhealthy for sensitive groups'
        elif city_aqi < 201:
            air_status = 'Unhealthy'
        elif city_aqi < 301:
            air_status = 'Very Unhealthy'
        else:
            air_status = 'Hazardous'
        city_temp = pollution['data']['current']['weather']['tp']
        city_hum = pollution['data']['current']['weather']['hu']

        pollution_text = bot.send_message(user_id,
                                          print_pollution(city_name, city_aqi,
                                                          air_status, city_temp, city_hum),
                                          reply_markup=keyboard)

    except KeyError:
        pollution_text = bot.send_message(user_id,
                                          f"{'I could not find anything about'}: {city_name} :(",
                                          reply_markup=keyboard)
    return pollution_text
