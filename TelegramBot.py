
from time import sleep
from time import time as unixtime


import telebot


import json

try:
    with open( "config.json" , "r" ) as f:
        bot = telebot.TeleBot(  json.loads( f.read() )["telegram-bot-token"]  )
except Exception as error:
    print( "Error: make sure you have config.json with  {\"telegram-bot-token\":\"727XX27X:XXXx8XxDX5XxXxxXxxxxxxxxXXXxx6xXxxX\"}" )
    exit(-1)



chat = -1002064929281



bot.send_message( chat , "📡 عملية التشغيل تمت بنجاح 🎛️" )



def sendReading( sgv_value , delta , enhanced_delta ):
    try:
        if delta < 0:
            enhanced_delta_str = str(enhanced_delta)
            delta_str = str(delta)
        else:
            enhanced_delta_str = "+" + str(enhanced_delta)
            delta_str = "+" + str(delta)

        bot.send_message( chat, "مستوى السكر: \n " + str(sgv_value)+ "  " + delta_str + "     |    d: " + enhanced_delta_str )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: " , e )


def send_plot():
    image_path = "plot.png"
    bot.send_photo( chat , open(image_path, 'rb') )

def SendUserMisuseAlert():
    try:
        bot.send_message( chat, "😡 تحذير: حمودي كاعد يستعمل تليفونه 😡" )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: " , e )



def SendReadingTimeoutAlert():
    try:
        bot.send_message( chat, "تحذير الاتصال مقطوع لاكثر من 15 دقيقة !!!" )
    except Exception as e:
        print( str(__file__)+" Telegram bot ERROR 002: " , e )



