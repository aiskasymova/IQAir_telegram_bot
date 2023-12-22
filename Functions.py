import schedule
from telebot import types
from time import sleep

from Globals import bot, Globals, db


def buttons_in_default_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_check_now = types.KeyboardButton(text="Check the AQI now")
    btn_subscribe = types.KeyboardButton(text="Receive daily")
    keyboard.add(btn_check_now, btn_subscribe)
    return keyboard


def button_in_mailing():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_sub = types.KeyboardButton(text="Subscribe")
    btn_unsub = types.KeyboardButton(text="Unsubscribe")
    btn_back = types.KeyboardButton(text="Back")
    keyboard.add(btn_sub, btn_unsub, btn_back)
    return keyboard


def button_in_subscribe():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_bish = types.KeyboardButton(text="Bishkek")
    btn_mos = types.KeyboardButton(text="Moscow")
    btn_tall = types.KeyboardButton(text="Tallinn")
    keyboard.add(btn_bish, btn_mos, btn_tall)
    return keyboard


def buttons_choose_city():
    """
    Function to add buttons in selecting city.
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_bishkek = types.KeyboardButton(text="Bishkek")
    btn_tallinn = types.KeyboardButton(text="Tallinn")
    btn_moscow = types.KeyboardButton(text="Moscow")
    keyboard.add(btn_bishkek, btn_moscow, btn_tallinn)
    return keyboard


def buttons_after_req():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cont_weather = types.KeyboardButton(text="Continue cheсking AQI")
    stop_weather = types.KeyboardButton(text="Menu")
    keyboard.add(cont_weather, stop_weather)
    return keyboard


def print_pollution(city_name, city_aqi, air_status, city_temp, city_hum):
    return (f"{city_name}:\nAQI {city_aqi} \n"
            f"{air_status}\n"
            f"⛅️{city_temp}℃\n"
            f"💧{city_hum}")


def check_user_unsubscribe(message):
    """
    checking from db
    """
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, message.text, False)
        bot.send_message(user_id, "You are not subscribed ")
    elif db.check_status(user_id) == "(True,)":
        db.update_subscription(user_id, False)
        bot.send_message(user_id, "You have successfully unsubscribed")
    elif db.check_status(user_id) == "(False,)":
        bot.send_message(user_id, "Your subscription is not active")
    db.print_info()


def check_user_subscribe(message, default_menu):
    """
    checking from db
    """
    user_id = message.chat.id
    if not db.subscriber_exists(user_id):
        db.add_subscriber(user_id, message.text, True)
        bot.send_message(user_id, "you have successfully subscribed")
    elif db.check_status(user_id) == "(False,)":
        db.update_subscription(user_id, True)
        bot.send_message(user_id, "You have subscribed")
    elif db.check_status(user_id) == "(True,)":
        bot.send_message(user_id, "Your subscription is active")
    db.print_info()


def daily_aqi_for_subs():
    """
    Function gets all subscribers and send them aqi
    """
    subscribers = db.get_subscriptions()
    for subscriber in subscribers:
        from api_request import aqi_api
        aqi_api(subscriber[1], subscriber[0])
    # Нужно получить подписчиков и город который они выбрали
    # Сделать апи запрос с этим городом


def processing_in_mailing(message, subscribe, unsubscribe, default_menu):
    """
    processing users message
    """
    if message.text in Globals.cities:
        subscribe(message)
    elif message.text == "Unsubscribe":
        unsubscribe(message)
    else:
        bot.send_message(message.chat.id,
                         "I can't understand(")
        default_menu(message)


def processing_in_continue_or_menu(message, choose_city, default_menu):
    """
    user could continue checking aqi in other cities or go to menu
    """
    if message.text == "Continue cheсking AQI":
        choose_city(message)
    elif message.text == "Menu":
        default_menu(message)
    else:
        bot.message_handler("I can't understand(")
        default_menu(message)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
