import json
import utils.PrintLog as PrintLog




configs = {}

with open( "config.json" ) as f:
    configs = json.loads( f.read() )


