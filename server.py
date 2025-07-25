from flask import Flask, jsonify , request
from waitress import serve


import utils.Settings as Settings
import utils.PrintLog  # silently overwrites builtin print and turns it into a logger (check sweetmeter.log)

import services.Telegram
import services.Status
import services.CGM
import utils.Settings





API_URL = Settings.configs["api-url-token"]
if utils.Settings.configs["testing"]:   # just so that you don't test on prod 💀
    API_URL = Settings.configs["testing-api-url-token"]

app = Flask(__name__)







@app.route(f"/{API_URL}/status")
@app.route(f"/{API_URL}/status.json")
def GetStatus():
    return jsonify( services.Status.getStatusFile() ) , 200





@app.route(f"/{API_URL}/entries" , methods=["POST"] )
@app.route(f"/{API_URL}/entries.json" , methods=["POST"] )
@app.route(f"/{API_URL}/api/v1/entries" , methods=["POST"] )
@app.route(f"/{API_URL}/api/v1/entries.json" , methods=["POST"] )
def Entries():
    sensor_data = request.get_json()
    print( "received" , sensor_data )

    # error handling
    if not "sgv" in sensor_data or not "date" in sensor_data:
        return "" , 403

    sgv_value = sensor_data["sgv"]
    unixtime_ms = sensor_data["date"]

    cgm_reading = services.CGM.CGM_Metrics()
    cgm_reading.capture( sgv_value , unixtime_ms )

    if cgm_reading.is_reading_old:
        return jsonify([]) , cgm_reading , 200

    services.Telegram.send_plot()
    services.Telegram.sendReading( cgm_reading.sgv , cgm_reading.delta , cgm_reading.enhanced_delta )
    
    return  jsonify([]) , 200





# setting server addresses

listen_host = utils.Settings.configs["listen"]
listen_port = utils.Settings.configs["port"]

if utils.Settings.configs["testing"]:   # just so that you don't test on prod 💀
    listen_host = utils.Settings.configs["testing-listen"]
    listen_port = utils.Settings.configs["testing-port"]


services.Telegram.send_boot_message()
serve(app, host=listen_host, port=listen_port)




