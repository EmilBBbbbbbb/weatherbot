import telebot
from config import bot_token
import requests
from config import week
from config import open_wether_token
from  datetime import  datetime

bot=telebot.TeleBot(bot_token)

def data(plus):
    a = datetime.weekday( datetime.now())+plus
    if a>6:
        a-=6
    return week[a]

def wether_day(data, day, chat_id):
    dt=data["list"][8*day]["dt_txt"][:10]
    temp=data["list"][8*day]["main"]["temp"]
    wind=data["list"][8*day]["wind"]["speed"]
    bot.send_message(chat_id, f"Погода на {dt}:\n"
              f"Температура: {temp}°С\n"
              f"Скорость ветра: {wind}м/с\n")
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите город:")


@bot.message_handler()
def get_wether(message):
    try:
        r= requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={message.text}&appid={open_wether_token}&units=metric"
        )
        data= r.json()
        chat_id = message.chat.id

        wether_day(data, 1,chat_id)



    except Exception as ex:
        bot.send_message(message.chat.id,"Проверьте название города")

bot.polling(none_stop=True)