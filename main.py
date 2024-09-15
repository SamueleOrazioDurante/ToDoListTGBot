import telebot # telegram bot manager

# general utilities


# script
import tokenManager
import logger
import database

BOT_TOKEN = tokenManager.read_bot_token()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot
database.init()

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    logger.command(message)

    f = open("patchnotes", "r") # reads and return entire file
    bot.send_message(message.chat.id, f.read())

@bot.message_handler(commands=['new_list', 'Crea una nuova lista'])
def create_new_list(message):

    logger.command(message)
# DA AGGIUNGERE, ELIMINA PRIMO MESSAGGIO
#CHIEDI NOME LISTA
# ELIMINA RICHIESTA E RISPOSTA
# MANDA MESSAGGIO DI OCNFERMA CREASIONE NUOVA LISTA
# ELIMINA IL MESSAGGIO DOPO 5/10 SECONDI
    database.new_list(message.chat.id,"Test1")
    bot.send_message(message.chat.id, "Lista creata")

logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")

bot.polling() # bot start   