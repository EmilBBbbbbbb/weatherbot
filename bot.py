import telebot
from config import bot_token
import requests
from config import week
from config import open_wether_token
from  datetime import  datetime
from telebot import types

bot=telebot.TeleBot(bot_token)

city=None
chat_id=None

chch=False
def data(plus):
    a = datetime.weekday(datetime.now()) + plus
    if a > 6:
        a-=6
    return week[a]


def wether_day(data, day, chat_id):
    dt=data["list"][8*day]["dt_txt"][:10]
    temp=data["list"][8*day]["main"]["temp"]
    wind=data["list"][8*day]["wind"]["speed"]

    marckup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton("Сегодня")
    item1 = types.KeyboardButton("Завтра")
    item2 = types.KeyboardButton("5 дней")

    marckup.add(item0, item1, item2)

    bot.send_message(chat_id, f"Погода на {dt}:\n"
              f"Температура: {temp}°С\n"
              f"Скорость ветра: {wind}м/с\n", reply_markup=marckup)



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