import json
import utils.PrintLog as PrintLog




configs = {}

with open( "config.json" , "r" ) as f:
    configs = json.loads( f.read() )


