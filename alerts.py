import schedule
from time import sleep
#import TelegramBot


last_date = None


def setMissedReadingAlertTask():
    print("Hello World")


schedule.every(5).seconds.do(setMissedReadingAlertTask)


while True:
    schedule.run_pending()
    sleep(0.1)

