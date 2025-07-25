import telebot

import utils.Settings
import utils.Localize as Localize




telegram_token = utils.Settings.configs["telegram-bot-token"]
chat = utils.Settings.configs["chat-id"]

if utils.Settings.configs["testing"]:   # just so that you don't test on prod 💀
    telegram_token = utils.Settings.configs["testing-telegram-bot-token"]
    chat = utils.Settings.configs["testing-chat-id"]





bot = telebot.TeleBot( telegram_token )





def sendReading( sgv_value , delta , enhanced_delta ):

    if delta == None:
        delta = 0


    if delta < 0:
        enhanced_delta_str = str(enhanced_delta)
        delta_str = str(delta)
    else:
        enhanced_delta_str = "+" + str(enhanced_delta)
        delta_str = "+" + str(delta)

    try:

        bot.send_message( chat, f"{ Localize.message('glucose_entry') }: \n " + str(sgv_value)+ "  " + delta_str + "     |    d: " + enhanced_delta_str )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: cannot send reading" , e )





def send_plot():
    image_path = "plot.png"
    bot.send_photo( chat , open(image_path, 'rb') )





def SendReadingTimeoutAlert():
    try:
        bot.send_message( chat, Localize.message("missed_reading") )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: " , e )





def send_boot_message():
    bot.send_message( chat , Localize.message("boot_message") )
    print( "Sweetmeter Telegram service started succefully" )


