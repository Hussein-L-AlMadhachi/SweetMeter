import telebot

import utils.Settings as Settings
import utils.Localize as Localize





bot = telebot.TeleBot(  Settings.configs["telegram-bot-token"]  )
chat = Settings.configs["chat-id"]





def sendReading( sgv_value , delta , enhanced_delta ):
    try:
        if delta < 0:
            enhanced_delta_str = str(enhanced_delta)
            delta_str = str(delta)
        else:
            enhanced_delta_str = "+" + str(enhanced_delta)
            delta_str = "+" + str(delta)

        bot.send_message( chat, f"{Localize.message("glucose_entry")}: \n " + str(sgv_value)+ "  " + delta_str + "     |    d: " + enhanced_delta_str )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: " , e )





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


