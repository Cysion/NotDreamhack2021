import telebot
from telebot import types
import time
from threading import Thread
import os
import json


TOKEN = str() 
with open("API-KEY") as f:
	TOKEN = f.read().strip()

TIME_STEP = 60


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, """
Greetings hero!
Welcome to the magical realm of Earth, where all sorts of adventures take place!
Now to get started you need to specify what you wish to get done! 
You can do this with the /addquest command, and to add items (to get rewarded for your heroics) simply use the /additem command
to summon further, and more detailed help, use the /help command
""")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, """
commands:
/addquest
/additem

""")

@bot.message_handler(commands=['remind'])
def remind(message):
    pass


def main():
    poll_thread = Thread(target=poll)
    poll_thread.start()
    while(True):



def poll():
    bot.polling(True)


@bot.message_handler(func=lambda m: True)
def echo_all(message):     
    bot.send_message(message.chat.id, "Command unknown, try again.")

if __name__ == "__main__":
    main()
