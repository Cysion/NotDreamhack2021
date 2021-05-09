import telebot
from telebot import types
import time
from threading import Thread
import os
import json
from bot_add_helpers import *

TOKEN = str() 
with open("API-KEY") as f:
	TOKEN = f.read().strip()

TIME_STEP = 60


bot = telebot.TeleBot(TOKEN)

templates{
    "quest":["name", "description", "reward", "priority", "repeatable", "duration"],
    "item":["name", "description", "duration", "cost"]
}

#Template
#quest:[heroId, name, description, reward, priority, repeatable, startTime, duration],
#item:[heroId, name, description, duration, cost]
#hero:[heroId, name]

def dialogue_handler(message, key, indict):
    indict[key] = message.text 

def interactivity_handler(message, handler_type):
    result = {"heroid" = message.chat.id}
    template = templates[handler_type]
    for item in template:
        bot.send_message(chat_id, f"Please give the {handler_type} a {item}, good sir")
        bot.register_next_step_handler(message, dialogue_handler)
    print("result")
    return result


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, """
Greetings hero!
Welcome to the magical realm of Earth, where all sorts of adventures take place!
Now to get started you need to specify what you wish to get done! 
You can do this with the /addquest command, and to add items (to get rewarded for your heroics) simply use the /additem command
to summon further, and more detailed help, use the /help command
""")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, """
commands:
/addquest
/additem
/log
/shop
/register
""")


@bot.message_handler(commands=['addquest'])
def frontend_addquest(message):
	chat_id = message.chat.id
    bot.send_message(chat_id, "Let's add a new quest!")
    interactivity_handler(message, "quest")
    

@bot.message_handler(commands=['additem'])
def frontend_additem(message):
	chat_id = message.chat.id
    bot.send_message(chat_id, "Let's add a new item!")
    interactivity_handler(message, "quest")

@bot.message_handler(commands=['shop'])
def frontend_shop(message):
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
