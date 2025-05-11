import json
import time
import schedule
import datetime

from threading import Lock , Thread


from flask import Flask, jsonify , request
from waitress import serve

from sliding_window import SlidingWindow
import TelegramBot


API_URL = "6BqS5fkRjvW0oD8FpdyahTrNG3cewzgI"


app = Flask(__name__)



data_lock = Lock()

data = {
    "sgv":0,
    "last-sgv":0,
    "unixtime":None,
    "last-unixtime":None,
    "enhanced-delta":None,

    "delta-sgv":None,
    "UploaderBattery":0
}





delta_triangle_window = SlidingWindow( 12 )
plot_window = SlidingWindow( 30 )




@app.route(f"/{API_URL}/status")
@app.route(f"/{API_URL}/status.json")
def GetStatus():
    with open( "status.json" , "r" ) as f:
        self_status = json.loads( f.read() )
    return jsonify(self_status) , 200





@app.route(f"/{API_URL}/entries" , methods=["POST"] )
def Entries():
    # extract data
    print( "-- data entry" )
    # NOTE: all the datetime is all in unix in milliseconds
    sensor_data = request.get_json()
    print( sensor_data )


    # error handling
    if not "sgv" in sensor_data:
        return "" , 403

    print( "sensor data: at", time.time()*1000 ,"\n   " , sensor_data )

    # delta calculation
    with data_lock:
        # unixtime is sent in millisecond. converting to seconds
        data["unixtime"] = sensor_data["date"] // 1000
        
        if time.time() > data["unixtime"] + 60*15 :
            return  jsonify([]) , 200


        if data["delta-sgv"] != None:
            data["delta-sgv"] = sensor_data["sgv"] - data["last-sgv"]
            data["last-sgv"] = sensor_data["sgv"]
        else:
            data["delta-sgv"] = 0
            data["last-sgv"] = sensor_data["sgv"]

        data["sgv"] = sensor_data["sgv"]



        plot_window.push( data["sgv"] )
        data[ "enhanced-delta" ] = delta_triangle_window.get_nth( 5 )
        plot_window.plot()

        TelegramBot.send_plot()
        TelegramBot.sendReading( sensor_data["sgv"] , data[ "delta-sgv" ] , data[ "enhanced-delta" ] )
    
    return  jsonify([]) , 200

    return f'""\t{sensor_data["date"]}\t{sensor_data["sgv"]}\t\"{sensor_data["direction"]}\"\t\"sensor_data["device"]\"' , 200





@app.route(f"/{API_URL}/devicestatus" , methods=["POST"] )
def DeviceStatus():
    device_status_data = request.get_json()
    print( device_status_data )

    with data_lock:
        delta_uploader_battery = data["UploaderBattery"] - int(device_status_data["uploader"]["battery"])

        if delta_uploader_battery > 1:
            TelegramBot.SendUserMisuseAlert()

        data["UploaderBattery"] = int(device_status_data["uploader"]["battery"])

    return "" , 200


@app.route(f"/{API_URL}/test/timeout" , methods=["GET"] )
def test_timeout():
    try:
        TelegramBot.SendReadingTimeoutAlert()
        return "hello"
    except Exception as err:
        return str(err) , 200



def missed_reading_alert():
    print("iter")
    with data_lock:
        reading = data["sgv"]
        timestamp = data["unixtime"]
        battery = data["UploaderBattery"]

    if (timestamp != None) and (int(time.time()) - timestamp)  > 420:
        plot_window.push( 0 )

    if (timestamp != None) and (int(time.time()) - timestamp)  > 900:
        data["delta-sgv"] = None
        TelegramBot.SendReadingTimeoutAlert()





def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)





if __name__ == "__main__":
    schedule.every(1).seconds.do(missed_reading_alert)

    x = Thread(target=start_scheduler )
    x.start()

    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=5000)




