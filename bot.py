import telebot
from config import bot_token
import requests
from config import week
from config import month
from config import code_to_smile
from config import open_wether_token
from datetime import datetime
from telebot import types

bot=telebot.TeleBot(bot_token)

city=None
chat_id=None

chch=False
def dataweek(plus):
    a = datetime.weekday(datetime.now()) + plus
    if a > 6:
        a-=7
    return week[a]


def wether_day(data, day, chat_id):
    dt=data["list"][8*day]["dt_txt"][:10]
    temp=data["list"][8*day]["main"]["temp"]
    wind=data["list"][8*day]["wind"]["speed"]
    weather_description = data["list"][8*day]['weather'][0]["main"]

    marckup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton("Сегодня")
    item1 = types.KeyboardButton("Завтра")
    item2 = types.KeyboardButton("5 дней")

    marckup.add(item0, item1, item2)

    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, не пойму что там за погода!"

    bot.send_message(chat_id, f"Погода на {dataweek(day)}, {dt[8:]} {month[dt[5:7]]}:\n"
                f"\n "
              f"\U0001F321 Температура: {temp}°С\n"
                              f"\n "
              f"\U0001F32C Скорость ветра: {wind}м/с\n"
                              f"\n "
              f"\U0001FA9F Погода на улице: {wd}", reply_markup=marckup)



@bot.message_handler(commands=["start","city"])
def start(message):
    bot.send_message(message.chat.id, "Введите город:")

    return True


@bot.message_handler(content_types=["text"])
def get_wether(message):
    global city
    global chat_id
    chat_id = message.chat.id
    if message.text == "Завтра":
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_wether_token}&units=metric"
            )
            data = r.json()
            wether_day(data, 1, chat_id)
        except Exception as ex:
            print(ex)

    elif message.text == "5 дней":
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_wether_token}&units=metric"
            )
            data = r.json()

            wether_day(data, 0, chat_id)
            wether_day(data, 1, chat_id)
            wether_day(data, 2, chat_id)
            wether_day(data, 3, chat_id)
            wether_day(data, 4, chat_id)
        except Exception as ex:
            print(ex)

    elif message.text == "Сегодня":
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_wether_token}&units=metric"
            )
            data = r.json()
            wether_day(data, 0, chat_id)
        except Exception as ex:
            print(ex)


    else:
        city = message.text
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_wether_token}&units=metric"
            )
            data = r.json()
            wether_day(data, 0, chat_id)
        except Exception as ex:
            print(ex)


bot.polling(none_stop=True)