import telebot
from telebot import types
import time
from threading import Thread
import os
import json
import quest_manager


TOKEN = str() 
with open("API-KEY") as f:
	TOKEN = f.read().strip()

TIME_STEP = 60
TIMEOUT = 60

bot = telebot.TeleBot(TOKEN)

templates = {
    "quest":["name", "description", "reward", "priority", "repeatable", "start time", "duration"],
    "item":["name", "description", "duration", "cost"]
}

#Template
#quest:[heroId, name, description, reward, priority, repeatable, startTime, duration],
#item:[heroId, name, description, duration, cost]
#hero:[heroId, name]

def dialogue_handler(message, key, indict):
    indict[key] = message.text 

def interactivity_handler(message, handler_type):
    result = {"heroid": message.chat.id}
    template = templates[handler_type]
    for item in template:
        bot.send_message(message.chat.id, f"Please give the {handler_type} a {item}, good sir")
        bot.register_next_step_handler(message, dialogue_handler, item, result)
        slept = 0
        while item not in result.keys():
            if slept >= TIMEOUT:
                bot.send_message(message.chat.id, "You'll have to be faster than that if you want to be a hero, sir")
                raise TimeoutError("user too slow")
            time.sleep(0.5)
    return result


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, """
Greetings hero!
Welcome to the magical realm of Earth, where all sorts of adventures take place!
I will me your questmaster, the good honorable sir Botalot, as employed by ';DROP ALL TABLES
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
/register [name]
""")

backend_adders = {
    "quest":quest_manager.addQuest,
    "item":quest_manager.addItem
}

@bot.message_handler(commands=['addquest', "additem"])
def frontend_add(message):
    #CHECK ID
    chat_id = message.chat.id
    desctype = message.text[4:]
    bot.send_message(chat_id, f"Let's add a new {desctype}!")
    #addbot = Thread(target=interactivity_handler, args=(message, desctype))
    try:
        to_backend = interactivity_handler(message, desctype)
        backend_adders[desctype](to_backend)
    except TimeoutError:
        pass
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the gobins said it was {e}")
    return

@bot.message_handler(commands=['shop'])
def frontend_shop(message):
    #CHECK ID
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    shop, balance = quest_manager.getShop(chat_id)
    formatted_shop = ("\n".join([f"{x}:{item[x]}" for x in item.keys()]) for item in shop)
    options = []
    for ind in range(len(formatted_shop)):
        formatted_shop[ind] = "{ind}:\n" + formatted_shop[ind]
        options.append(types.KeyboardButton(str(ind)))
    try:
        for i in range(options % 4):
            markup.row(options)
    except:
        pass


    while "=(":
        if slept >= TIMEOUT:
            bot.send_message(message.chat.id, "You'll have to be faster than that if you want to be a hero, sir")
            raise TimeoutError("user too slow")
        time.sleep(0.5)
    #markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, "choose letter", reply_markup=markup)

    return

@bot.message_handler(commands=['register'])
def frontend_register(message):
    name = message.text.split(" ")[-1]
    try:
        herodict={"heroid":message.chat.id, "name":name}
        quest_manager.registerHero(herodict)
    except Exception:
        pass
    bot.send_message(message.chat.id, f"Welcome to the guild of heroes, {name}")

def poll():
    bot.polling(True)

def main():
    bot.polling(True)
    """poll_thread = Thread(target=poll)
    poll_thread.start()
    while(True):
        time.sleep(TIME_STEP)"""
        
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Command unknown, try again.")

if __name__ == "__main__":
    main()
