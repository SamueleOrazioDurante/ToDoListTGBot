import telebot # telegram bot manager

# general utilities
import time

# script
import tokenManager
import logger
import database

BOT_TOKEN = tokenManager.read_bot_token()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot
database.init()

def see_specific_list(chat_id,list_id):

    if(list_id == "-1"): # no list has list_id of -1 (so we need to print main lists)

        see_all_lists(chat_id)

    else:

        row = database.get_list_data(list_id) # ask db for name and master_id
        lists = database.get_list_lists(list_id) # ask db for slave lists
        todos = database.get_list_todos(list_id) # ask db for todo

        markup = telebot.types.InlineKeyboardMarkup(row_width=4) # markup for answer

        for list in lists:
            markup.add(telebot.types.InlineKeyboardButton(list[0], callback_data="list"+str(list[1]))) # add all lists

        for todo in todos:
            markup.add(telebot.types.InlineKeyboardButton(todo[0], callback_data="todo"+str(todo[1]))) # add all todos
        
        markup.add(telebot.types.InlineKeyboardButton("Aggiungi lista", callback_data="addlist"+list_id)) # add list button (with list_id)
        markup.add(telebot.types.InlineKeyboardButton("Aggiungi todo", callback_data="addtodo"+list_id)) # add todo button (with list_id)
        markup.add(telebot.types.InlineKeyboardButton("🔙Esci", callback_data="back"+str(row[1]))) # exit button (with master id to define exit position [-1 = all main lists, other value = list that have that particular id_list] )

        bot.send_message(chat_id, row[0], reply_markup=markup)

def see_all_lists(chat_id):
    lists = database.get_list(chat_id) # get lists name from db

    markup = telebot.types.InlineKeyboardMarkup(row_width=4) # markup for answer

    for list in lists:
        markup.add(telebot.types.InlineKeyboardButton(list[0], callback_data="list"+str(list[1])))

    markup.add(telebot.types.InlineKeyboardButton("Aggiungi lista", callback_data="addlist"+"-1")) # add list button (with master id, in this case -1 cuz is a main list)
    markup.add(telebot.types.InlineKeyboardButton("🔙Esci", callback_data="back")) # exit button

    bot.send_message(chat_id, "Seleziona la lista:", reply_markup=markup)

def create_new_todo(message,question,master_id):

    todo_name = message.text

    bot.delete_message(message.chat.id,question.id) # delete question to user
    bot.delete_message(message.chat.id,message.id) # delete answer

    database.new_todo(todo_name,master_id)

    confirm = bot.send_message(message.chat.id, "Todo creato con nome "+todo_name)

    see_specific_list(message.chat.id,master_id)

    time.sleep(5) # wait 5 seconds before deleting confirm
    bot.delete_message(message.chat.id,confirm.id) # delete confirmation

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    logger.command(message)

    f = open("patchnotes", "r") # reads and return entire file
    bot.send_message(message.chat.id, f.read())

@bot.message_handler(commands=['new_list', 'Crea una nuova lista'])
def new_list(message):

    logger.command(message)

    bot.delete_message(message.chat.id,message.id) # delete command

    question = bot.send_message(message.chat.id, "Nome lista") 

    bot.register_next_step_handler(message,create_new_list,question,-1)

def create_new_list(message,question,master_id):

    list_name = message.text

    bot.delete_message(message.chat.id,question.id) # delete question to user
    bot.delete_message(message.chat.id,message.id) # delete answer

    database.new_list(message.chat.id,list_name,master_id)

    confirm = bot.send_message(message.chat.id, "Lista creata con nome "+list_name)

    see_specific_list(message.chat.id,master_id)

    time.sleep(5) # wait 5 seconds before deleting confirm
    bot.delete_message(message.chat.id,confirm.id) # delete confirmation

@bot.message_handler(commands=['my_list', 'Visualizza tutte le proprie liste'])

def see_list(message):

    logger.command(message)

    bot.delete_message(message.chat.id,message.id) # delete command

    see_all_lists(message.chat.id)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    
    # main back
    if call.data == "back":
        bot.delete_message(call.message.chat.id,call.message.id)    

    # back from a list 
    elif call.data[:4] == "back":
        master_id = call.data[4:]
        bot.delete_message(call.message.chat.id,call.message.id)

        if master_id == "-1": # if its a main list then print all main lists
            see_all_lists(call.message.chat.id)
        else:               # else print master list 
            see_specific_list(call.message.chat.id,master_id)
    
    # create a new list
    elif call.data[:7] == "addlist":
        
        master_id = call.data[7:]
        bot.delete_message(call.message.chat.id,call.message.id)

        question = bot.send_message(call.message.chat.id, "Nome lista") 

        bot.register_next_step_handler(call.message,create_new_list,question,master_id)

    # create a new todo
    elif call.data[:7] == "addtodo":
        
        master_id = call.data[7:]
        bot.delete_message(call.message.chat.id,call.message.id)

        question = bot.send_message(call.message.chat.id, "Nome todo") 

        bot.register_next_step_handler(call.message,create_new_todo,question,master_id)

    elif call.data[:4] == "list":
        
        id_list = call.data[4:]

        bot.delete_message(call.message.chat.id,call.message.id) # delete lists message

        see_specific_list(call.message.chat.id,id_list)

    elif call.data[:4] == "todo":
        
        id_todo = call.data[4:]

        bot.delete_message(call.message.chat.id,call.message.id) # delete lists message

        bot.send_message(call.message.chat.id,"todo rilevato")
    
    else:
        bot.send_message(call.message.chat.id,"Ciao daddy")


logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")


bot.polling() # bot start   