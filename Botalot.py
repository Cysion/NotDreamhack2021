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

TIME_STEP = 5
TIMEOUT = 60

bot = telebot.TeleBot(TOKEN)

templates = {
    "quest":["name", "description", "reward", "priority", "repeatable", "start time", "duration", "active"],
    "item":["name", "description", "duration", "cost"]
}


backend_adders = {
    "quest":quest_manager.addQuest,
    "item":quest_manager.addItem
}

#Template
#quest:[heroId, name, description, reward, priority, repeatable, startTime, duration],
#item:[heroId, name, description, duration, cost]
#hero:[heroId, name]

def dialogue_handler(message, key, indict):
    indict[key] = message.text 

def simple_dialogue_handler(message, returnable):
    returnable = message.text

def interactivity_handler(message, handler_type):
    chat_id = message.chat.id
    result = {"heroid": chat_id}
    template = templates[handler_type]
    for item in template:
        bot.send_message(chat_id, f"Please give the {handler_type} a {item}, good sir")
        bot.register_next_step_handler(message, dialogue_handler, item, result)
        slept = 0
        while item not in result.keys():
            if slept >= TIMEOUT:
                bot.send_message(chat_id, "You'll have to be faster than that if you want to be a hero, sir")
                #raise TimeoutError("user too slow")
                return
            time.sleep(0.5)
    #return result
    try:
        backend_adders[desctype](result)
        bot.send_message(chat_id, f"Quest sucessfully added!")
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return
    


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
You already forgot the commands sir?
Well here they are
commands:
/register [name]
/cheat [code]

quests:
/addquest
/log
/log inactive
/start [id]
/turnin [id]
/abandon [id]

items:
/additem
/shop
/buy [id]
""")

@bot.message_handler(commands=['cheat'])
def send_help(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    code = message.text.split(" ")[-1]
    codes = {
        "rosebud":quest_manager
    }
    if not code in codes:
        bot.send_message(chat_id, "thats not a valid cheat code!")
    else:
        codes[code]



@bot.message_handler(commands=['addquest', "additem"])
def frontend_add(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        #return
    chat_id = message.chat.id
    desctype = message.text[4:]
    bot.send_message(chat_id, f"Let's add a new {desctype}!")
    addbot = Thread(target=interactivity_handler, args=(message, desctype))
    addbot.start()
    """
    try:
        to_backend = interactivity_handler(message, desctype)
        backend_adders[desctype](to_backend)
    except TimeoutError:
        pass
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return
    """

@bot.message_handler(commands=['log', 'log inactive'])
def frontend_log(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    loglist = quest_manager.getQuestLog(chat_id, "inactive" not in message.text)
    sendable = ""
    for quest in loglist:
        for key in quest:
            sendable += key + ":" + quest[key]
    bot.send_message(chat_id, sendable)



@bot.message_handler(commands=['shop'])
def frontend_shop(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    shop, balance = quest_manager.getShop(chat_id)
    formatted_shop = ("\n".join([f"{x}:{item[x]}" for x in item.keys()]) for item in shop)
    for ind in range(len(formatted_shop)):
        formatted_shop[ind] = "{ind}:\n" + formatted_shop[ind]
        options.append(str(ind))
    balance = f"Your account balance is: {balance}\n"
    bot.send_message(chat_id, balance + formatted_shop)
    """
    slept = 0
    selection = ""
    
    bot.register_next_step_handler(message, simple_dialogue_handler, selection)
    while not selection:
        if slept >= TIMEOUT:
            bot.send_message(message.chat.id, "You'll have to be faster than that if you want to be a hero, sir")
            raise TimeoutError("user too slow")
        time.sleep(0.5)
        slept += 0.5
    """


@bot.message_handler(commands=['buy'])
def frontend_buy(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    try:
        selection = int(message.text.split(" ")[-1])
        quest_manager.purchase(chat_id, selection)
        bot.send_message(chat_id, "Purchase completed, sir!")
        print(chat_id, " bought ", selection)
    except TypeError:
        bot.send_message(chat_id, f"Whatever {selection} is, it's not in the shop, sir!")
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return




@bot.message_handler(commands=['register'])
def frontend_register(message):
    if len(message.text.split(" ")) < 2:
        bot.send_message(message.chat.id, f"You gave me no name sir!")
    else:
        name = message.text.split(" ")[-1]
        try:
            herodict={"heroid":message.chat.id, "name":name}
            quest_manager.registerHero(herodict)
            print(herodict)
        except ValueError:
            bot.send_message(message.chat.id, f"Sir, you are already registered!")
        except Exception:
            bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
        return
        bot.send_message(message.chat.id, f"Welcome to the guild of heroes, {name}")

@bot.message_handler(commands=['turnin'])
def frontend_turnin(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    try:
        selection = int(message.text.split(" ")[-1])
        quest_manager.turnIn(chat_id, selection)
        bot.send_message(chat_id, "Quest completed, sir!")
        print(chat_id, " turned in ", selection)
    except TypeError:
        bot.send_message(chat_id, f"Whatever {selection} is, it's not a quest, sir!")
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return

@bot.message_handler(commands=['abandon'])
def frontend_abandon(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    try:
        selection = int(message.text.split(" ")[-1])
        quest_manager.abandon(chat_id, selection)
        bot.send_message(chat_id, "Quest successfully failed, sir!")
        print(chat_id, " abandoned ", selection)
    except TypeError:
        bot.send_message(chat_id, f"Whatever {selection} is, it's not a quest, sir!")
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return

@bot.message_handler(commands=['start'])
def frontend_start(message):
    chat_id = message.chat.id
    if not quest_manager.checkId(chat_id):
        bot.send_message(chat_id, "You're not registered")
        return
    try:
        selection = int(message.text.split(" ")[-1])
        quest_manager.start(chat_id, selection)
        bot.send_message(chat_id, "Very good sir, I will make the appropriate entry in your log")
        print(chat_id, " started ", selection)
    except TypeError:
        bot.send_message(chat_id, f"Whatever {selection} is, it's not a quest, sir!")
    except Exception as e:
        bot.send_message(chat_id, f"something terrible happened on the back end, sir. the goblins said it was {e}")
    return


def quest_request(quest):
    hero_id = quest["heroid"]
    sendable = "There is a new quest for you, hero! Here are the details...\n"
    for key in quest:
        sendable += f"{key}:{quest[key]}"
    
    markup = types.ReplyKeyboardMarkup()
    itembtny = types.KeyboardButton('Yes')
    itembtnn = types.KeyboardButton('No')
    markup.row(itembtna, itembtnn)
    tb.send_message(chat_id, sendable + "Will you take the quest?", reply_markup=markup)
    markup = types.ReplyKeyboardRemove(selective=False)
    selection = ""
    while not selection:
        if slept >= TIMEOUT:
            bot.send_message(message.chat.id, "You'll have to be faster than that if you want to be a hero, sir")
            return
        time.sleep(0.5)
    sendable = ""
    if selection == "Yes":
        sendable = "Very well sir, I will add the quest to your log!"
    elif selection == "No":
        sendable = "Sir, you know that heroes have to complete quests, no?"
    else:
        sendable = f"What the blazes do you you mean by {selection} sir?"
    
    tb.send_message(chat_id, message, reply_markup=markup)

    bot.send_message()


def poll():
    bot.polling(True)

def main():
    poll_thread = Thread(target=poll)
    poll_thread.start()
    while(True):
        print("tick")
        time.sleep(TIME_STEP)
        
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, "What in the blazes are you trying to say, sir?")

if __name__ == "__main__":
    main()
