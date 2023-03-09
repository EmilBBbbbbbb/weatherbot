import telebot
from config import bot_token
import requests
from pprint import pprint
from config import open_wether_token

bot=telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите город:")


@bot.message_handler()
def get_wether(message):
    try:
        r= requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_wether_token}&units=metric"
        )
        data= r.json()

        #pprint(data) #all wether

        city=message.text
        temp_now=data["main"]["temp"]
        wind = data["wind"]["speed"]
        pressure = data["main"]["pressure"]


        bot.send_message(message.chat.id, f"Погода в городе {city} на сегодня:\n"
              f"Температура: {temp_now}°С\n"
              f"Скорость ветра: {wind}м/с\n"
              f"Давление: {pressure}мм р.с\n")
    except Exception as ex:
        bot.send_message(message.chat.id,"Проверьте название города")

bot.polling(none_stop=True)