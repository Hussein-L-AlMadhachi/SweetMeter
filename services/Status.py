import json


with open( "status.json" , "r" ) as f:
    self_status = json.loads( f.read() )

def getStatusFile():
    return self_status


