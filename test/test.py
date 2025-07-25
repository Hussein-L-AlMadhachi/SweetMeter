import requests
import json
import time
import os



base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "..", "config.json")


configs = {}
with open( config_path ) as f:
    configs = json.loads( f.read() )




domain = configs["domain"]
port = configs["chat-id"]
api_url_token = configs["api-url-token"]
protocol = "https"

if configs["testing"]:   # just so that you don't test on prod 💀
    domain = configs["testing-domain"]
    port = configs["testing-port"]
    api_url_token = configs["testing-api-url-token"]
    protocol = "http"





fake_readings = [ 
    297,309,303,305,266,255,
    224,195,175,124,130,126,
    134,143,143,139,121,119,
    122,117,114,110,107,108,
    114,120,123,125,127,130
]





url = f"{protocol}://{domain}:{port}/{api_url_token}/entries"


print( "sending readings to" , url )


for reading in fake_readings:

    headers = {'Content-Type': 'application/json'}

    data = {
        'device': 'xDrip-LibreReceiver',
        'date': int(time.time()*1000),
        'dateString': '2025-02-023T21:18:45.242+0300',
        'sgv': reading,
        'direction': 'DoubleDown'
    }

    json_data = json.dumps(data)

    try:
        response = requests.post(url, data=json_data, headers=headers)
        print( f" [*]  Fake glucose reading {reading} sent successfully" )
    except Exception as error:
        print( f"\n\n [!]  Connot send fake readings to {url}" )
        print( "\tbecause" , error )
        print( f"\n\tTip: make sure your sweetmeter is up and running and accessible on {url}" )


    time.sleep( 5 )


