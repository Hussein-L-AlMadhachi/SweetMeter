import time
import schedule
from threading import Lock , Thread

from utils.SlidingWindow import SlidingWindow_TS # TS stands for thread safe
import services.Telegram as Telegram





# =========== LOCK THESE VARIABLES WITH data_lock TO AVOID UNEXPECTED BEHAVIOR ==============
data_lock = Lock()

data = {
    "sgv":0,
    "last-sgv":0,
    "unixtime":None,
    "last-unixtime":None,
    "enhanced-delta":None,

    "delta-sgv":None,
    "is_reading_missed" : False
}

delta_window = SlidingWindow_TS( 12 )
plot_window = SlidingWindow_TS( 30 )
# ===========================================================================================



def minutes( number ):
    return number * 60


def seconds( number ):
    return number // 1000




class CGM_Metrics:


    def __init__( self ):
        self.is_reading_old = False
        self.sgv = None
        self.delta = None
        self.enhanced_delta = None


    def capture( self , svg , unixtime_ms ):
        global data_lock , data , delta_window , plot_window

        with data_lock:
            data["is_reading_missed"] = False

            # unixtime is sent in millisecond. converting to seconds
            data["unixtime"] = seconds(unixtime_ms)

            if time.time() > data["unixtime"] + minutes(7):
                self.is_reading_old = True
                return self

            if data["delta-sgv"] != None:
                data["delta-sgv"] = svg - data["last-sgv"]
                data["last-sgv"] = svg
            else:
                data["last-sgv"] = svg

            data["sgv"] = svg

            plot_window.push( data["sgv"] )
            data[ "enhanced-delta" ] = delta_window.get_nth( 5 )
            plot_window.plot()  # saving to sliding window to plot.png

            ##  setting parameters
            self.sgv = data["sgv"]
            self.delta = data["delta-sgv"]
            self.enhanced_delta = data[ "enhanced-delta" ]

        return self







def __missed_reading_alerts_poll():
    global data_lock , data , delta_window , plot_window

    with data_lock:
        timestamp = data["unixtime"]

    if (timestamp != None) and (int(time.time()) - timestamp)  > minutes(7):
        plot_window.push( 0 )
    elif (timestamp != None) and (int(time.time()) - timestamp)  > minutes(15):
        with data_lock:
            if data["is_reading_missed"]:
                return
            
            data["is_reading_missed"] = True #alert but next time avoid spamming alerts
            data["delta-sgv"] = None
            data["enhanced-delta"] = None
        
        Telegram.SendReadingTimeoutAlert()





def __start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)





schedule.every(1).seconds.do(__missed_reading_alerts_poll)

x = Thread(target=__start_scheduler)
x.start()


