import schedule
from threading import Thread

from api_request import aqi_api
from Functions import buttons_in_default_menu, button_in_mailing, \
    buttons_choose_city, button_in_subscribe, \
    schedule_checker, \
    processing_in_mailing, \
    processing_in_continue_or_menu, \
    daily_aqi_for_subs, check_user_subscribe, check_user_unsubscribe
from Globals import bot, Globals


@bot.message_handler(commands=["start"])
def start(message):
    """
    start of the program
    """
    start_message = bot.send_message(message.chat.id, Globals.str_welcome)
    default_menu(start_message)


@bot.message_handler(command=["menu"])
def default_menu(message):
    """
    In defaul menu 2 buttons
    """
    keyboard = buttons_in_default_menu()
    menu_question = bot.send_message(message.chat.id,
                                     Globals.str_def_menu,
                                     reply_markup=keyboard)
    bot.register_next_step_handler(menu_question, menu)


@bot.message_handler(content_types=["text"])
def menu(message):
    process_menu(message, choose_city, mailing_buttons,
                 help, subscribe, unsubscribe)


def process_menu(message, choose_city, mailing_buttons, help,
                 subscribe, unsubscribe):
    """
    processing received commands
    """
    commands_list = {"Check the AQI now": choose_city,
                     "/help": help,
                     "Receive daily": mailing_buttons,
                     "/subscribe": mailing_sub,
                     "/unsubscribe": unsubscribe,
                     "/aqi": choose_city}
    if message.text in commands_list.keys():
        commands_list[message.text](message)
    elif message.text == "/subscribe":
        for_subscribers()
    else:
        bot_does_not_understand(message)


def bot_does_not_understand(message):
    """
    this funtion used everytime when bot can't understand the user's message
    """
    bot.send_message(message.chat.id, "I can't understand you")
    default_menu(message)


def mailing_buttons(message):
    """
    buttons of mailing
    """
    keyboard = button_in_mailing()
    mailing_message = bot.send_message(message.chat.id,
                                       Globals.mailing_question_text,
                                       reply_markup=keyboard)
    bot.register_next_step_handler(mailing_message, mailing)


def mailing(message):
    """
    receive daily, for subscribe additional one function
    """
    if message.text == "Subscribe":
        keyboard = button_in_subscribe()
        city_to_sub = bot.send_message(message.chat.id,
                                       Globals.sub_city,
                                       reply_markup=keyboard)
        bot.register_next_step_handler(city_to_sub, mailing_sub)
    elif message.text == "Back":
        default_menu(message)
    else:
        processing_in_mailing(message, subscribe, unsubscribe, default_menu)


def mailing_sub(message):
    processing_in_mailing(message, subscribe, unsubscribe, default_menu)


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    check_user_subscribe(message, default_menu)
    default_menu(message)


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    check_user_unsubscribe(message)
    default_menu(message)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, Globals.help_message)


@bot.message_handler(commands=["aqi"])
def choose_city(message):
    """
    selecting city for aqi
    """
    keyboard = buttons_choose_city()
    chosen_city = bot.send_message(message.chat.id,
                                   "In which city do you want to know the air quality? 🌤",
                                   reply_markup=keyboard)
    print("in choose_city:  ", message.text)

    bot.register_next_step_handler(chosen_city, aqi_city)


def process_chosen_city(message):
    bot.register_next_step_handler(message, aqi_city)


def aqi_city(message):
    aqi_text = aqi_api(message.text, message.chat.id)
    bot.register_next_step_handler(aqi_text, continue_or_menu)


def continue_or_menu(message):
    """
    continue checking aqi in other cities or go to menu
    """
    processing_in_continue_or_menu(message, choose_city, default_menu)


@bot.message_handler(commands=["receive"])
def for_subscribers():
    """
    Sending all information to subscribers
    """
    daily_aqi_for_subs()


if __name__ == "__main__":
    schedule.every().day.at("10:00").do(for_subscribers)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True, interval=0)
  
