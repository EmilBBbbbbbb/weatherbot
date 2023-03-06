import telebot
from config import bot_token

bot=telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите город:")

bot.polling(none_stop=True)