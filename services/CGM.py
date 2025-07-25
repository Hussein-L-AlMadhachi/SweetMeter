import time
import schedule
from threading import Lock , Thread

from utils.SlidingWindow import SlidingWindow_TS # TS stands for thread safe
import services.Telegram
import utils.Settings




# =========== LOCK THESE VARIABLES WITH data_lock TO AVOID UNEXPECTED BEHAVIOR ==============
data_lock = Lock()

data = {
    "sgv":0,
    "last-sgv":None,
    "unixtime":None,
    "empty-reading-unixtime":None,
    "empty_slot_unixtime" : None,
    "enhanced-delta":None,

    "delta-sgv":None,
    "is_reading_missed" : False
}

delta_window = SlidingWindow_TS( 12 )
plot_window = SlidingWindow_TS( 30 )
# ===========================================================================================



def minutes( number ):
    return number * 60


def ms_to_seconds( number ):
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
            data["unixtime"] = ms_to_seconds(unixtime_ms)
            data["empty-reading-unixtime"] = data["unixtime"]

            if time.time() > data["unixtime"] + minutes(7):
                self.is_reading_old = True
                return self

            if data["last-sgv"] == None:
                data["delta-sgv"] = 0
            else:
                data["delta-sgv"] = svg - data["last-sgv"]

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
    global data_lock , data , plot_window

    reading_timeout = minutes(15)
    if utils.Settings.configs["testing"]:   # reduce timeout to 15 seconds so you can cover all cases fast when testing
        reading_timeout = 20

    graph_reading_timeout = minutes(7)
    if utils.Settings.configs["testing"]:   # reduce timeout to 15 seconds so you can cover all cases fast when testing
        graph_reading_timeout = 10


    captured_time = int(time.time())

    with data_lock:
        timestamp = data["unixtime"]
        empty_reading_timestamp = data["empty-reading-unixtime"]


    if (empty_reading_timestamp != None) and (captured_time - empty_reading_timestamp)  > graph_reading_timeout:
        with data_lock:
            data["empty-reading-unixtime"] = captured_time
            empty_reading_timestamp = captured_time
            plot_window.push( 0 )
    
    if (timestamp != None) and (captured_time - timestamp)  > reading_timeout:
        with data_lock:

            if data["is_reading_missed"]==True:
                return
            
            data["is_reading_missed"] = True #alert but next time avoid spamming alerts
            data["delta-sgv"] = None
            data["enhanced-delta"] = None
        
        services.Telegram.SendReadingTimeoutAlert()





def __start_scheduler():
    while True:
        schedule.run_pending()

        if utils.Settings.configs["testing"]:   # reduce polling time to 1 second so you can cover all cases fast when testing
            time.sleep(3)
        else:
            time.sleep(60)




polling_time = 60
if utils.Settings.configs["testing"]:   # reduce polling time to 1 second so you can cover all cases fast when testing
    polling_time = 3


schedule.every(polling_time).seconds.do(__missed_reading_alerts_poll)

x = Thread(target=__start_scheduler)
x.start()


