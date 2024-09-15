import telebot # telegram bot manager

# general utilities


# script
import tokenManager
import logger

BOT_TOKEN = tokenManager.read_bot_token()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    logger.command(message)

    f = open("patchnotes", "r") # reads and return entire file
    bot.send_message(message.chat.id, f.read())

logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")

bot.polling() # bot start   