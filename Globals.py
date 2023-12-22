from enum import Enum
import telebot

from PostgreSQL import PostgresDb


class Cities(Enum):
    Bishkek = 1
    Moscow = 2
    Tallinn = 3


def return_url_api(city_name):
    url_api = ""
    if city_name == Cities(1).name:
        url_api = url_iqair_bishkek
    elif city_name == Cities(2).name:
        url_api = url_iqair_moscow
    else:
        url_api = url_iqair_tallinn
    return url_api


class Globals(object):
    # --------------Sentences--------------
    str_welcome = "Hi! I'm a bot who knows about the Air Quality Index in your city"
    str_def_menu = "What you what to know?"
    str_city = "In which city do you want to know the air quality? "
    sub_city = "Which city do you want to subscribe to?"
    help_message = "Hi, I'm a bot that can quickly tell you\n" \
                   "the air quality in the city!\n" \
                   "Only three cities are available now,\n" \
                   "but soon all cities in the world will appear🙂\n" \
                   "/start - start work with bot\n" \
                   "/aqi - to know aqi in city\n" \
                   "/subscribe - subscribe for daily mailing\n" \
                   "/unsubscribe - unsubscribe\n" \
                   "/help - to know information"
    mailing_question_text = "What are you interested in?"
    cities = {"Moscow", "Bishkek", "Tallinn"}


# --------------bot-------------
TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(TOKEN)

# --------------API-------------
api_key = "YOUR KEY

# --------------url----------
url_iqair_bishkek = "http://api.airvisual.com/v2/city?city=Bishkek&state=Bishkek&country=Kyrgyzstan&key=---------"
url_iqair_moscow = "http://api.airvisual.com/v2/city?city=Moscow&state=Moscow&country=Russia&key=--------"
url_iqair_tallinn = "http://api.airvisual.com/v2/city?city=Tallinn&state=Harjumaa&country=Estonia&key=--------"

# ---------------Database-----------
db = PostgresDb()
